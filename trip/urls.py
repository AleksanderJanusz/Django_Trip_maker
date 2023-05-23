from django.urls import path
from trip import views

urlpatterns = [
    path('places/', views.PlacesView.as_view(), name='places'),
    path('attraction/<int:pk>/', views.AttractionDetailView.as_view(), name='attractions'),
    path('get_place_by_country/', views.GetPlaceByCountryApi.as_view(), name='places_by_country_api'),
    path('get_attraction_by_place/', views.GetAttractionByPlaceApi.as_view(), name='attraction_by_place_api'),
    path('add/place/', views.AddPlaceView.as_view(), name='add_place'),
]
