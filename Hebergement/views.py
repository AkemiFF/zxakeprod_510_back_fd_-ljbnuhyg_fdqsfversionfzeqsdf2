# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import ImageChambreSerializer, HebergementSerializer
from rest_framework import generics
from Hebergement.models import ImageChambre, Hebergement


class ImageChambreListAPIView(generics.ListAPIView):
    queryset = ImageChambre.objects.all()
    serializer_class = ImageChambreSerializer


@api_view(['GET'])
def get_count(request):
    try:
        number_hebergement = Hebergement.objects.count(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = HebergementSerializer(number_hebergement)
    return Response(serializer.data)


@api_view(['POST'])
def post_count(request, pk):
    serializer = HebergementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def put_count(request, pk):
    try:
        type_responsable = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Hebergement(type_responsable, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_count(request, pk):
    try:
        type_responsable = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    type_responsable.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
