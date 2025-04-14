from django import forms
from .models import Religion, Church, Pastor, Disciple


class ReligionForm(forms.ModelForm):
    class Meta:
        model = Religion
        fields = "__all__"


class ChurchForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = "__all__"


class PastorUpdateForm(forms.ModelForm):
    class Meta:
        model = Pastor
        fields = ["first_name", "last_name", "email", "bio", "photo",
                  "religion"]


class DiscipleForm(forms.ModelForm):
    class Meta:
        model = Disciple
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mentor_pastor"].queryset = Pastor.objects.filter(
            is_superuser=False)
