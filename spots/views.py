from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .models import Grid, Square

# Create your views here.


@api_view(['POST'])
def create_grid(request):

    if request.method == 'POST':
        # Make new grid
        grid = Grid()
        grid.save()

        # Response grid has to be a dictionary
        response_grid = grid.to_dict()
        response_grid['squares'] = []

        # Make new squares and add them to the list on the response grid dictionary
        for i in range(0, 30):
            new_square = Square(grid=grid)
            new_square.save()
            response_grid['squares'].append(new_square.to_dict())

        return JsonResponse(response_grid, status=201)


@api_view(['GET', 'PATCH'])
def retrieve_or_update_animation_order(request, grid_id):

    if request.method == 'GET':
        # Need to add squares
        grid = Grid.objects.get(pk=grid_id)
        return JsonResponse(grid.to_dict())

    if request.method == 'PATCH':
        # Parse request data from JSON
        data = JSONParser().parse(request)

        # Find grid to update and update animation_order using request data
        grid = Grid.objects.get(pk=grid_id)
        grid.animation_order = data['animationOrder']
        grid.save()

        return JsonResponse(grid.to_dict())
