import os

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_invoice_pdf(order, cart_items):
    """To generate invoice as a PDF using an HTML template"""

    pdf_path = f"invoices/order_{order.id}.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    context = {
        "order": order,
        "cart_items": cart_items,
    }
    html_string = render_to_string("invoice_template.html", context)

    HTML(string=html_string).write_pdf(pdf_path)
    return pdf_path


def send_email_notification(email, pdf_path):
    """Send a Email notification"""

    subject = "Your Order Invoice"
    message = "Thank you for your order. Please find the attached invoice."
    from_email = "your_email@example.com"
    email_message = EmailMessage(subject, message, from_email, [email])
    email_message.attach_file(pdf_path)
    email_message.send()
