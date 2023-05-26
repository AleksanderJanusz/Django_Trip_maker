from rest_framework import serializers

from trip.models import Travel, Place


class TravelSerializer(serializers.ModelSerializer):
    choice = serializers.SerializerMethodField()

    class Meta:
        model = Travel
        fields = ['name', 'status', 'user', 'choice']

    def get_choice(self, obj):
        # return obj.get_status_display()
        return obj.GENRE_CHOICES
