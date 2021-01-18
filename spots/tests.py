from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Grid
import json


class GridTests(TestCase):

    def test_create_grid(self):
        client = APIClient()
        response = client.post('/grids/', {}, format='json')

        # Grid object got added to database
        self.assertEqual(len(Grid.objects.all()), 1)

        # Response status code and correct JSON in response
        self.assertEqual(response.status_code, 201)
        self.assertEquals(response.json()['animation_order'], '')

    def test_retrieve_animation_order(self):
        test_grid = Grid(animation_order='')
        test_grid.save()
        client = APIClient()
        response = client.get(f'/grids/{test_grid.id}')

        # Response status code and correct JSON in response, meaning correct grid is retrieved
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_grid.to_dict())

    def test_save_animation_order(self):
        test_grid = Grid(animation_order='')
        test_grid.save()
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
