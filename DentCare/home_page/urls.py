from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("about", views.about, name="about"),
    path("treatment", views.treatment, name="treatment"),
    path("appointment", views.appointment, name="appointment"),
    path("contact", views.contact, name="contact"),
    path("appointment/login/", views.appointment_login, name="appointment_login"),
    path("appointment/register", views.appointment_register, name="appointment_register"),
     path('appointment/book', views.book_appointment, name='book_appointment'),
    path("appointment/Dr", views.appointment_admin, name="appointment_admin"),
    path("appointment/Dr/dashboard", views.dr_dashboard, name="dr_dashboard"),
    path('submit_report/<int:appointment_id>/', views.submit_report, name='submit_report'),
    path('my-appointments/', views.view_my_appointments, name='view_my_appointments'),
    path('appointments/filter/', views.filter_appointments, name='filter_appointments'),
    path('fetch_slots/', views.fetch_slots, name='fetch_slots'),

]
