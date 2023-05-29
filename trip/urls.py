from django.urls import path
from trip import views


urlpatterns = [
    path('get_place_by_country/', views.GetPlaceByCountryApi.as_view(), name='places_by_country_api'),
    path('get_attraction_by_place/', views.GetAttractionByPlaceApi.as_view(), name='attraction_by_place_api'),
    path('get_attraction_place/', views.GetAttractionPlace.as_view(), name='attraction_place_api'),
    path('get_countries/', views.GetCountryDistinctApi.as_view(), name='countries_api'),
    path('get_places/', views.GetPlacesApi.as_view(), name='places_api'),
    path('get_attractions/', views.GetAttractionsApi.as_view(), name='attractions_api'),

    path('places/', views.PlacesView.as_view(), name='places'),
    path('attraction/<int:pk>/', views.AttractionDetailView.as_view(), name='attractions'),
    path('add/place/', views.AddPlaceView.as_view(), name='add_place'),
    path('add/attraction/', views.AddAttractionView.as_view(), name='add_attraction'),
    path('add/travel/', views.AddTravelView.as_view(), name='add_travel'),
    path('add/travel/part2/<int:pk>/', views.AddTravelStepTwoView.as_view(), name='add_travel_part2'),
    path('travels/', views.TravelView.as_view(), name='travels'),
    path('travels/details/<int:pk>/', views.TravelDetailView.as_view(), name='travel_details'),
    path('travels/<int:pk>', views.TravelStatusSerializer.as_view(), name='travels_status'),
    path('day/<int:trip_pk>/<int:order>/', views.DayView.as_view(), name='day'),
    path('day/detail/<int:pk>/', views.DayDetailsView.as_view(), name='day_detail'),
    path('day/delete/<int:pk>/', views.DeleteDayView.as_view(), name='day_delete'),
    path('travel/delete/<int:pk>/', views.DeleteTravelView.as_view(), name='travel_delete'),
    path('day/delete/<int:trip_pk>/<int:order>', views.DaysDeleteView.as_view(), name='day_detail_delete'),
    path('add/note/<int:pk>', views.AddNote.as_view(), name='add_note'),
    path('delete/note/<int:pk>', views.DeleteNote.as_view(), name='delete_note'),
    path('edit/note/<int:pk>', views.EditNote.as_view(), name='edit_note'),

]
