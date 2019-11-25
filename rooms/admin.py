from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """  Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    """ Photo Inline Here """

    model = models.Photo


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """  Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="90px" height: 90px src={obj.file.url}/>')

    get_thumbnail.short_description = "Thumbnail"


# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        (
            "Accommodation Information",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        ("More Information", {"fields": ("amenities", "facilities", "house_rules")}),
        ("Last Detail", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "country",
        "city",
        "instant_book",
        "amenities",
        "facilities",
        "house_rules",
    )

    raw_id_fields = ("host",)

    search_fields = (
        "city",
        "^host__username",
    )  # host is a model 'Room' and inside, it has username.
    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

    def save_model(self, request, obj, form, change):
        print(obj.city)
        super().save_model(request, obj, form, change)

    count_amenities.short_description = "Count Amenities"
    count_photos.short_description = "Count Photos"
