from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .models import Grid, Square


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
        # Find grid with ID
        grid = Grid.objects.get(pk=grid_id)

        # Find squares for that grid and convert to a list of dictionaries
        squares = [square.to_dict()
                   for square in Square.objects.filter(grid=grid_id)]

        # Convert Grid object to list dictionary and add squares key equal to squares list
        response_grid = grid.to_dict()
        response_grid['squares'] = squares

        # Send grid dictionary back as JSON
        return JsonResponse(response_grid)

    if request.method == 'PATCH':
        # Parse request data from JSON
        data = JSONParser().parse(request)

        # Find grid to update and update animation_order using request data
        grid = Grid.objects.get(pk=grid_id)
        grid.animation_order = data['animationOrder']
        grid.save()

        return JsonResponse(grid.to_dict())


@api_view(['PATCH'])
def update_square(request, square_id):
    # Parse request data from JSON
    data = JSONParser().parse(request)

    # Find square to update and update color
    square = Square.objects.get(pk=square_id)
    square.color = data['color']
    square.save()

    return JsonResponse(square.to_dict())
