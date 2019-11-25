from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from cores import models as core_models


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """ Room Type Model """

    class Meta:
        verbose_name_plural = "Room Types"


class Amenity(AbstractItem):
    """ Amenity Type Model """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Type Model """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ House Rule Type Model """

    class Meta:
        verbose_name_plural = "House Rules"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    name = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    caption = models.CharField(max_length=140, blank=True)
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(core_models.TimeStampedModel):

    """ Room Model """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_rating = 0
        for review in all_reviews:
            all_rating += review.rating_average()
        if all_reviews:
            all_rating = all_rating / len(all_reviews)
        else:
            all_rating = 0
        return round(all_rating, 2)

    def first_photo(self):
        first_photo = self.photos.all()[0]
        first_photo = first_photo.file.url
        return first_photo
