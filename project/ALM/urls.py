from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Analytics/', views.analytics, name='analytics'),
    path('Tech_Analytics/', views.Tech_Analytics, name='Tech_Analytics'),
    path('Machine_Learning/', views.Machine_Learning, name='Machine_Learning'),
    path('Modelling/', views.Modelling, name='Modelling'),
    path('Time_Series/', views.Time_Series, name='Time_Series'),
    path('Statistical_Analysis/', views.Statistical_Analysis, name='Statistical_Analysis'),
    path('Portfolio/', views.Portfolio, name='Portfolio'),
    path('Special_Events/', views.Special_Events, name='Special_Events'),
    path('Unstructured_data/', views.Unstructured_data, name='Unstructured_data'),
]