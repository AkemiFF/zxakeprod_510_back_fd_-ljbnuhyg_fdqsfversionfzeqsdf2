from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from Accounts.models import ResponsableEtablissement
from validate_email import validate_email  # type: ignore
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ResponsableEtablissementLoginSerializer
from .serializers import ResponsableEtablissementSerializer


# Tous les responsable
@api_view(['GET'])
def get_responsables_etablissement(request):
    responsables = ResponsableEtablissement.objects.all()
    serializer = ResponsableEtablissementSerializer(responsables, many=True)
    return Response(serializer.data)

# Responsable selectionner par id


@api_view(['GET'])
def get_responsable_etablissement_detail(request, pk):
    try:
        responsable = ResponsableEtablissement.objects.get(pk=pk)
        serializer = ResponsableEtablissementSerializer(responsable)
        return Response(serializer.data)
    except ResponsableEtablissement.DoesNotExist:
        return Response({"message": "Le responsable d'établissement n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

# Creer des responsable etablissement


@api_view(['POST'])
def signup_responsable(request):
    if request.method == 'POST':
        serializer = ResponsableEtablissementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update responsable


@api_view(['PUT'])
def update_responsable_etablissement(request, pk):
    try:
        responsable = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response({"message": "Le responsable d'établissement n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ResponsableEtablissementSerializer(
        responsable, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete responsable


@api_view(['DELETE'])
def delete_responsable_etablissement(request, pk):
    try:
        responsable = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response({"message": "Le responsable d'établissement n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

    responsable.delete()
    return Response({"message": "Le responsable d'établissement a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)


# Login
@api_view(['POST'])
@permission_classes([AllowAny])  # Permettre à tout le monde de se connecter
def responsable_etablissement_login(request):
    serializer = ResponsableEtablissementLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check_email(request):
    email = request.GET.get('email')
    # Vérifie l'existence du domaine
    is_valid = validate_email(email, verify=True)
    return JsonResponse({'is_valid': is_valid})
