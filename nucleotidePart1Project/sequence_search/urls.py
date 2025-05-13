from django.urls import path
from . import views
from .views import pattern_search_api

urlpatterns = [
    path('', views.search_pattern, name='search'),
    path('api/v1/search', pattern_search_api, name='api-search'),
]
