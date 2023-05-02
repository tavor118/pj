from django.contrib.auth import get_user_model
from pytest import fixture
from rest_framework.test import APIClient

from src.apps.questions.models import Question
from src.apps.social.models import Note

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestNoteViewSet:
    list_url = "/api/questions/notes/"
    detail_url = "/api/questions/notes/{}/"


class TestListNoteView(TestNoteViewSet):
    def test_list_notes(
        self, client: APIClient, user: User, note: Note, django_assert_num_queries
    ):
        with django_assert_num_queries(0):
            response = client.get(self.list_url)

        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        # 2 queries - count, select
        with django_assert_num_queries(2):
            response = client.get(self.list_url)

        assert response.status_code == 200, response.data

        assert response.data["count"] == 1
        result = response.data["results"][0]
        assert result["id"] == note.id
        assert result["content"] == note.content


class TestDetailNoteView(TestNoteViewSet):
    def test_details_note(self, client: APIClient, user: User, note: Note):
        url = self.detail_url.format(note.pk)
        response = client.get(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.get(url)

        assert response.status_code == 200, response.data

        result = response.data
        assert result["id"] == note.id
        assert result["content"] == note.content


class TestCreateNoteView(TestNoteViewSet):
    def test_create_note(self, client: APIClient, user: User, question: Question):
        content = "test note"
        data = {"content": content, "question": question.id}

        response = client.post(self.list_url, data=data)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.post(self.list_url, data=data)

        assert response.status_code == 201, response.data

        [note] = Note.objects.all()

        result = response.data
        assert result["id"] == note.id
        assert result["content"] == content


class TestUpdateNoteView(TestNoteViewSet):
    def test_update_note(
        self, client: APIClient, user: User, question: Question, note: Note
    ):
        url = self.detail_url.format(note.pk)

        content = "test note"
        data = {"content": content, "question": question.id}

        response = client.put(url, data=data)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.put(url, data=data)

        assert response.status_code == 200, response.data

        result = response.data
        assert result["id"] == note.id
        assert result["content"] == content


class TestDeleteNoteView(TestNoteViewSet):
    def test_delete_note(self, client: APIClient, user: User, note: Note):
        url = self.detail_url.format(note.pk)
        response = client.delete(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.delete(url)

        assert response.status_code == 204, response.data

        note_count = Note.objects.count()
        assert note_count == 0
