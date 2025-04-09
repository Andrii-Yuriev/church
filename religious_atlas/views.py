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
