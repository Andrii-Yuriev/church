from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Religion, Church, Pastor, Disciple


def get_common_counts():
    return {
        "religion_count": Religion.objects.count(),
        "church_count": Church.objects.count(),
        "pastor_count": Pastor.objects.count(),
        "disciple_count": Disciple.objects.count(),
    }


class ReligionListView(ListView):
    model = Religion
    template_name = "religious_atlas/religion_list.html"
    context_object_name = "religions"
    paginate_by = 1

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


class ChurchListView(ListView):
    model = Church
    template_name = "religious_atlas/church_list.html"
    context_object_name = "churches"
    paginate_by = 1

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

    def context_data(self, **kwargs):
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


class PastorListView(ListView):
    model = Pastor
    template_name = "religious_atlas/pastor_list.html"
    context_object_name = "pastors"
    paginate_by = 1

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


class DiscipleListView(ListView):
    model = Disciple
    template_name = "religious_atlas/disciple_list.html"
    context_object_name = "disciples"
    paginate_by = 1

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
