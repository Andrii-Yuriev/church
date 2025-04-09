from django.urls import path
from . import views

app_name = "religious_atlas"

urlpatterns = [
    path("religions/", views.ReligionListView.as_view(),
         name="religion_list"),
    path("religions/<int:pk>/", views.ReligionDetailView.as_view(),
         name="religion_detail"),
]
