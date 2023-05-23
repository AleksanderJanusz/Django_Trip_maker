from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from trip.forms import AddPlaceForm, AddAttractionForm
from trip.models import Place, Attraction, Cost, PlaceAttraction


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


class AddAttractionView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddAttractionForm()
        return render(request, 'trip/attraction_form.html', {'form': form,
                                                             'places': Place.objects.all()})

    def post(self, request):
        form = AddAttractionForm(request.POST)
        check = request.POST.get('checkbox')
        place = int(request.POST.get('place'))
        try:
            cost_from = int(request.POST.get('from'))
            cost_to = int(request.POST.get('to'))
            persons = int(request.POST.get('persons'))
        except ValueError:
            return render(request, 'trip/attraction_form.html', {'form': form,
                                                                 'places': Place.objects.all(),
                                                                 'error': 'error'})

        if cost_to < 0 or cost_from < 0 or persons < 0:
            return render(request, 'trip/attraction_form.html', {'form': form,
                                                                 'places': Place.objects.all(),
                                                                 'error': 'error'})
        if form.is_valid():
            attraction = form.save()
            if check:
                Cost.objects.create(persons=persons, cost=cost_from, attraction_id=attraction.id)
                Cost.objects.create(persons=persons, cost=cost_to, attraction_id=attraction.id)
            else:
                Cost.objects.create(persons=persons, cost=cost_from, attraction_id=attraction.id)
            PlaceAttraction.objects.create(attraction_id=attraction.id, place_id=place)
            return redirect('index')
        return render(request, 'trip/attraction_form.html', {'form': form,
                                                             'places': Place.objects.all()})
