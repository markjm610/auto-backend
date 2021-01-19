from django.db import models


class Grid(models.Model):
    def __str__(self):
        return self.animation_order + self.color

    def to_dict(self):
        return {
            'id': self.id,
            'animation_order': self.animation_order,
            'color': self.color,
        }

    animation_order = models.CharField(max_length=200, default='')
    color = models.CharField(max_length=200, default='blue')
