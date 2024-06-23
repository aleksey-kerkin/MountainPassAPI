from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Tourist, Coord, Level, Image, MountainPass
from .serializers import (
    TouristSerializer,
    CoordSerializer,
    LevelSerializer,
    ImageSerializer,
    MountainPassSerializer,
)


class TouristViewset(viewsets.ModelViewSet):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer


class CoordViewset(viewsets.ModelViewSet):
    queryset = Coord.objects.all()
    serializer_class = CoordSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class MountainPassViewset(viewsets.ModelViewSet):
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassSerializer
    filterset_fields = ("tourist_id__email",)

    def create(self, request, *args, **kwargs):
        serializer = MountainPassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": None,
                    "id": serializer.data["id"],
                }
            )
        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad Request",
                    "id": None,
                }
            )
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Ошибка подключения к базе данных",
                    "id": None,
                }
            )

    def partial_update(self, request, *args, **kwargs):
        mountain_pass = self.get_object()
        if mountain_pass.status == "NW":
            serializer = MountainPassSerializer(
                mountain_pass, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "state": "1",
                        "message": "Запись успешно изменена",
                    }
                )
            else:
                return Response({"state": "0", "message": serializer.errors})
        else:
            return Response(
                {
                    "state": "0",
                    "message": f"Отклонено! Причина: {mountain_pass.get_status_display()}",
                }
            )
