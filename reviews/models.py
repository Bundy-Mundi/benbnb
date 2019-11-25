from django.db import models
from cores import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    cleanliness = models.IntegerField()
    communication = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    location = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    rooms = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def rating_average(self):
        avg = (
            self.accuracy
            + self.cleanliness
            + self.communication
            + self.check_in
            + self.value
            + self.location
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Average"

    def __str__(self):
        return f"{self.review} - {self.rooms}"
