from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    availability = models.BooleanField(default=True)

    # rearrange the order of the fields in the admin page
    class Meta:
        ordering = ['title']
