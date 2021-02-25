from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class ServiceStatus(GenericAPIView):
    def get(self, request):
        return Response(data={'OK': 'O serviço está funcionando!'}, status=status.HTTP_200_OK)
