from django.db import models
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError



class Article (models.Model):
    #class Meta:
    #   abstract = True
    heading = models.CharField(validators=[validators.MinLengthValidator(2), validators.MaxLengthValidator(100)], max_length=100)
    content = models.CharField(validators=[validators.MinLengthValidator(10), validators.MaxLengthValidator(500)], max_length=500)
    publication = models.DateTimeField()
    def is_published(self):
        return self.publication < timezone.now()

    def __unicode__(self):
        return self.heading
    
    def validate(self, value):
        self.heading.validate()

