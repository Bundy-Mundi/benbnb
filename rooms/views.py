from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from . import models as room_models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = room_models.Room
    paginate_by = 12
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except room_models.Room.DoesNotExist:
        raise Http404()


class SearchView(View):
    """ Search View Definition """

    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city", "Anywhere")
                city = str.capitalize(city)
                country = form.cleaned_data.get("country", "KR")
                price = form.cleaned_data.get("price", 0)
                room_type = form.cleaned_data.get("room_type", 0)
                price = form.cleaned_data.get("price", 0)
                guests = form.cleaned_data.get("guests", 0)
                bedrooms = form.cleaned_data.get("bedrooms", 0)
                beds = form.cleaned_data.get("beds", 0)
                baths = form.cleaned_data.get("baths", 0)
                instant_book = form.cleaned_data.get("instant_book", False)
                super_host = form.cleaned_data.get("super_host", False)
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if super_host is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = room_models.Room.objects.filter(**filter_args)

                paginator = Paginator(qs, 10)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:
            form = forms.SearchForm()
            return render(request, "rooms/search.html", {"form": form})
