from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.views import (
    TouristViewset,
    CoordViewset,
    LevelViewset,
    ImageViewset,
    MountainPassViewset,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = routers.DefaultRouter()
router.register(r"tourists", TouristViewset, basename="tourists")
router.register(r"coords", CoordViewset, basename="coords")
router.register(r"levels", LevelViewset, basename="levels")
router.register(r"images", ImageViewset, basename="images")
router.register(r"mountain-pass", MountainPassViewset, basename="mountain-pass")
router.register(r"mountain-pass", MountainPassViewset, basename="mountain-pass-list")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
