import calendar
from datetime import date
import datetime
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import dailyInformation, monthSummery, weekSummery


def singleTemplate(request, title, page, content):
    if not request.user.is_authenticated and page != "login.html":
        return HttpResponseRedirect("/login")

    variables = {"title": title, "page": page}
    variables.update(content)
    return render(request, "index.html", variables)


def indexPage(request):
    weekSummeryData = list(
        weekSummery.objects.filter(userName=request.user.username).values_list(
            "week", flat=True
        )
    )
    weekCost = list(
        weekSummery.objects.filter(userName=request.user.username).values_list(
            "totalCost", flat=True
        )
    )

    monthSummeryData = list(
        monthSummery.objects.filter(userName=request.user.username).values_list(
            "month", flat=True
        )
    )
    monthCost = list(
        monthSummery.objects.filter(userName=request.user.username).values_list(
            "totalCost", flat=True
        )
    )
    monthNames = [get_month_name(month_number) for month_number in monthSummeryData]

    thisMonthTotalCost = (
        monthSummery.objects.filter(
            month=date.today().month, userName=request.user.username
        )
        .values_list("totalCost", flat=True)
        .first()
    )
    thisWeekTotalCost = (
        weekSummery.objects.filter(
            week=get_iso_week_numbers(), userName=request.user.username
        )
        .values_list("totalCost", flat=True)
        .first()
    )

    todaysTotalCost = dailyInformation.get_total_cost_for_today(
        userName=request.user.username
    )

    yearData = {
        "labels": monthNames,
        "values": monthCost,
    }
    monthData = {
        "labels": weekSummeryData,
        "values": weekCost,
    }
    content = {
        "yearData": json.dumps(yearData),
        "monthData": json.dumps(monthData),
        "monthCost": thisMonthTotalCost,
        "weekCost": thisWeekTotalCost,
        "dayCost": todaysTotalCost,
    }
    return singleTemplate(request, "Home", "home.html", content)


def loginPage(request):
    content = {}
    return singleTemplate(request, "Login", "login.html", content)


def insertPage(request):
    content = {}
    return singleTemplate(request, "Insert", "Insert.html", content)


def user_login(request):
    content = {}
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser == True:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    messages.success(request, "Not Allowed to login.")
                    return HttpResponseRedirect("/login")
            else:
                messages.error(
                    request, "Password Not match. Re-enter password correctly."
                )
                return HttpResponseRedirect("/login")
        else:
            messages.error(request, "Invalid User.")
            return singleTemplate(request, "Login", "login.html", content)
    else:
        return HttpResponseRedirect("/")


def expenseAdd(request):
    type = request.POST["type"]
    cost = float(request.POST["cost"])
    storeInformation = dailyInformation.objects.create(
        type=type, cost=cost, userName=request.user.username
    )
    if monthSummery.objects.filter(
        month=storeInformation.dateAndTime.month,
        year=storeInformation.dateAndTime.year,
        userName=request.user.username,
    ).exists():
        monthSummeryData = monthSummery.objects.filter(
            month=storeInformation.dateAndTime.month,
            year=storeInformation.dateAndTime.year,
            userName=request.user.username,
        )
        newCost = monthSummeryData.get().totalCost + storeInformation.cost
        monthSummeryData.update(totalCost=newCost)
    else:
        monthSummery.objects.create(
            month=storeInformation.dateAndTime.month,
            year=storeInformation.dateAndTime.year,
            totalCost=storeInformation.cost,
            userName=request.user.username,
        )

    if weekSummery.objects.filter(
        week=get_iso_week_numbers(),
        month=storeInformation.dateAndTime.month,
        userName=request.user.username,
    ).exists():
        weekSummeryData = weekSummery.objects.filter(
            week=get_iso_week_numbers(),
            month=storeInformation.dateAndTime.month,
            userName=request.user.username,
        )
        weekUpdateCost = weekSummeryData.get().totalCost + storeInformation.cost
        weekSummeryData.update(totalCost=weekUpdateCost)
    else:
        weekSummery.objects.create(
            week=get_iso_week_numbers(),
            month=storeInformation.dateAndTime.month,
            totalCost=storeInformation.cost,
            userName=request.user.username,
        )
    return HttpResponseRedirect("/")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login")


def get_month_name(month_number):
    return calendar.month_name[month_number]


def get_iso_week_numbers():
    date_obj = datetime.date.today()
    iso_week_number = date_obj.isocalendar()[1]
    first_day_of_month = datetime.date(date_obj.year, date_obj.month, 1)
    first_week_number = first_day_of_month.isocalendar()[1]
    week_number_in_month = iso_week_number - first_week_number + 1

    return week_number_in_month
