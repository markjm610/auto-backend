## [Link to application](https://auto-frontend-mark.herokuapp.com/)

# What is this?
## Django application that servers as a back end server for a React front end using Django REST Framework

# Example view:

```python
@api_view(['GET', 'PATCH'])
def retrieve_or_update_grid(request, grid_id):

    if request.method == 'GET':
        # Find grid with ID
        grid = Grid.objects.get(pk=grid_id)

        # Find squares for that grid and convert to a list of dictionaries
        squares = [square.to_dict()
                   for square in Square.objects.filter(grid=grid_id).order_by('id')]

        # Convert Grid object to list dictionary and set squares key to squares list
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

        # If specific square colors need to be updated, update them
        if 'squareColors' in data:
            for square in data['squareColors']:
                square_to_update = Square.objects.get(pk=square['id'])
                square_to_update.color = square['color']
                square_to_update.save()
        # If no square colors are on the request, it means this is a reset, so reset all colors to their defaults
        else:
            squares = Square.objects.filter(grid=grid_id)
            for square in squares:
                square.color = 'blue'
                square.save()

        return JsonResponse(grid.to_dict())

```

# Test for that view:
```python
def test_update_grid(self):
        # Create test grid
        test_grid = Grid(animation_order='')
        test_grid.save()

        # Create squares and save a few square IDs for a request later
        saved_square_ids = []

        for i in range(0, 30):
            new_square = Square(grid=test_grid)
            new_square.save()
            if i == 3 or i == 10 or i == 20 or i == 24:
                saved_square_ids.append(new_square.id)

        # Mock response
        client = APIClient()
        response = client.patch(
            f'/grids/{test_grid.id}', {'animationOrder': '1,2,3,4,5'}, format='json')
        updated_grid = Grid.objects.get(pk=test_grid.id)

        # Animation order gets updated, but ID doesn't
        self.assertEqual(test_grid.id, updated_grid.id)
        self.assertNotEqual(test_grid.animation_order,
                            updated_grid.animation_order)

        # Animation order is updated to correct value
        self.assertEqual(updated_grid.animation_order, '1,2,3,4,5')

        # Colors are all reset when there is no squareColors key in the request
        squares = Square.objects.filter(grid=updated_grid)
        for square in squares:
            self.assertEqual(square.color, 'blue')

        # Response status code and correct JSON in response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), updated_grid.to_dict())
        self.assertEqual(
            response.json()['animation_order'], updated_grid.animation_order)

        # Correct square colors are reset when there is a squareColors key in the request using saved square IDs from above
        response = client.patch(
            f'/grids/{test_grid.id}', {'animationOrder': '1,2,3,4,5', 'squareColors': [{'id': saved_square_ids[0], 'color': 'red'}, {'id': saved_square_ids[1], 'color': 'green'}, {'id': saved_square_ids[2], 'color': 'blue'}]}, format='json')
        self.assertEqual(Square.objects.get(
            pk=saved_square_ids[0]).color, 'red')
        self.assertEqual(Square.objects.get(
            pk=saved_square_ids[1]).color, 'green')
        self.assertEqual(Square.objects.get(
            pk=saved_square_ids[2]).color, 'blue')
        # This last one wasn't edited
        self.assertEqual(Square.objects.get(
            pk=saved_square_ids[3]).color, 'blue')

        # Grid is still updated
        updated_grid = Grid.objects.get(pk=test_grid.id)
        self.assertEqual(updated_grid.animation_order, '1,2,3,4,5')
```
