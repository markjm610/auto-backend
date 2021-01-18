from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Grid
import json


class GridTests(TestCase):

    def test_create_grid(self):
        client = APIClient()
        response = client.post('/grids/', {}, format='json')
        # print(response.status_code)
        self.assertEqual(response.status_code, 201)
        self.assertEquals(response.json()['animation_order'], '')

    def test_retrieve_animation_order(self):
        test_grid = Grid(animation_order='')
        test_grid.save()
        client = APIClient()
        response = client.get(f'/grids/{test_grid.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_grid.to_dict())

    def test_save_animation_order(self):
        pass
