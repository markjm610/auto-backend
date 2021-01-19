from django.db import models


class Grid(models.Model):
    def __str__(self):
        return self.animation_order

    def to_dict(self):
        return {
            'id': self.id,
            'animation_order': self.animation_order,
        }

    animation_order = models.CharField(max_length=200, default='')


class Square(models.Model):

    def to_dict(self):
        return {
            'id': self.id,
            'color': self.color,
            'grid': self.grid.id,
        }

    color = models.CharField(max_length=200, default='blue')
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE)
