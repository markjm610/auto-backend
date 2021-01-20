from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Grid, Square
import json

# def create_grid_and_squares():


class GridTests(TestCase):

    def test_create_grid(self):
        # Mock response
        client = APIClient()
        response = client.post('/grids/', {}, format='json')

        # Grid object got added to database
        self.assertEqual(len(Grid.objects.all()), 1)

        # Response status code and correct JSON in response
        self.assertEqual(response.status_code, 201)
        self.assertEquals(response.json()['animation_order'], '')
        self.assertEquals(len(response.json()['squares']), 30)

    def test_retrieve_grid(self):
        # Make test grid and test squares, adding squares to grid dictionary on squares key
        test_grid = Grid(animation_order='')
        test_grid.save()
        test_squares = [square.to_dict()
                        for square in Square.objects.filter(grid=test_grid.id)]
        test_response_grid = test_grid.to_dict()
        test_response_grid['squares'] = test_squares

        # Mock response
        client = APIClient()
        response = client.get(f'/grids/{test_grid.id}')

        # Response status code and correct JSON in response, meaning correct grid is retrieved
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_response_grid)

    def test_save_animation_order(self):
        # Create test grid
        test_grid = Grid(animation_order='')
        test_grid.save()

        # Mock response
        client = APIClient()
        response = client.patch(
            f'/grids/{test_grid.id}', {'animationOrder': '12345'}, format='json')
        updated_grid = Grid.objects.get(pk=test_grid.id)

        # Animation order gets updated, but ID doesn't
        self.assertEqual(test_grid.id, updated_grid.id)
        self.assertNotEqual(test_grid.animation_order,
                            updated_grid.animation_order)

        # Animation order is updated to correct value
        self.assertEqual(updated_grid.animation_order, '12345')

        # Response status code and correct JSON in response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), updated_grid.to_dict())
        self.assertEqual(
            response.json()['animation_order'], updated_grid.animation_order)

    def test_update_square(self):
        # Making test grid and test square
        test_grid = Grid()
        test_grid.save()
        test_square = Square(grid=test_grid)
        test_square.save()

        # Mock response
        client = APIClient()
        response = client.patch(
            f'/grids/squares/{test_square.id}', {'color': 'red'}, format='json')

        # Get updated test square
        updated_square = Square.objects.get(pk=test_square.id)

        # Color property is updated on square
        self.assertNotEqual(test_square.color, updated_square.color)

        # Response status code and correct JSON in response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), updated_square.to_dict())
