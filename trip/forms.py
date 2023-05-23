from django import forms

from trip.models import Place


class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["name", "country", "description"]
        labels = {'name': 'Nazwa', 'country': 'Kraj', 'description': 'Opis'}
