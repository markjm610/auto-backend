from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_grid, name='create_grid'),
    path('<int:grid_id>', views.retrieve_or_update_grid,
         name='retrieve_or_update_grid'),
    path('squares/<int:square_id>',
         views.update_square, name='update_square'),
]
