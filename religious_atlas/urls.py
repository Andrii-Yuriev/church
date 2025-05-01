from django.urls import path
from . import views

app_name = "religious_atlas"

urlpatterns = [
    path("religions/", views.ReligionListView.as_view(),
         name="religion_list"),
    path("religions/<int:pk>/", views.ReligionDetailView.as_view(),
         name="religion_detail"),

    path("religions/add/", views.ReligionCreateView.as_view(),
         name="religion_add"),
    path("religions/<int:pk>/edit/", views.ReligionUpdateView.as_view(),
         name="religion_edit"),
    path("religions/<int:pk>/delete/", views.ReligionDeleteView.as_view(),
         name="religion_delete"),

    path("churches/", views.ChurchListView.as_view(), name="church_list"),
    path("churches/<int:pk>/", views.ChurchDetailView.as_view(),
         name="church_detail"),
    path("churches/add/", views.ChurchCreateView.as_view(), name="church_add"),
    path("churches/<int:pk>/edit/", views.ChurchUpdateView.as_view(),
         name="church_edit"),
    path("churches/<int:pk>/delete/", views.ChurchDeleteView.as_view(),
         name="church_delete"),

    path("pastors/", views.PastorListView.as_view(), name="pastor_list"),
    path("pastors/<int:pk>/", views.PastorDetailView.as_view(),
         name="pastor_detail"),
    path("pastors/<int:pk>/edit/", views.PastorUpdateView.as_view(),
         name="pastor_edit"),
    path("pastors/<int:pk>/delete/", views.PastorDeleteView.as_view(),
         name="pastor_delete"),

    path("disciples/", views.DiscipleListView.as_view(), name="disciple_list"),
    path("disciples/add/", views.DiscipleCreateView.as_view(),
         name="disciple_add"),
    path("disciples/<int:pk>/edit/", views.DiscipleUpdateView.as_view(),
         name="disciple_edit"),
    path("disciples/<int:pk>/delete/", views.DiscipleDeleteView.as_view(),
         name="disciple_delete"),
]
