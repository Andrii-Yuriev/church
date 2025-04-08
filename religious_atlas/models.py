from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Religion(models.Model):
    name = models.CharField(
        _("Religion Name"),
        max_length=255,
        unique=True,
        help_text=_("Unique name of the religion")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Detailed description of the religion")
    )
    founded_date = models.DateField(
        _("Founded Date"),
        null=True,
        blank=True,
        help_text=_("Approximate or exact date the religion was founded")
    )
    icon = models.ImageField(
        _("Icon/Symbol"),
        upload_to="religion/icons/",
        blank=True,
        null=True,
        help_text=_("Graphic symbol or icon of the religion")
    )

    class Meta:
        verbose_name = _("Religion")
        verbose_name_plural = _("Religions")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Pastor(AbstractUser):
    bio = models.TextField(
        _("Biography"),
        blank=True,
        help_text=_("Short biography of the pastor")
    )
    photo = models.ImageField(
        _("Photo"),
        upload_to="pastors/photos/",
        null=True,
        blank=True,
        help_text=_("Photograph of the pastor")
    )
    religion = models.ForeignKey(
        Religion,
        verbose_name=_("Religion"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="religions",
        help_text=_("The religion of the pastor represents")
    )

    class Meta:
        verbose_name = _("Pastor")
        verbose_name_plural = _("Pastors")

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class Church(models.Model):
    name = models.CharField(
        _("Church Name"),
        max_length=255,
        help_text=_("Official or common name of the church")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("History, features, etc"),
    )
    religion = models.ForeignKey(
        Religion,
        verbose_name=_("Religion"),
        on_delete=models.CASCADE,
        related_name="churches",
        help_text=_("The main religion of this church")
    )
    photo = models.ImageField(
        _("Photo"),
        upload_to="churches/photos/",
        null=True,
        blank=True,
        help_text=_("Photograph of the church or representative image")
    )
    pastors = models.ManyToManyField(
        Pastor,
        verbose_name=_("Pastors"),
        blank=True,
        related_name="serving_in_churches",
        help_text=_("Pastors serving in this church")
    )

    class Meta:
        verbose_name = _("Church")
        verbose_name_plural = _("Churches")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Disciple(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(
        _("Email Address"),
        blank=True,
        null=True,
        help_text=_("Email address of the discipline(optional)")
    )
    joining_date = models.DateField(
        _("Joining Date"),
        null=True,
        blank=True,
        help_text=_("Date the person joined the church/community")
    )
    church = models.ForeignKey(
        Church,
        verbose_name=_("Church"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="disciples",
        help_text=_("The church the disciple belongs to (can be unspecified)")
    )
    mentor_pastor = models.ForeignKey(
        Pastor,
        verbose_name=_("Mentor Pastor"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentors",
        help_text=_("The pastor mentoring this person (optional)")
    )

    class Meta:
        verbose_name = _("Disciple")
        verbose_name_plural = _("Disciples")
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
