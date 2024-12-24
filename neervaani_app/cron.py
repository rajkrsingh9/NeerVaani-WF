from django_cron import CronJobBase, Schedule
from .models import OTP
from datetime import datetime, timedelta

class CleanOTPTable(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Runs daily at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'neervaani_app.clean_otp_table'  # Unique code for this cron job

    def do(self):
        cutoff_date = datetime.now() - timedelta(weeks=1)
        OTP.objects.filter(created_at__lte=cutoff_date).delete()
