from http import HTTPStatus

from django.test import Client, TestCase

from about.tests import test_constants as const


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URLs, генерируемые при помощи имен about, доступны."""
        url_names = (const.ABOUT_AUTHOR_URL, const.ABOUT_TECH_URL)
        for url in url_names:
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_pages_names = {
            const.ABOUT_AUTHOR_URL: const.ABOUT_AUTHOR_TEMPLATE,
            const.ABOUT_TECH_URL: const.ABOUT_TECH_TEMPLATE,
        }
        for url, template in templates_pages_names.items():
            response = self.guest_client.get(url)
            self.assertTemplateUsed(response, template)
