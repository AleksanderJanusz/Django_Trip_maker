from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from trip.forms import AddPlaceForm
from trip.models import Place, Attraction


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'trip/index.html')


class PlacesView(View):
    def get(self, request):
        places = Place.objects.all().order_by('country').distinct('country')
        return render(request, 'trip/places.html', {'places': places})


class GetPlaceByCountryApi(View):

    def get(self, request):
        country_id = int(request.GET.get('place_country_api'))
        country = Place.objects.get(pk=country_id)
        places = Place.objects.filter(country=country.country)
        places = [{'name': place.name, 'id': place.id} for place in places]
        return JsonResponse(places, safe=False)


class GetAttractionByPlaceApi(View):
    def get(self, request):
        place_id = int(request.GET.get('place_api'))
        place = Place.objects.get(pk=place_id)
        attractions = [{'name': attraction.name,
                        'description': attraction.description,
                        'id': attraction.id}
                       for attraction in place.attraction.all()]
        return JsonResponse(attractions, safe=False)


class AttractionDetailView(View):
    def get(self, request, pk):
        attraction = Attraction.objects.get(pk=pk)
        return render(request, 'trip/attraction_details.html', {'attraction': attraction})


class AddPlaceView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPlaceForm()
        return render(request, 'trip/place_form.html', {'form': form})

    def post(self, request):
        form = AddPlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.country = form.cleaned_data['country'].capitalize()
            place.name = form.cleaned_data['name'].capitalize()
            place.save()
            return redirect('index')
        return render(request, 'trip/place_form.html', {'form': form})
