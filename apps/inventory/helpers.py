import os

from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_invoice_pdf(order):
    """To generate invoice"""

    pdf_path = f"invoices/order_{order.id}.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)  # Ensure directory exists
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Invoice")
    c.drawString(100, 735, f"Order ID: {order.id}")
    c.drawString(100, 720, f"Customer: {order.user.username}")
    c.drawString(100, 705, f"Total Price: ${order.total_price:.2f}")
    c.drawString(100, 690, f"Payment Status: {order.payment_status}")
    c.drawString(100, 100, "Thank you for your purchase!")
    c.save()
    return pdf_path


def send_email_notification(email, pdf_path):
    """Send a Email notification"""

    subject = "Your Order Invoice"
    message = "Thank you for your order. Please find the attached invoice."
    from_email = "your_email@example.com"
    email_message = EmailMessage(subject, message, from_email, [email])
    email_message.attach_file(pdf_path)
    email_message.send()
