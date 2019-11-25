from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rooms.models import Room
from . import models


class RoomInline(admin.TabularInline):
    model = Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):  # Defined by user
    """ Custom User Admin """

    inlines = (RoomInline,)
    # If don't bind those two fieldsets, one will wholey replace the other.
    fieldsets = UserAdmin.fieldsets + (
        (
            "In Detail",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "date_of_birth",
                    "language",
                    "currency",
                    "superhost",
                    "auth",
                )
            },
        ),
    )
    list_filter = UserAdmin.list_filter + ("superhost",)
    list_display = UserAdmin.list_display + (
        "currency",
        "language",
        "superhost",
        "is_active",
        "email_verified",
        "email_secret",
        "auth",
    )

