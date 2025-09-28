from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Tests for Book endpoints:
    - CRUD operations
    - Filtering, searching, ordering
    - Permission enforcement for write endpoints
    """

    def setUp(self):
        self.client = APIClient()
        # Users
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Authors
        self.author_rowling = Author.objects.create(name="J.K. Rowling")
        self.author_orwell = Author.objects.create(name="George Orwell")

        # Books
        self.book_hp1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author_rowling,
        )
        self.book_hp2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author_rowling,
        )
        self.book_1984 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author_orwell,
        )

        self.book_list_url = reverse("book-list")
        self.book_detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.book_create_url = reverse("book-create")
        self.book_update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.book_delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})

    # Read operations
    def test_list_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book(self):
        response = self.client.get(self.book_detail_url(self.book_hp1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book_hp1.title)

    # Create (permission required)
    def test_create_book_requires_authentication(self):
        payload = {
            "title": "The Hobbit",
            "publication_year": 1937,
            "author": self.author_rowling.id,
        }
        response = self.client.post(self.book_create_url, payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        payload = {
            "title": "The Hobbit",
            "publication_year": 1937,
            "author": self.author_rowling.id,
        }
        response = self.client.post(self.book_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    # Update (permission required)
    def test_update_book_requires_authentication(self):
        payload = {"title": "Harry Potter and the Philosopher's Stone (Updated)"}
        response = self.client.patch(self.book_update_url(self.book_hp1.id), payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        payload = {"title": "Harry Potter and the Sorcerer's Stone"}
        response = self.client.patch(self.book_update_url(self.book_hp1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_hp1.refresh_from_db()
        self.assertEqual(self.book_hp1.title, "Harry Potter and the Sorcerer's Stone")

    # Delete (permission required)
    def test_delete_book_requires_authentication(self):
        response = self.client.delete(self.book_delete_url(self.book_hp2.id))
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.book_delete_url(self.book_hp2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book_hp2.id).exists())

    # Filtering
    def test_filter_by_title(self):
        response = self.client.get(self.book_list_url + "?title=1984")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_filter_by_author(self):
        response = self.client.get(self.book_list_url + f"?author={self.author_rowling.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_publication_year(self):
        response = self.client.get(self.book_list_url + "?publication_year=1997")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book_hp1.title)

    # Search
    def test_search_by_title(self):
        response = self.client.get(self.book_list_url + "?search=Harry%20Potter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_by_author_name(self):
        response = self.client.get(self.book_list_url + "?search=Orwell")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    # Ordering
    def test_ordering_by_title(self):
        response = self.client.get(self.book_list_url + "?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(self.book_list_url + "?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))


