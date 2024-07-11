from django.contrib import admin
from django.utils import timezone

from .models import dailyInformation, monthSummery, weekSummery 


# @admin.register(dailyInformation)
# class dailyInformationAdmin(admin.ModelAdmin):
#     list_display = ("dateAndTime", "cost", "type")

class dailyInformationAdmin(admin.ModelAdmin):
    list_display = ("adjusted_date_and_time", "cost", "type","userName")

    def adjusted_date_and_time(self, obj):
        # Adjust dateAndTime to UTC+5:30 (IST)
        local_time = timezone.localtime(obj.dateAndTime) + timezone.timedelta(hours=5, minutes=30)
        return local_time.strftime('%B %d, %Y, %I:%M %p')

    adjusted_date_and_time.short_description = 'Date and Time (IST)'

admin.site.register(dailyInformation, dailyInformationAdmin)

@admin.register(monthSummery)
class monthSummeryAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "totalCost", "userName")

@admin.register(weekSummery)
class weekSummeryAdmin(admin.ModelAdmin):
    list_display = ("week", "month", "totalCost", "userName")