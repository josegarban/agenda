import json

from django.db import models
from django.urls import reverse
from django.forms.models import model_to_dict

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def to_dict(self):
        dict_self = model_to_dict(self)
        return dict_self

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
