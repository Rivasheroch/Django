#myapp/urls.py

from django.urls import path
from . import views
from .views import upload_csv

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('descriptive-statistics/', views.descriptive_statistics, name='descriptive_statistics'),
    path('correlation-heatmap/', views.correlation_heatmap, name='correlation_heatmap'),
    path('predictive-model-metrics/', views.predictive_model_metrics, name='predictive_model_metrics'),
    path('predictive-models/', views.predictive_models, name='predictive_models'),
    path('predictive-models/education/', views.education_energy_prediction, name='education_energy_prediction'),
    path('predictive-models/food-services/', views.food_services_energy_prediction, name='food_services_energy_prediction'),
    path('predictive-models/healthcare/', views.healthcare_energy_prediction, name='healthcare_energy_prediction'),
    path('predictive-models/lodging/', views.lodging_energy_prediction, name='lodging_energy_prediction'),
    path('predictive-models/mercantile/', views.mercantile_energy_prediction, name='mercantile_energy_prediction'),
    path('predictive-models/mobile-home/', views.mobile_home_energy_prediction, name='mobile_home_energy_prediction'),
    path('predictive-models/multifamily-2-4/', views.multifamily_2_4_energy_prediction, name='multifamily_2_4_energy_prediction'),
    path('predictive-models/multifamily-5plus/', views.multifamily_5plus_energy_prediction, name='multifamily_5plus_energy_prediction'),
    path('predictive-models/office/', views.office_energy_prediction, name='office_energy_prediction'),
    path('predictive-models/single-family-attached/', views.single_family_attached_energy_prediction, name='single_family_attached_energy_prediction'),
    path('predictive-models/single-family-detached/', views.single_family_detached_energy_prediction, name='single_family_detached_energy_prediction'),
    path('predictive-models/warehouse/', views.warehouse_energy_prediction, name='warehouse_energy_prediction'),
    path('upload/', upload_csv, name='upload_csv'),
]
