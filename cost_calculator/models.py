from django.db import models
from django.utils import timezone


class dailyInformation(models.Model):
    dateAndTime = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField()
    type = models.CharField(max_length=50)
    userName = models.CharField(max_length=50)

    @classmethod
    def get_total_cost_for_today(cls, userName):
        today = timezone.localdate()
        total_cost_today = (
            cls.objects.filter(dateAndTime__date=today, userName=userName).aggregate(
                total_cost=models.Sum("cost")
            )["total_cost"]
            or 0.0
        )
        return total_cost_today

    def __str__(self):
        local_time = timezone.localtime(self.dateAndTime) + timezone.timedelta(
            hours=5, minutes=30
        )
        return f"{local_time.strftime('%B %d, %Y, %I:%M %p')} - {self.cost} - {self.type} - {self.userName}"


class monthSummery(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    totalCost = models.FloatField()
    userName = models.CharField(max_length=50)


class weekSummery(models.Model):
    week = models.IntegerField()
    month = models.IntegerField()
    totalCost = models.FloatField()
    userName = models.CharField(max_length=50)
