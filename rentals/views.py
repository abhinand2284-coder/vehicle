from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.contrib.auth import login, logout

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


from .models import Vehicle, Booking
def home(request):

    return render(
        request,
        "rentals/home.html"
    )


def vehicle_list(request):

    vehicles = Vehicle.objects.filter(
        available=True
    )

    return render(
        request,
        "rentals/vehicle_list.html",
        {
            "vehicles": vehicles
        }
    )


def vehicle_detail(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    return render(
        request,
        "rentals/vehicle_detail.html",
        {
            "vehicle": vehicle
        }
    )


def register(request):

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(
        request,
        "rentals/register.html",
        {
            "form": form
        }
    )


def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "rentals/login.html",
        {
            "form": form
        }
    )

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(
        request,
        "rentals/register.html",
        {
            "form": form
        }
    )
@login_required
def book_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        available=True
    )

    if request.method == "POST":

        start_date = request.POST.get(
            "start_date"
        )

        end_date = request.POST.get(
            "end_date"
        )

        if not start_date or not end_date:

            messages.error(
                request,
                "Please select both dates."
            )

            return redirect(
                "book_vehicle",
                vehicle_id=vehicle.id
            )

        start_date = date.fromisoformat(
            start_date
        )

        end_date = date.fromisoformat(
            end_date
        )

        if start_date < date.today():

            messages.error(
                request,
                "Start date cannot be in the past."
            )

            return redirect(
                "book_vehicle",
                vehicle_id=vehicle.id
            )

        if end_date <= start_date:

            messages.error(
                request,
                "End date must be after the start date."
            )

            return redirect(
                "book_vehicle",
                vehicle_id=vehicle.id
            )

        number_of_days = (
            end_date - start_date
        ).days

        total_amount = (
            number_of_days *
            vehicle.price_per_day
        )

        overlapping_booking = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=[
                "Pending",
                "Approved"
            ]
        ).exists()

        if overlapping_booking:

            messages.error(
                request,
                "This vehicle is already booked for the selected dates."
            )

            return redirect(
                "book_vehicle",
                vehicle_id=vehicle.id
            )

        Booking.objects.create(

            customer=request.user,

            vehicle=vehicle,

            start_date=start_date,

            end_date=end_date,

            number_of_days=number_of_days,

            total_amount=total_amount,

            status="Pending"
        )

        messages.success(
            request,
            "Your booking has been submitted successfully."
        )

        return redirect(
            "home"
        )

    return render(
        request,
        "rentals/book_vehicle.html",
        {
            "vehicle": vehicle
        }
    )


def user_logout(request):

    logout(request)

    return redirect("home")

@staff_member_required
def admin_dashboard(request):

    total_vehicles = Vehicle.objects.count()

    available_vehicles = Vehicle.objects.filter(
        available=True
    ).count()

    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    total_bookings = Booking.objects.count()

    pending_bookings = Booking.objects.filter(
        status="Pending"
    ).count()

    recent_bookings = Booking.objects.select_related(
        "customer",
        "vehicle"
    ).order_by(
        "-booking_date"
    )[:5]

    context = {
        "total_vehicles": total_vehicles,
        "available_vehicles": available_vehicles,
        "total_customers": total_customers,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "recent_bookings": recent_bookings,
    }

    return render(
        request,
        "rentals/admin_dashboard.html",
        context
    )
@staff_member_required
def update_booking_status(request, booking_id, status):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == "POST":

        if status in ["Approved", "Rejected"]:

            booking.status = status

            booking.save()

        return redirect("admin_dashboard")

    return redirect("admin_dashboard")
@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related(
        "vehicle"
    ).order_by(
        "-booking_date"
    )

    return render(
        request,
        "rentals/my_bookings.html",
        {
            "bookings": bookings
        }
    )