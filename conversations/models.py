from django.db import models
from cores import models as core_models


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):

        participants = self.participants.all()
        username = []

        if len(participants) == 3:
            for n in range(3):
                username.append(participants[n].username)
            return ", ".join(username)
        elif len(participants) == 2:
            for n in range(2):
                username.append(participants[n].username)
            return ", ".join(username)
        elif len(participants) == 1:
            for n in range(1):
                username.append(participants[n].username)
            return ", ".join(username)
        elif len(participants) > 3:
            for n in range(len(participants)-1):
                username.append(participants[n].username)
            username = (
                ", ".join(username) + f", {str(len(participants)-3)} more people."
            )
            return username
        else:
            return "No User"

    def username(self):
        return self.participants.name


class Message(core_models.TimeStampedModel):

    creator = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    message = models.TextField()
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):

        return f"{self.creator} says: {self.message}"
