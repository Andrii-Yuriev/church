from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Religion, Pastor, Church, Disciple


class PastorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Pastor info", {"fields": ("bio", "photo", "religion")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Pastor info", {"fields": (
            "bio", "photo", "religion",
            "first_name", "last_name", "email")}),
    )
    list_display = ("username", "email",
                    "first_name", "last_name", "is_staff", "religion")
    list_filter = UserAdmin.list_filter + ("religion",)
    search_fields = UserAdmin.search_fields + ("bio",)


@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    list_display = ("name", "founded_date")
    search_fields = ("name", "description")


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ("name", "religion", "founding_period", "get_pastors_count")
    list_filter = ("religion",)
    search_fields = ("name", "description", "founding_period")
    filter_horizontal = ("pastors",)

    def get_pastors_count(self, obj):
        return obj.pastors.count()

    get_pastors_count.short_description = "Number of Pastors"


@admin.register(Disciple)
class DiscipleAdmin(admin.ModelAdmin):
    list_display = ("full_name", "church", "mentor_pastor", "joining_date")
    list_filter = ("church", "mentor_pastor", "joining_date")
    search_fields = ("first_name", "last_name", "email",
                     "church__name", "mentor_pastor__username")
    list_select_related = ("church", "mentor_pastor")


admin.site.register(Pastor, PastorAdmin)
