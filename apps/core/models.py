from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.edited = True
        super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
