# main/email_utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_booking_email(user_email, movie_name, booking_details):
    subject = f"Booking Confirmation for {movie_name}"
    message = f"""
    Dear Customer,

    Thank you for booking tickets with us. Here are your booking details:

    {booking_details}

    Enjoy your movie!

    Best regards,
    BoxOffice Team
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
