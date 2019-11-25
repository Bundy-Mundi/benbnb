from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    RoomType = models.RoomType.objects.all()
    Amenity = models.Amenity.objects.all()
    Facility = models.Facility.objects.all()

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    price = forms.IntegerField(initial=0)
    room_type = forms.ModelChoiceField(
        required= False,
        empty_label="Anykind",
        queryset=RoomType)
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    super_host = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(required=False, queryset=Amenity, widget=forms.CheckboxSelectMultiple)
    facilities = forms.ModelMultipleChoiceField(required=False, queryset=Facility, widget=forms.CheckboxSelectMultiple)