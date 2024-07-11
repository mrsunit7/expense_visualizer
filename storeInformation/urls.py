
from django.contrib import admin
from django.urls import path
from cost_calculator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexPage),
    path('login/', views.loginPage),
    path('insert/', views.insertPage),
    path('user_login/', views.user_login),
    path('expenseAdd/', views.expenseAdd),
    path('logout/', views.logout_user),
]
