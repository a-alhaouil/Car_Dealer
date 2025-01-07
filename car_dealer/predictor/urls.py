from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('car-list/', views.car_list, name='car_list'),

    path('category-cars/', views.category_cars, name='category_cars'),

]
