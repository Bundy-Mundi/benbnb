from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Here """

    list_display = ("__str__", "created")


@admin.register(models.Conversation)
class ConverstaionAdmin(admin.ModelAdmin):

    list_display = ("__str__",)
    filter_horizontal = ("participants",)

