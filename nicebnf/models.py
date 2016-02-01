from django.db import models


"""
Models for nicebnf
"""
#
# Warning - even if you don't have any models, please don't delete this file.
# Some parts of Django require you to have something it can import called
# nicebnf.models in order for us to let you be a Django app.
#

class NiceBnfLinks(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=256)
