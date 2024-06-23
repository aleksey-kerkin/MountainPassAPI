from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Tourist, Coord, Level, Image, MountainPass


class TouristSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourist
        fields = ["email", "last_name", "first_name", "middle_name", "phone"]


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ["latitude", "longitude", "height"]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["winter_lev", "spring_lev", "summer_lev", "autumn_lev"]


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Image
        fields = ["image", "title"]


class MountainPassSerializer(WritableNestedModelSerializer):
    tourist_id = TouristSerializer()
    coord_id = CoordSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)
    add_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = MountainPass
        depth = 1
        fields = [
            "id",
            "beauty_title",
            "title",
            "other_titles",
            "connect",
            "add_time",
            "tourist_id",
            "coord_id",
            "level",
            "images",
            "status",
        ]

    def create(self, validated_data, **kwargs):
        tourist_id = validated_data.pop("tourist_id")
        coord_id = validated_data.pop("coord_id")
        level = validated_data.pop("level")
        images = validated_data.pop("images")

        tourist_id, created = Tourist.objects.get_or_create(**tourist_id)

        coord_id = Coord.objects.create(**coord_id)
        level = Level.objects.create(**level)
        mountain_pass = MountainPass.objects.create(
            **validated_data, tourist_id=tourist_id, coord_id=coord_id, level=level
        )

        for i in images:
            image = i.pop("image")
            title = i.pop("title")
            Image.objects.create(image=image, pereval_id=mountain_pass, title=title)

        return mountain_pass

    def validate(self, data):
        if self.instance is not None:
            instance_tourist_id = self.instance.tourist_id
            data_tourist_id = data.get("tourist_id")

            if data_tourist_id is not None:
                validating_tourist_id_fields = [
                    instance_tourist_id.last_name != data_tourist_id["last_name"],
                    instance_tourist_id.first_name != data_tourist_id["first_name"],
                    instance_tourist_id.middle_name != data_tourist_id["middle_name"],
                    instance_tourist_id.phone != data_tourist_id["phone"],
                    instance_tourist_id.email != data_tourist_id["email"],
                ]

                if any(validating_tourist_id_fields):
                    raise serializers.ValidationError(
                        {"Отклонено": "Нельзя изменять данные пользователя"}
                    )
        return data
