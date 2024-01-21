from django.db import models


class Church(models.Model):
    """Church model"""
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Churches"


class CostPurpose(models.Model):
    """Cost Purpose model"""
    church = models.ForeignKey(Church,
                               null=True,
                               related_name='cost_purposes',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cost_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
