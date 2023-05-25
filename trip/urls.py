from django.urls import path
from trip import views

urlpatterns = [
    path('places/', views.PlacesView.as_view(), name='places'),
    path('attraction/<int:pk>/', views.AttractionDetailView.as_view(), name='attractions'),
    path('get_place_by_country/', views.GetPlaceByCountryApi.as_view(), name='places_by_country_api'),
    path('get_attraction_by_place/', views.GetAttractionByPlaceApi.as_view(), name='attraction_by_place_api'),
    path('get_attraction_place/', views.GetAttractionPlace.as_view(), name='attraction_place_api'),
    path('add/place/', views.AddPlaceView.as_view(), name='add_place'),
    path('add/attraction/', views.AddAttractionView.as_view(), name='add_attraction'),
    path('add/travel/', views.AddTravelView.as_view(), name='add_travel'),
    path('add/travel/part2/<int:pk>/', views.AddTravelStepTwoView.as_view(), name='add_travel_part2'),
    path('travels/', views.TravelView.as_view(), name='travels'),
    path('travels/details/<int:pk>/', views.TravelDetailView.as_view(), name='travel_details'),
    path('travels/<int:pk>', views.TravelStatusSerializer.as_view(), name='travels_status'),
    path('day/<int:trip_pk>/<int:order>/', views.DayView.as_view(), name='day'),
    path('day/detail/<int:pk>/', views.DayDetailsView.as_view(), name='day_detail'),

]
