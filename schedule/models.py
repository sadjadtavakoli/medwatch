from datetime import time

from django.db import models


class DoctorSchedule(models.Model):
    doctor = models.OneToOneField('member.DoctorMember', null=False)
    session_interval = models.PositiveIntegerField(default=30)

    def __init__(self, *args, **kwargs):
        super(DoctorSchedule, self).__init__(*args, **kwargs)
        self.weekly_schedule_cache = None

    def get_weekly_schedule(self):
        if self.weekly_schedule_cache is None:
            self.weekly_schedule_cache = self.dailyschedule_set.order_by('day_of_week')
        return self.weekly_schedule_cache

    def get_session_interval(self):
        return self.session_interval

    @staticmethod
    def get_by_doctor(doctor):
        doctor_schedule, created = DoctorSchedule.objects.get_or_create(doctor=doctor)

        if created:
            for day in range(7):
                DailySchedule.objects.create(day_of_week=day, doctor_schedule=doctor_schedule)

        return doctor_schedule


class DailySchedule(models.Model):
    day_of_week = models.SmallIntegerField()
    doctor_schedule = models.ForeignKey(DoctorSchedule, null=False)
    start_time = models.TimeField(default=time(hour=9))
    end_time = models.TimeField(default=time(hour=17))


class AppointmentRequest(models.Model):
    patient = models.ForeignKey('member.Member', null=False)
    doctor = models.ForeignKey('member.DoctorMember', null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
