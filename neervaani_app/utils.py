import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import OTP

def generate_otp(email):
    otp_code = str(random.randint(100000, 999999))
    expires_at = timezone.now() + timedelta(minutes=10)  # OTP valid for 10 minutes
    OTP.objects.create(email=email, otp_code=otp_code, expires_at=expires_at)
    
    # Send OTP via email
    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP code is {otp_code}. It is valid for 10 minutes.",
        from_email="info.vidyavista@gmail.com",
        recipient_list=[email],
    )
