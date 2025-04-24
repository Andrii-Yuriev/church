import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import (
    RegistrationForm,
    PastorUpdateForm,
    DiscipleForm,
    ReligionForm,
)

from .models import Religion, Church, Pastor, Disciple

User = get_user_model()


class ReligionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Religion.objects.create(
            name="Test Religion", description="A test description"
        )

    def test_religion_str(self):
        religion = Religion.objects.get(id=1)
        self.assertEqual(str(religion), "Test Religion")

    def test_religion_content(self):
        religion = Religion.objects.get(id=1)
        self.assertEqual(religion.name, "Test Religion")
        self.assertEqual(religion.description, "A test description")


class PastorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="testpastor_model",
            password="password123",
            first_name="Test",
            last_name="PastorModel",
        )

    def test_pastor_full_name(self):
        pastor = get_user_model().objects.get(username="testpastor_model")
        self.assertEqual(pastor.get_full_name(), "Test PastorModel")

    def test_pastor_str(self):
        pastor = get_user_model().objects.get(username="testpastor_model")
        self.assertEqual(str(pastor), "Test PastorModel")


class ReligiousAtlasViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_pastor_del = User.objects.create_user(
            username="testpastor_del",
            password="password123",
            first_name="Test",
            last_name="Pastor Del",
            is_staff=False,
        )
        cls.staff_user = User.objects.create_user(
            username="staffuser",
            password="password123",
            is_staff=True,
            first_name="Staff",
            last_name="User",
        )
        cls.regular_user = User.objects.create_user(
            username="regularuser",
            password="password123",
            first_name="Regular",
            last_name="User",
        )
        cls.pastor2 = User.objects.create_user(
            username="pastor2_usr",
            password="password123",
            first_name="Pastor",
            last_name="Two",
            is_staff=False,
        )
        cls.pastor3 = User.objects.create_user(
            username="pastor3_usr",
            password="password123",
            first_name="Pastor",
            last_name="Three",
            is_staff=False,
        )
        cls.pastor4 = User.objects.create_user(
            username="pastor4_usr",
            password="password123",
            first_name="Pastor",
            last_name="Four",
            is_staff=False,
        )

        cls.religion1 = Religion.objects.create(
            name="Religion Alpha",
            description="Desc Alpha",
            founded_date="2000-01-01",
        )
        cls.religion2 = Religion.objects.create(
            name="Religion Beta",
            description="Desc Beta",
            founded_date="2010-01-01",
        )
        cls.church1 = Church.objects.create(
            name="Church Alpha",
            religion=cls.religion1,
            description="Church Desc 1",
        )
        cls.church2 = Church.objects.create(
            name="Church Beta",
            religion=cls.religion2,
            description="Church Desc 2",
        )
        cls.disciple1 = Disciple.objects.create(
            first_name="Disc",
            last_name="One",
            email="disc1@example.com",
            church=cls.church1,
            mentor_pastor=cls.test_pastor_del,
        )
        cls.disciple2 = Disciple.objects.create(
            first_name="Disc",
            last_name="Two",
            email="disc2@example.com",
            church=cls.church2,
            mentor_pastor=cls.pastor2,
        )

    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "religious_atlas/home.html")

    def test_home_view_context_counts(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.context["religion_count"], 2)
        self.assertEqual(response.context["church_count"], 2)
        self.assertEqual(response.context["pastor_count"], 6)
        self.assertEqual(response.context["disciple_count"], 2)

    def test_religion_list_view_status_code(self):
        url = reverse("religious_atlas:religion_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_religion_list_view_template(self):
        url = reverse("religious_atlas:religion_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "religious_atlas/religion_list.html")

    def test_religion_list_view_context(self):
        url = reverse("religious_atlas:religion_list")
        response = self.client.get(url)
        self.assertTrue("religions" in response.context)
        self.assertEqual(len(response.context["religions"]), 2)
        self.assertContains(response, "Religion Alpha")
        self.assertContains(response, "Religion Beta")
        self.assertEqual(response.context["paginator"].count, 2)

    def test_religion_list_search(self):
        url = reverse("religious_atlas:religion_list") + "?q=Alpha"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Religion Alpha")
        self.assertNotContains(response, "Religion Beta")
        self.assertEqual(len(response.context["religions"]), 1)
        self.assertEqual(response.context["search_query"], "Alpha")
        self.assertEqual(response.context["paginator"].count, 1)

    def test_religion_detail_view_status_code(self):
        url = reverse(
            "religious_atlas:religion_detail", args=[self.religion1.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_religion_detail_view_template(self):
        url = reverse(
            "religious_atlas:religion_detail", args=[self.religion1.pk]
        )
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "religious_atlas/religion_detail.html"
        )

    def test_religion_detail_view_context(self):
        url = reverse(
            "religious_atlas:religion_detail", args=[self.religion1.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.context["religion"], self.religion1)
        self.assertContains(response, "Desc Alpha")
        self.assertTrue("related_churches" in response.context)
        self.assertEqual(response.context["related_churches"].count(), 1)
        self.assertEqual(
            response.context["related_churches"].first(), self.church1
        )

    def test_religion_create_view_get_unauthenticated(self):
        url = reverse("religious_atlas:religion_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        login_url = reverse("login")
        expected_redirect_url = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect_url)

    def test_religion_create_view_get_authenticated(self):
        self.client.login(username="regularuser", password="password123")
        url = reverse("religious_atlas:religion_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "religious_atlas/religion_form.html"
        )
        self.assertIsInstance(response.context["form"], ReligionForm)

    def test_religion_create_view_post(self):
        self.client.login(username="regularuser", password="password123")
        religion_count_before = Religion.objects.count()
        url = reverse("religious_atlas:religion_add")
        response = self.client.post(
            url,
            {
                "name": "Religion Gamma",
                "description": "Desc Gamma",
                "founded_date": "2024-01-01",
            },
        )
        redirect_url = reverse("religious_atlas:religion_list")
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.assertEqual(Religion.objects.count(), religion_count_before + 1)
        self.assertTrue(Religion.objects.filter(name="Religion Gamma").exists())

    def test_religion_update_view_post(self):
        self.client.login(username="regularuser", password="password123")
        url = reverse(
            "religious_atlas:religion_edit", args=[self.religion1.pk]
        )
        response = self.client.post(
            url,
            {
                "name": "Religion Alpha Updated",
                "description": self.religion1.description,
                "founded_date": self.religion1.founded_date or "2000-01-01",
            },
        )
        redirect_url = reverse("religious_atlas:religion_list")
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.religion1.refresh_from_db()
        self.assertEqual(self.religion1.name, "Religion Alpha Updated")

    def test_pastor_delete_permission(self):
        pastor_to_delete = User.objects.create_user(
            username=f"temp_pastor_del_{uuid.uuid4().hex[:8]}",
            password="password123",
            first_name="Temp",
            last_name="Delete",
        )
        delete_url = reverse(
            "religious_atlas:pastor_delete", args=[pastor_to_delete.pk]
        )
        login_url = reverse("login")
        pastor_list_url = reverse("religious_atlas:pastor_list")

        self.client.logout()
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{login_url}?next={delete_url}",
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(User.objects.filter(pk=pastor_to_delete.pk).exists())

        self.client.logout()
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{login_url}?next={delete_url}",
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(User.objects.filter(pk=pastor_to_delete.pk).exists())

        self.client.login(username="regularuser", password="password123")
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, pastor_list_url, status_code=302, target_status_code=200
        )
        self.assertFalse(User.objects.filter(pk=pastor_to_delete.pk).exists())

        pastor_to_delete_staff = User.objects.create_user(
            username=f"temp_pastor_staff_{uuid.uuid4().hex[:8]}",
            password="password123",
            first_name="TempStaff",
            last_name="DeleteStaff",
        )
        delete_url_staff = reverse(
            "religious_atlas:pastor_delete", args=[pastor_to_delete_staff.pk]
        )

        self.client.login(username="staffuser", password="password123")
        response = self.client.post(delete_url_staff)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, pastor_list_url, status_code=302, target_status_code=200
        )
        self.assertFalse(
            User.objects.filter(pk=pastor_to_delete_staff.pk).exists()
        )

    def test_pastor_list_excludes_superuser(self):
        superuser = User.objects.create_superuser(
            "admin_superuser_test", "admin_test@example.com", "password123"
        )
        url = reverse("religious_atlas:pastor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["pastors"]), 2)
        self.assertEqual(response.context["paginator"].count, 6)

        self.assertNotContains(response, superuser.username)
        self.assertNotContains(response, str(superuser))

    def test_registration_view_post_get(self):
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertIsInstance(response.context["form"], RegistrationForm)

    def test_church_list_view(self):
        url = reverse("religious_atlas:church_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/church_list.html")
        self.assertTrue("churches" in response.context)
        self.assertEqual(len(response.context["churches"]), 2)
        self.assertEqual(response.context["paginator"].count, 2)
        self.assertContains(response, "Church Alpha")
        self.assertContains(response, "Church Beta")

    def test_church_list_search(self):
        url = reverse("religious_atlas:church_list") + "?q=Alpha"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Church Alpha")
        self.assertNotContains(response, "Church Beta")
        self.assertEqual(len(response.context["churches"]), 1)
        self.assertEqual(response.context["search_query"], "Alpha")
        self.assertEqual(response.context["paginator"].count, 1)

        url = reverse("religious_atlas:church_list") + "?q=Beta"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Church Alpha")
        self.assertContains(response, "Church Beta")
        self.assertEqual(len(response.context["churches"]), 1)
        self.assertEqual(response.context["search_query"], "Beta")
        self.assertEqual(response.context["paginator"].count, 1)

    def test_pastor_list_view(self):
        url = reverse("religious_atlas:pastor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/pastor_list.html")
        self.assertTrue("pastors" in response.context)
        self.assertEqual(len(response.context["pastors"]), 2)
        self.assertEqual(response.context["paginator"].count, 6)

    def test_pastor_list_search(self):
        url = reverse("religious_atlas:pastor_list") + "?q=Pastor"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["paginator"].count, 4)

        self.assertEqual(len(response.context["pastors"]), 2)

        self.assertContains(response, "Pastor Four")
        self.assertContains(response, "Test Pastor Del")
        self.assertNotContains(response, "Pastor Three")
        self.assertNotContains(response, "Pastor Two")
        self.assertEqual(response.context["search_query"], "Pastor")

        url_page2 = reverse("religious_atlas:pastor_list") + "?q=Pastor&page=2"
        response_page2 = self.client.get(url_page2)
        self.assertEqual(response_page2.status_code, 200)
        self.assertEqual(len(response_page2.context["pastors"]), 2)
        self.assertContains(response_page2, "Pastor Three")
        self.assertContains(response_page2, "Pastor Two")
        self.assertNotContains(response_page2, "Pastor Four")
        self.assertNotContains(response_page2, "Test Pastor Del")

    def test_disciple_list_view(self):
        url = reverse("religious_atlas:disciple_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/disciple_list.html")
        self.assertTrue("disciples" in response.context)
        self.assertEqual(len(response.context["disciples"]), 2)
        self.assertEqual(response.context["paginator"].count, 2)
        self.assertContains(response, "Disc One")
        self.assertContains(response, "Disc Two")

    def test_disciple_list_search(self):
        url = reverse("religious_atlas:disciple_list") + "?q=One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disc One")
        self.assertNotContains(response, "Disc Two")
        self.assertEqual(len(response.context["disciples"]), 1)
        self.assertEqual(response.context["search_query"], "One")
        self.assertEqual(response.context["paginator"].count, 1)

        url = reverse("religious_atlas:disciple_list") + "?q=Two"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Disc One")
        self.assertContains(response, "Disc Two")
        self.assertEqual(len(response.context["disciples"]), 1)
        self.assertEqual(response.context["search_query"], "Two")
        self.assertEqual(response.context["paginator"].count, 1)

        url = reverse("religious_atlas:disciple_list") + "?q=Disc"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disc One")
        self.assertContains(response, "Disc Two")
        self.assertEqual(len(response.context["disciples"]), 2)
        self.assertEqual(response.context["search_query"], "Disc")
        self.assertEqual(response.context["paginator"].count, 2)

        url = reverse("religious_atlas:disciple_list") + "?q=Church Alpha"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disc One")
        self.assertNotContains(response, "Disc Two")
        self.assertEqual(len(response.context["disciples"]), 1)
        self.assertEqual(response.context["search_query"], "Church Alpha")
        self.assertEqual(response.context["paginator"].count, 1)

        url = reverse("religious_atlas:disciple_list") + "?q=pastor2_usr"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Disc One")
        self.assertContains(response, "Disc Two")
        self.assertEqual(len(response.context["disciples"]), 1)
        self.assertEqual(response.context["search_query"], "pastor2_usr")
        self.assertEqual(response.context["paginator"].count, 1)

    def test_church_detail_view(self):
        url = reverse("religious_atlas:church_detail", args=[self.church1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/church_detail.html")
        self.assertEqual(response.context["church"], self.church1)
        self.assertTrue("related_pastors" in response.context)
        pastor_serving = User.objects.create_user(
            username="pastor_serving",
            password="password123",
            first_name="Serving",
            last_name="PastorServing",
        )
        pastor_serving.serving_in_churches.add(self.church1)
        response = self.client.get(url)
        self.assertEqual(response.context["related_pastors"].count(), 1)
        self.assertEqual(
            response.context["related_pastors"].first(), pastor_serving
        )

    def test_pastor_detail_view(self):
        url = reverse(
            "religious_atlas:pastor_detail", args=[self.test_pastor_del.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/pastor_detail.html")
        self.assertEqual(response.context["pastor"], self.test_pastor_del)
        self.assertTrue("serving_churches" in response.context)
        self.assertTrue("mentors" in response.context)
        self.assertEqual(response.context["mentors"].count(), 1)
        self.assertEqual(response.context["mentors"].first(), self.disciple1)

    def test_pastor_update_view_get_authenticated(self):
        self.client.login(username="regularuser", password="password123")
        url = reverse(
            "religious_atlas:pastor_edit", args=[self.regular_user.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/generic_form.html")
        self.assertIsInstance(response.context["form"], PastorUpdateForm)
        self.assertEqual(
            response.context["view_title"],
            f"Edit profile: {self.regular_user.get_full_name()}",
        )

    def test_pastor_update_view_post_authenticated(self):
        self.client.login(username="regularuser", password="password123")
        url = reverse(
            "religious_atlas:pastor_edit", args=[self.regular_user.pk]
        )
        new_first_name = "Updated"
        response = self.client.post(
            url,
            {
                "username": self.regular_user.username,
                "email": self.regular_user.email,
                "first_name": new_first_name,
                "last_name": self.regular_user.last_name,
                "religion": (
                    self.regular_user.religion.pk
                    if self.regular_user.religion
                    else ""
                ),
                "serving_in_churches": [
                    church.pk for church in
                    self.regular_user.serving_in_churches.all()
                ],
            },
        )
        redirect_url = reverse(
            "religious_atlas:pastor_detail", args=[self.regular_user.pk]
        )
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.first_name, new_first_name)

    def test_disciple_create_view_get_authenticated(self):
        self.client.login(username="regularuser", password="password123")
        url = reverse("religious_atlas:disciple_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "religious_atlas/generic_form.html")
        self.assertIsInstance(response.context["form"], DiscipleForm)
        self.assertEqual(response.context["view_title"], "Add new disciple")

    def test_disciple_create_view_post_authenticated(self):
        self.client.login(username="regularuser", password="password123")
        disciple_count_before = Disciple.objects.count()
        url = reverse("religious_atlas:disciple_add")
        response = self.client.post(
            url,
            {
                "first_name": "New",
                "last_name": "Disciple",
                "email": "new_disciple@example.com",
                "church": self.church1.pk,
                "mentor_pastor": self.test_pastor_del.pk,
            },
        )
        redirect_url = reverse("religious_atlas:disciple_list")
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.assertEqual(Disciple.objects.count(), disciple_count_before + 1)
        self.assertTrue(
            Disciple.objects.filter(email="new_disciple@example.com").exists()
        )

    def test_disciple_update_view_post_authenticated(self):
        self.client.login(username="regularuser", password="password123")
        url = reverse(
            "religious_atlas:disciple_edit", args=[self.disciple1.pk]
        )
        new_last_name = "One Updated"
        response = self.client.post(
            url,
            {
                "first_name": self.disciple1.first_name,
                "last_name": new_last_name,
                "email": self.disciple1.email,
                "church": self.disciple1.church.pk,
                "mentor_pastor": self.disciple1.mentor_pastor.pk,
            },
        )
        redirect_url = reverse("religious_atlas:disciple_list")
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.disciple1.refresh_from_db()
        self.assertEqual(self.disciple1.last_name, new_last_name)

    def test_disciple_delete_view_post_authenticated(self):
        disciple_to_delete = Disciple.objects.create(
            first_name="Temp",
            last_name="DeleteDisc",
            church=self.church1,
            email="tempdelete@example.com",
        )
        url = reverse(
            "religious_atlas:disciple_delete", args=[disciple_to_delete.pk]
        )
        disciple_list_url = reverse("religious_atlas:disciple_list")

        self.client.login(username="regularuser", password="password123")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, disciple_list_url, status_code=302, target_status_code=200
        )
        self.assertFalse(
            Disciple.objects.filter(pk=disciple_to_delete.pk).exists()
        )

    def test_church_create_view_login_required(self):
        url = reverse("religious_atlas:church_add")
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url, {})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")

    def test_church_update_view_login_required(self):
        url = reverse("religious_atlas:church_edit", args=[self.church1.pk])
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url, {})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")

    def test_church_delete_view_login_required(self):
        url = reverse("religious_atlas:church_delete", args=[self.church1.pk])
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url)
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")

    def test_pastor_update_view_login_required(self):
        url = reverse(
            "religious_atlas:pastor_edit", args=[self.test_pastor_del.pk]
        )
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url, {})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")

    def test_disciple_create_view_login_required(self):
        url = reverse("religious_atlas:disciple_add")
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url, {})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")

    def test_disciple_update_view_login_required(self):
        url = reverse(
            "religious_atlas:disciple_edit", args=[self.disciple1.pk]
        )
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url, {})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")

    def test_disciple_delete_view_login_required(self):
        url = reverse(
            "religious_atlas:disciple_delete", args=[self.disciple1.pk]
        )
        self.client.logout()
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)
        login_url = reverse("login")
        self.assertRedirects(response_get, f"{login_url}?next={url}")

        response_post = self.client.post(url)
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, f"{login_url}?next={url}")
