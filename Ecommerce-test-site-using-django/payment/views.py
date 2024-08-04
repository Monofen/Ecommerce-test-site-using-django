
import uuid
import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib import messages
import logging
from authentication.models import UserProfile
from cart.models import CartItem, Purchase
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from payment.models import PaymentTransaction

logger = logging.getLogger(__name__)

def initiate_payment(request):
    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = request.build_absolute_uri('/payment/verify/')
        purchase_order_id = str(uuid.uuid4())  
        amount = int(float(request.POST['amount']) * 100)
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        
        user_profile = UserProfile.objects.filter(user=request.user).first()
        phone_number = user_profile.phone_number if user_profile else "9812345678"

        payload = json.dumps({
            "return_url": return_url,
            "website_url": "http://127.0.0.1:8000/",
            "amount": amount,
            "purchase_order_id": purchase_order_id,  
            "purchase_order_name": product_name,
            "customer_info": {
                "name": request.user.username,
                "email": request.user.email,
                "phone": phone_number
            }
        })

        headers = {
            'Authorization': f'Key {settings.KHALTI_API_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()

        if response.status_code == 200:
            PaymentTransaction.objects.create(
                user=request.user,
                product_id=product_id,
                purchase_order_id=purchase_order_id,
                amount=amount
            )
            return redirect(response_data['payment_url'])
        else:
            messages.error(request, "Failed to initiate payment. Please try again.")
            return redirect('payment:failure')
    else:
        return HttpResponseBadRequest("Invalid request method")


def payment_success(request):
    return render(request, 'payment/success.html')

def payment_failure(request):
    return render(request, 'payment/failure.html')

@login_required
def verify_payment(request):
    if request.method == 'GET':
        try:
            pidx = request.GET.get('pidx')
            purchase_order_id = request.GET.get('purchase_order_id')  
            if not pidx or not purchase_order_id:
                return HttpResponseBadRequest("Missing pidx or purchase_order_id parameter")

            url = "https://a.khalti.com/api/v2/epayment/lookup/"
            payload = {'pidx': pidx}
            headers = {
                'Authorization': f'Key {settings.KHALTI_API_KEY}',
                'Content-Type': 'application/json',
            }

            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()

            logger.debug("Payment verification response: %s", response_data)

            if response_data.get('status') == 'Completed':
                payment_transaction = PaymentTransaction.objects.filter(purchase_order_id=purchase_order_id).first()
                if payment_transaction:
                    cart_items = CartItem.objects.filter(user=request.user, product=payment_transaction.product)
                    if cart_items.exists():
                        total_quantity = sum(item.quantity for item in cart_items)
                        
                        user_profile = UserProfile.objects.filter(user=request.user).first()
                        phone_number = user_profile.phone_number if user_profile else "Unknown"
                        address = user_profile.address if user_profile else "Unknown"

                        purchase = Purchase.objects.create(
                            user=request.user,
                            product=payment_transaction.product,
                            quantity=total_quantity,
                            phone=phone_number,
                            address=address
                        )
                        
                        payment_transaction.status = 'Completed'
                        payment_transaction.save()

                        CartItem.objects.filter(user=request.user, product=payment_transaction.product).delete()

                        # Send email
                        bill_details = f"Product: {purchase.product.name}\nQuantity: {purchase.quantity}\nPrice per unit: ${(purchase.product.sale_price if purchase.product.on_sale else purchase.product.price):.2f}\nTotal: ${(purchase.product.sale_price if purchase.product.on_sale else purchase.product.price) * purchase.quantity:.2f}\nGrand Total: ${(purchase.product.sale_price if purchase.product.on_sale else purchase.product.price) * purchase.quantity:.2f}\n"
                        subject = "Purchase Complete"
                        message = f"Hello {request.user.first_name},\n\nYour transaction was completed successfully!\nThank you for your purchase.\n\n{bill_details}\nThank you!"
                        from_email = settings.EMAIL_HOST_USER
                        to_email = [request.user.email]

                        try:
                            email = EmailMessage(subject, message, from_email, to_email)
                            email.send(fail_silently=False)
                            logger.info("Email sent successfully to %s", request.user.email)
                        except Exception as e:
                            logger.error("Failed to send email: %s", str(e))

                return redirect('payment:success')
            else:
                messages.error(request, "Payment verification failed. Please try again.")
                return redirect('payment:failure')
        except Exception as e:
            logger.error("Error during payment verification: %s", str(e))
            messages.error(request, "An error occurred during payment verification.")
            return redirect('payment:failure')
    else:
        return HttpResponseBadRequest("Invalid request method")


