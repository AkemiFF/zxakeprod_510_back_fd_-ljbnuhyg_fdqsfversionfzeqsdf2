from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import HebergementSerializer
from Hebergement.models import Hebergement
from rest_framework.permissions import IsAdminUser, IsAuthenticated

@api_view(['GET'])
def get_count(request):
    try:
        number_hebergement = Hebergement.objects.count()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_hebergement}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_hebergements(request):
    try:
        all_hebergement = Hebergement.objects.all()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(all_hebergement, many=True)
    return Response({'hebergements': serializer.data}, status=status.HTTP_200_OK)
