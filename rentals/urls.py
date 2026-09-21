from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("vehicles/", views.vehicle_list, name="vehicle_list"),

    path(
        "vehicles/<int:vehicle_id>/",
        views.vehicle_detail,
        name="vehicle_detail"
    ),
    path(
    "register/",
    views.register,
    name="register"
    ),
    path(
    "login/",
    views.user_login,
    name="login"
    ),

    path(
    "logout/",
    views.user_logout,
    name="logout"
    ),

    path(
    "register/",
    views.register,
    name="register"
    ),
    path(
    "vehicles/<int:vehicle_id>/book/",
    views.book_vehicle,
    name="book_vehicle"
    ),
    path(
    "dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
    ),
    path(
    "dashboard/booking/<int:booking_id>/<str:status>/",
    views.update_booking_status,
    name="update_booking_status"
    ),
    path(
    "my-bookings/",
    views.my_bookings,
    name="my_bookings"
    ),
]
