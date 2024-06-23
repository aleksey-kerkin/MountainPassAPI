from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def get_path_upload_photos(instance, file):
    return f"photos/pereval-{instance.pereval.id}/{file}"


class Tourist(models.Model):
    email = models.EmailField(max_length=128)
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128)
    phone = PhoneNumberField(blank=True)

    class Meta:
        verbose_name = "Tourist"
        verbose_name_plural = "Tourists"


class MountainPassAdded(models.Model):
    STATUS_CHOICES = (
        ("new", "новый"),
        ("pending", "в работе"),
        ("accepted", "принято"),
        ("rejected", "отклонено"),
    )

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255)
    add_time = models.DateTimeField(auto_now_add=True)
    coord_id = models.OneToOneField("Coord", on_delete=models.CASCADE)
    tourist_id = models.ForeignKey("Tourist", on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="new")
    level = models.ForeignKey("Level", on_delete=models.CASCADE)


class MountainPass(models.Model):
    NEW = "NW"
    PENDING = "PN"
    ACCEPTED = "AC"
    REJECTED = "RJ"
    STATUS_CHOICES = (
        ("NW", "new"),
        ("PN", "pending"),
        ("AC", "accepted"),
        ("RJ", "rejected"),
    )

    beauty_title = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    other_titles = models.CharField(max_length=128)
    connect = models.CharField(max_length=128)
    add_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    coord_id = models.OneToOneField("Coord", on_delete=models.CASCADE)
    tourist_id = models.ForeignKey("Tourist", on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="NW")
    level = models.ForeignKey("Level", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MountainPass"
        verbose_name_plural = "MountainPasses"


class Coord(models.Model):
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=10)
    height = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Coord"
        verbose_name_plural = "Coords"


class Level(models.Model):
    winter = "4A"
    spring = "2A"
    summer = "1A"
    autumn = "3A"

    LEVEL_CHOICES = (
        ("4A", "winter"),
        ("2A", "spring"),
        ("1A", "summer"),
        ("3A", "autumn"),
    )
    winter_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)
    spring_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)
    summer_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)
    autumn_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)


class Image(models.Model):
    image = models.ImageField(
        upload_to=get_path_upload_photos, verbose_name="picture", blank=True, null=True
    )
    title = models.CharField(max_length=128)
    pereval_id = models.ForeignKey(
        "MountainPass", on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self):
        return f"{self.pk}: {self.title}"

    class Meta:
        verbose_name = "pictures"
        verbose_name_plural = "pictures"
