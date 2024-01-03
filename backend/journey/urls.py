from django.urls import path

from . import api

urlpatterns = [
    path('', api.journey_feed_list, name='journey_feed_list'),
    path('create/', api.journey_create, name='journey_create'),
    path('profile/<uuid:id>/', api.journey_list_profile, name='journey_list_profile'),
    path('<uuid:pk>/', api.journey_view, name='journey_view'),
    path('<uuid:pk>/edit/', api.journey_edit, name='journey_edit'),
    path('<uuid:pk>/delete/', api.journey_delete, name='journey_delete'),
    path('<uuid:pk>/report/', api.journey_report, name='journey_report'),
]