from django.contrib import admin

from .models import Vehicle, Booking


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "brand",
        "model",
        "vehicle_type",
        "registration_number",
        "price_per_day",
        "availability_status",
    )

    list_filter = (
        "vehicle_type",
        "available",
    )

    search_fields = (
        "name",
        "brand",
        "model",
        "registration_number",
    )

    list_editable = (
        "price_per_day",
    )

    ordering = (
        "brand",
        "model",
    )

    def availability_status(self, obj):

        if obj.available:
            return "Available"

        return "Unavailable"

    availability_status.short_description = "Status"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "vehicle",
        "start_date",
        "end_date",
        "number_of_days",
        "total_amount",
        "status",
        "booking_date",
    )

    list_filter = (
        "status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "customer__username",
        "vehicle__name",
        "vehicle__brand",
        "vehicle__model",
        "vehicle__registration_number",
    )

    ordering = (
        "-booking_date",
    )

    readonly_fields = (
        "booking_date",
        "number_of_days",
        "total_amount",
    )


admin.site.site_header = "DriveRent Administration"
admin.site.site_title = "DriveRent Admin"
admin.site.index_title = "Vehicle Rental Management"