from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .models import Grid

# Create your views here.


@api_view(['POST'])
def create_grid(request):

    if request.method == 'POST':
        grid = Grid(animation_order='')
        grid.save()
        return JsonResponse(grid.to_dict())


@api_view(['GET', 'PATCH'])
def retrieve_or_save_animation_order(request, grid_id):

    if request.method == 'GET':
        grid = Grid.objects.get(pk=grid_id)
        return JsonResponse(grid.to_dict())

    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        grid = Grid.objects.get(pk=grid_id)
        grid.animation_order = data['animationOrder']
        grid.save()
        return JsonResponse(grid.to_dict())
