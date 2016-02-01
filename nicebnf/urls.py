"""
Urls for the nicebnf OPAL plugin
"""
from django.conf.urls import patterns, url
from nicebnf import api

urlpatterns = patterns(
    '',
    url('^nicebnf/', api.NiceBnfLinks.as_view()),
)
