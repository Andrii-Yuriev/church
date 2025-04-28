from django.db.models import Q
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView)
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import Religion, Church, Pastor, Disciple
from .forms import (
    ReligionForm,
    ChurchForm,
    PastorUpdateForm,
    DiscipleForm,
    RegistrationForm)


def get_common_counts():
    return {
        "religion_count": Religion.objects.count(),
        "church_count": Church.objects.count(),
        "pastor_count": Pastor.objects.count(),
        "disciple_count": Disciple.objects.count(),
    }


class HomeView(TemplateView):
    template_name = "religious_atlas/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        return context


class ReligionListView(ListView):
    model = Religion
    template_name = "religious_atlas/religion_list.html"
    context_object_name = "religions"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(founded_date__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ReligionDetailView(DetailView):
    model = Religion
    template_name = "religious_atlas/religion_detail.html"
    context_object_name = "religion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        religion_object = self.get_object()
        context["related_churches"] = Church.objects.filter(
            religion=religion_object)
        return context


class ReligionCreateView(LoginRequiredMixin, CreateView):
    model = Religion
    form_class = ReligionForm
    template_name = "religious_atlas/religion_form.html"
    success_url = reverse_lazy("religious_atlas:religion_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["view_title"] = "Add new religion"
        return context


class ReligionUpdateView(LoginRequiredMixin, UpdateView):
    model = Religion
    form_class = ReligionForm
    template_name = "religious_atlas/religion_form.html"
    success_url = reverse_lazy("religious_atlas:religion_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["view_title"] = f"Edit {self.object.name}"
        return context


class ReligionDeleteView(LoginRequiredMixin, DeleteView):
    model = Religion
    template_name = "religious_atlas/religion_confirm_delete.html"
    success_url = reverse_lazy("religious_atlas:religion_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        return context


class ChurchListView(ListView):
    model = Church
    template_name = "religious_atlas/church_list.html"
    context_object_name = "churches"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset().select_related("religion")
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(religion__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ChurchDetailView(DetailView):
    model = Church
    template_name = "religious_atlas/church_detail.html"
    context_object_name = "church"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        church_object = self.get_object()
        context["related_pastors"] = church_object.pastors.prefetch_related(
            "religion").all()
        return context


class ChurchCreateView(LoginRequiredMixin, CreateView):
    model = Church
    form_class = ChurchForm
    template_name = "religious_atlas/generic_form.html"
    success_url = reverse_lazy("religious_atlas:church_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["view_title"] = "Add new church"
        context["cancel_url"] = reverse_lazy("religious_atlas:church_list")
        return context


class ChurchUpdateView(LoginRequiredMixin, UpdateView):
    model = Church
    form_class = ChurchForm
    template_name = "religious_atlas/generic_form.html"
    success_url = reverse_lazy("religious_atlas:church_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["view_title"] = f"Edit: {self.object.name}"
        # Передаємо URL для кнопки "Скасувати" (на детальну сторінку)
        context["cancel_url"] = reverse_lazy("religious_atlas:church_detail",
                                             kwargs={"pk": self.object.pk})
        return context


class ChurchDeleteView(LoginRequiredMixin, DeleteView):
    model = Church
    template_name = "religious_atlas/generic_confirm_delete.html"
    success_url = reverse_lazy("religious_atlas:church_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["object_type"] = "Church"
        context["object_name"] = self.object.name
        context["cancel_url"] = reverse_lazy("religious_atlas:church_detail",
                                             kwargs={"pk": self.object.pk})
        return context


class PastorListView(ListView):
    model = Pastor
    template_name = "religious_atlas/pastor_list.html"
    context_object_name = "pastors"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset().select_related("religion")
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                (Q(religion__isnull=False) & Q(
                    religion__name__icontains=search_query))
            )
        queryset = queryset.filter(is_superuser=False)
        queryset = queryset.order_by("last_name", "first_name")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["search_query"] = self.request.GET.get("q", "")
        return context


class PastorDetailView(DetailView):
    model = Pastor
    template_name = "religious_atlas/pastor_detail.html"
    context_object_name = "pastor"

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        pastor_object = self.get_object()

        context[
            "serving_churches"] = pastor_object.serving_in_churches.prefetch_related(
            "religion").all()
        context["mentors"] = pastor_object.mentors.select_related(
            "church").all()
        return context


class PastorUpdateView(LoginRequiredMixin, UpdateView):
    model = Pastor
    form_class = PastorUpdateForm
    template_name = "religious_atlas/generic_form.html"

    def get_success_url(self):
        return reverse_lazy("religious_atlas:pastor_detail",
                            kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context[
            "view_title"] = f"Edit profile: {self.object.get_full_name()
                                             or self.object.username}"
        context[
            "cancel_url"] = self.get_success_url()
        return context


class PastorDeleteView(LoginRequiredMixin, DeleteView):
    model = Pastor
    template_name = "religious_atlas/generic_confirm_delete.html"
    success_url = reverse_lazy(
        "religious_atlas:pastor_list")

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["object_type"] = "Pastor"
        context[
            "object_name"] = (self.object.get_full_name()
                              or self.object.username)
        context['cancel_url'] = reverse_lazy("religious_atlas:pastor_detail",
                                             kwargs={"pk": self.object.pk})
        return context


class DiscipleListView(ListView):
    model = Disciple
    template_name = "religious_atlas/disciple_list.html"
    context_object_name = "disciples"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset().select_related('church',
                                                         'mentor_pastor',
                                                         'church__religion')
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                (Q(church__isnull=False) & Q(
                    church__name__icontains=search_query)) |
                (Q(mentor_pastor__isnull=False) & (
                        Q(mentor_pastor__username__icontains=search_query) |
                        Q(mentor_pastor__first_name__icontains=search_query) |
                        Q(mentor_pastor__last_name__icontains=search_query)
                ))
            )
        return queryset.order_by('last_name',
                                 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context['search_query'] = self.request.GET.get('q',
                                                       '')
        return context


class DiscipleCreateView(LoginRequiredMixin, CreateView):
    model = Disciple
    form_class = DiscipleForm
    template_name = "religious_atlas/generic_form.html"
    success_url = reverse_lazy("religious_atlas:disciple_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["view_title"] = "Add new disciple"
        context["cancel_url"] = reverse_lazy("religious_atlas:disciple_list")
        return context


class DiscipleUpdateView(LoginRequiredMixin, UpdateView):
    model = Disciple
    form_class = DiscipleForm
    template_name = "religious_atlas/generic_form.html"
    success_url = reverse_lazy("religious_atlas:disciple_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["view_title"] = f"Edit: {self.object.full_name}"
        context["cancel_url"] = reverse_lazy("religious_atlas:disciple_list")
        return context


class DiscipleDeleteView(LoginRequiredMixin, DeleteView):
    model = Disciple
    template_name = "religious_atlas/generic_confirm_delete.html"
    success_url = reverse_lazy("religious_atlas:disciple_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_counts())
        context["object_type"] = "Disciple"
        context["object_name"] = self.object.full_name
        context["cancel_url"] = reverse_lazy("religious_atlas:disciple_list")
        return context


class RegistrationView(FormView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("/")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
