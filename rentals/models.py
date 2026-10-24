from django.db import models


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('SUV', 'SUV'),
        ('Van', 'Van'),
    ]

    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPES
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    registration_number = models.CharField(
        max_length=20,
        unique=True
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='vehicles/',
        blank=True,
        null=True
    )
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model}"
    
class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    customer = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    # Customer contact details
    customer_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    customer_email = models.EmailField(
        blank=True,
        default=""
    )

    customer_phone = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    customer_address = models.TextField(
        blank=True,
        default=""
    )

    start_date = models.DateField()
    end_date = models.DateField()

    number_of_days = models.PositiveIntegerField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.customer.username} - "
            f"{self.vehicle.name}"
        )