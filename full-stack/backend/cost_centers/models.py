from django.db import models


class Church(models.Model):
    """Church model"""
    short_name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    claims_counter = models.IntegerField(default=0)
    finance_contact_name = models.CharField(max_length=200, null=True,
                                            blank=True)
    finance_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.short_name

    def increment_claims_counter(self):
        self.claims_counter += 1
        self.save()

    class Meta:
        verbose_name_plural = "Churches"


class CostPurpose(models.Model):
    """Cost Purpose model"""
    church = models.ForeignKey(Church,
                               null=True,
                               related_name='cost_purposes',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cost_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
