import json

import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.inventory.helpers import generate_invoice_pdf, send_email_notification
from apps.inventory.models.salesorder import Cart, CartItem, Invoice, Order, OrderItem, Payment


@csrf_exempt
def razorpay_webhook(request):
    """Razorpay webhook"""

    if request.method == "POST":
        try:
            payload = request.body.decode("utf-8")
            signature = request.headers.get("X-Razorpay-Signature")
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            client.utility.verify_webhook_signature(payload, signature, settings.RAZORPAY_WEBHOOK_SECRET)
            event = json.loads(payload)
            if event["event"] == "payment.captured":
                payment_entity = event["payload"]["payment"]["entity"]
                notes = payment_entity.get("notes", {})
                order_id = int(notes.get("order_id"))
                user_id = int(notes.get("user_id"))
                order = Order.objects.get(pk=order_id)
                order.payment_status = "SUCCESS"
                order.save()
                Payment.objects.create(
                    order=order,
                    payment_id=payment_entity["id"],
                    status="SUCCESS",
                    amount=payment_entity["amount"] / 100,
                )

                cart = Cart.objects.get(user_id=user_id, is_active=True)
                cart_items = CartItem.objects.filter(cart=cart)
                pdf_path = generate_invoice_pdf(order, cart_items)
                Invoice.objects.create(order=order, pdf_path=pdf_path)
                send_email_notification(order.user.email, pdf_path)

                order_items = []
                for cart_item in cart_items:
                    order_item = OrderItem.objects.create(
                        user_id=user_id,
                        product=cart_item.product,
                    )
                order_items.append(order_item)
            return JsonResponse({"status": "success"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Signature verification failed"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
