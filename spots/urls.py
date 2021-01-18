from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_grid, name='create_grid'),
    path('<int:grid_id>', views.retrieve_or_save_animation_order,
         name='retrieve_or_save_animation_order'),
]
