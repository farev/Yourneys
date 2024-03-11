from django.urls import path

from . import api


urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<uuid:user_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
    path('<uuid:journey_pk>/create/', api.journey_conversation_create, name='journey_conversation_create'),
    path('<uuid:journey_pk>/add/', api.journey_conversation_add, name='journey_conversation_add'),
    path('<uuid:pk>/read/', api.readMessage, name='readMessage'),
    path('check/', api.checkMessages, name='checkMessages')
]