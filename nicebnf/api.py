from rest_framework import generics
from rest_framework.response import Response
from nicebnf.models import NiceBnfLinks

class NiceBnfLinks(generics.ListCreateAPIView):
    queryset = NiceBnfLinks.objects.all()

    def list(self, request):
        return Response(self.get_queryset().values_list("href", "title"))
