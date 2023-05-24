from django import forms
from django.core.exceptions import ValidationError

from trip.models import Place, Attraction, Travel, Days


class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["name", "country", "description"]
        labels = {'name': 'Nazwa', 'country': 'Kraj', 'description': 'Opis'}


class AddAttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = ["name", "description", "time"]
        labels = {'name': 'Nazwa', 'description': 'Opis', 'time': 'Oszacuj czas'}


class AddTravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['name', 'status']
        labels = {'name': 'Nazwa', 'status': 'Wybierz status'}


class AddDaysForm(forms.ModelForm):
    class Meta:
        model = Days
        fields = ['place_attraction', 'order']
        labels = {'order': 'Dzień numer:', 'place_attraction': 'Wybierz atrakcję'}
