from django import forms
from django.core.exceptions import ValidationError

from trip.models import Place, Attraction


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
