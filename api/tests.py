from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Coord, Image, Level, MountainPass, Tourist
from .serializers import MountainPassSerializer


class TestViews(TestCase):
    def test_list_perevals(self):
        client = Client()

        response = client.get(reverse("mountain-pass-list"))

        self.assertEqual(response.status_code, 200)


class SubmitDataAPITests(APITestCase):
    def setUp(self):
        self.pereval_1 = MountainPass.objects.create(
            tourist_id=Tourist.objects.create(
                email="emailtest@gmail.com",
                last_name="testLastName",
                first_name="testName",
                middle_name="testMiddleName",
                phone="+7(999)9999999",
            ),
            beauty_title="test BT",
            title="test title",
            other_titles="tests other titles",
            connect="test connect",
            status="NW",
            coord_id=Coord.objects.create(
                latitude=23.123, longitude=87.789, height=234
            ),
            level=Level.objects.create(
                winter_lev="4A",
                spring_lev="2A",
                summer_lev="1A",
                autumn_lev="3A",
            ),
        )
        self.image_1 = Image.objects.create(
            image="", title="test-title", pereval_id=self.pereval_1
        )

        self.pereval_2 = MountainPass.objects.create(
            tourist_id=Tourist.objects.create(
                email="emailtesttwo@gmail.com",
                last_name="testLastNameTwo",
                first_name="testNametwo",
                middle_name="testMiddleNameTwo",
                phone="+7(959)9595599",
            ),
            beauty_title="test two BT",
            title="test two title",
            other_titles="tests other titles two",
            connect="test connect two",
            status="NW",
            coord_id=Coord.objects.create(
                latitude=23.983, longitude=97.789, height=224
            ),
            level=Level.objects.create(
                winter_lev="4A",
                spring_lev="2A",
                summer_lev="1A",
                autumn_lev="3A",
            ),
        )
        self.image_2 = Image.objects.create(
            image="", title="test-title-two", pereval_id=self.pereval_2
        )

    def test_list(self):
        response = self.client.get(reverse("mountain-pass-list"))
        serializer_data = MountainPassSerializer(
            [self.pereval_1, self.pereval_2], many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MountainPass.objects.count(), 2)
        self.assertEqual(serializer_data, response.data)
        pereval_object_1 = MountainPass.objects.filter(beauty_title="test BT").first()
        self.assertEqual(pereval_object_1.beauty_title, "test BT")
        pereval_object_2 = MountainPass.objects.filter(
            beauty_title="test two BT"
        ).first()
        self.assertEqual(pereval_object_2.beauty_title, "test two BT")

    def test_detail(self):
        response = self.client.get(
            reverse("mountain-pass-detail", kwargs={"pk": self.pereval_1.pk})
        )
        serializer_data = MountainPassSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_two(self):
        response = self.client.get(
            reverse("mountain-pass-detail", kwargs={"pk": self.pereval_2.pk})
        )
        serializer_data = MountainPassSerializer(self.pereval_2).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
