from django.urls import path
from . import views

app_name = "religious_atlas"

urlpatterns = [
    path("religions/", views.ReligionListView.as_view(),
         name="religion_list"),
    path("religions/<int:pk>/", views.ReligionDetailView.as_view(),
         name="religion_detail"),

    path("churches/", views.ChurchListView.as_view(), name="church_list"),
    path("churches/<int:pk>/", views.ChurchDetailView.as_view(),
         name="church_detail"),

    path("pastors/", views.PastorListView.as_view(), name="pastor_list"),
    path("pastors/<int:pk>/", views.PastorDetailView.as_view(),
         name="pastor_detail"),
    path("disciples/", views.DiscipleListView.as_view(), name="disciple_list"),
]
