import generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView
from rest_framework import generics
from trip.forms import AddPlaceForm, AddAttractionForm, AddTravelForm, AddDaysForm, AddNoteForm
from trip.models import Place, Attraction, Cost, PlaceAttraction, Travel, Days, TravelNotes
from trip.serializers import TravelSerializer


# --------------------API---------------------
class GetAttractionsApi(View):
    def get(self, request):
        attractions = [{'name': attraction.name,
                        'description': attraction.description,
                        'id': attraction.id}
                       for attraction in Attraction.objects.all()]
        return JsonResponse(attractions, safe=False)


class GetPlacesApi(View):
    def get(self, request):
        places = Place.objects.all()
        places = [{'name': place.name, 'id': place.id} for place in places]
        return JsonResponse(places, safe=False)


class GetCountryDistinctApi(View):
    def get(self, request):
        places = Place.objects.all().order_by('country').distinct('country')
        countries = [{'country': place.country, 'id': place.id} for place in places]
        return JsonResponse(countries, safe=False)


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


class GetAttractionPlace(View):
    def get(self, request):
        place_id = int(request.GET.get('place_api'))
        place = PlaceAttraction.objects.filter(place_id=place_id)
        attractions = [{'id': attraction.id} for attraction in place]
        return JsonResponse(attractions, safe=False)


# ---------------------------Django----------------------------
class IndexView(View):
    def get(self, request):
        return render(request, 'trip/index.html')


class PlacesView(View):
    def get(self, request):
        places = Place.objects.all().order_by('country').distinct('country')
        return render(request, 'trip/places.html', {'places': places})


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
            return redirect('add_attraction')
        return render(request, 'trip/attraction_form.html', {'form': form,
                                                             'places': Place.objects.all()})


# HERE WE START ADD TRIP VIEWS

class AddTravelView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddTravelForm()
        return render(request, 'trip/add_travel.html', {'form': form})

    def post(self, request):
        form = AddTravelForm(request.POST)
        if form.is_valid():
            travel = form.save(commit=False)
            travel.user = request.user
            travel.save()
            url = reverse_lazy('add_travel_part2', kwargs={'pk': travel.id})
            return redirect(url)
        return render(request, 'trip/add_travel.html', {'form': form})


class AddTravelStepTwoView(LoginRequiredMixin, View):
    def get(self, request, pk):
        days = Days.objects.filter(travel_id=pk)
        orders = days.distinct('order')
        trip = Travel.objects.get(pk=pk)
        form = AddDaysForm()
        places = Place.objects.all().order_by('country').distinct('country')
        return render(request, 'trip/add_travel_part2.html', {'form': form, 'trip': trip, 'places': places,
                                                              'days': days, 'orders': orders})

    def post(self, request, pk):
        days = Days.objects.filter(travel_id=pk)
        orders = days.distinct('order')
        trip = Travel.objects.get(pk=pk)
        form = AddDaysForm(request.POST)
        places = Place.objects.all().order_by('country').distinct('country')
        if form.is_valid():
            day = form.save(commit=False)
            day.travel_id = pk
            day.save()
            url = reverse_lazy('add_travel_part2', kwargs={'pk': pk})
            return redirect(url)
        return render(request, 'trip/add_travel_part2.html', {'form': form, 'trip': trip, 'places': places,
                                                              'days': days, 'orders': orders})


class TravelView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'trip/travels.html',
                      {'travels': Travel.objects.filter(user_id=request.user.id).order_by('name')})


class TravelDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        notes = TravelNotes.objects.filter(trip_id=pk)
        days = Days.objects.filter(travel_id=pk)
        orders = days.distinct('order')
        trip = Travel.objects.get(pk=pk)
        return render(request, 'trip/travel_details.html',
                      {'trip': trip, 'days': days, 'orders': orders, 'notes': notes})

    def post(self, request, pk):
        notes = TravelNotes.objects.filter(trip_id=pk)
        days = Days.objects.filter(travel_id=pk)
        orders = days.distinct('order')
        trip = Travel.objects.get(pk=pk)
        return render(request, 'trip/travel_details_delete.html',
                      {'trip': trip, 'days': days, 'orders': orders, 'notes': notes})


class DayView(LoginRequiredMixin, View):
    def get(self, request, trip_pk, order):
        days = Days.objects.filter(travel_id=trip_pk).filter(order=order)
        return render(request, 'trip/day.html', {'days': days})


class DayDetailsView(LoginRequiredMixin, UpdateView):
    model = Days
    fields = '__all__'
    template_name = 'trip/day_details.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        day = Days.objects.get(pk=pk)
        return reverse_lazy('day', kwargs={'trip_pk': day.travel_id, 'order': day.order})


class DeleteDayView(UserPassesTestMixin, View):
    def test_func(self):
        day = Days.objects.get(pk=self.kwargs['pk'])
        return day.travel.user == self.request.user

    def get(self, request, pk):
        day = Days.objects.get(pk=pk)
        order = day.order
        trip_pk = day.travel_id
        day.delete()
        return redirect('day_detail_delete', order=order, trip_pk=trip_pk)


class DaysDeleteView(LoginRequiredMixin, View):
    def get(self, request, trip_pk, order):
        days = Days.objects.filter(travel_id=trip_pk).filter(order=order)
        return render(request, 'trip/day_delete.html', {'days': days})


class DeleteTravelView(UserPassesTestMixin, View):
    def test_func(self):
        travel = Travel.objects.get(pk=self.kwargs['pk'])
        return travel.user == self.request.user

    def get(self, request, pk):
        travel = Travel.objects.get(pk=pk)
        travel.delete()
        return redirect('travels')


class AddNote(LoginRequiredMixin, CreateView):
    model = TravelNotes
    fields = ['note']
    template_name = 'trip/add_note.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['note'].label = 'Notatka'
        return form

    def form_valid(self, form):
        pk = self.kwargs['pk']
        note = form.save(commit=False)
        note.status = Travel.objects.get(pk=pk).status
        note.trip_id = pk
        note.save()
        return redirect('travel_details', pk=pk)


class DeleteNote(UserPassesTestMixin, View):
    def test_func(self):
        pk = TravelNotes.objects.get(pk=self.kwargs['pk']).trip_id
        travel = Travel.objects.get(pk=pk)
        return travel.user == self.request.user

    def get(self, request, pk):
        note = TravelNotes.objects.get(pk=pk)
        travel_id = note.trip_id
        note.delete()
        return redirect('travel_details', pk=travel_id)


class EditNote(UserPassesTestMixin, UpdateView):
    def test_func(self):
        pk = TravelNotes.objects.get(pk=self.kwargs['pk']).trip_id
        travel = Travel.objects.get(pk=pk)
        return travel.user == self.request.user

    model = TravelNotes
    fields = ['note', 'status']
    template_name = 'trip/add_note.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        trip_id = TravelNotes.objects.get(pk=pk).trip_id
        note = form.save(commit=False)
        note.trip_id = trip_id
        if not note.note.endswith('(edytowany)'):
            note.note += ' (edytowany)'
        note.save()
        return redirect('travel_details', pk=trip_id)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['note'].label = 'Notatka'
        return form

    def get_form_kwargs(self):
        note = super().get_form_kwargs()
        if note['instance'].note.endswith('(edytowany)'):
            note['instance'].note = note['instance'].note[:-12]
        return note


# -------------SERIALIZER---------------

class TravelStatusSerializer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
