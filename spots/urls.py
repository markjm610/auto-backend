from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_grid, name='create_grid'),
    path('<int:grid_id>', views.retrieve_or_update_animation_order,
         name='retrieve_or_update_animation_order'),
    path('squares/<int:square_id>',
         views.update_square, name='update_square'),
]
