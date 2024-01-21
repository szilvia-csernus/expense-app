from django.db import models


class ClaimsCounter(models.Model):
    counter = models.IntegerField()

    def increment(self):
        self.counter += 1
        self.save()

    def __str__(self):
        return str(self.counter)
