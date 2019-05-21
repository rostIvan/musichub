from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse

from lessons.models import Lesson
from musichub.tests import APIAuthorizeUserTestCase

lesson_json = {
    'title': 'Hello world!!!',
    'text': 'Lorem ipsum...'
}
lesson_count = 10


class Test(APIAuthorizeUserTestCase):
    def setUp(self):
        mixer.cycle(lesson_count).blend(Lesson)

    def test_get_lessons(self):
        response = self.client.get(reverse('lessons-list'))
        self.assertEqual(response.data['count'], lesson_count)

    def test_get_lesson_by_id(self):
        lesson_id = 1
        response = self.client.get(reverse('lessons-detail',
                                           args=(lesson_id,)))
        lesson = Lesson.objects.get(id=lesson_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], lesson.title)
        self.assertEqual(response.data['text'], lesson.text)

    def test_post_lesson_unauthorized_user(self):
        response = self.client.post(reverse('lessons-list'), lesson_json)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), lesson_count)

    def test_post_lesson_authorized_user(self):
        self.create_and_auth(email='user@gmail.com', password='qwerty_1234')
        response = self.client.post(reverse('lessons-list'), lesson_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), lesson_count + 1)

    def test_put_lesson_unauthorized_user(self):
        response = self.client.put(reverse('lessons-detail', args=(1,)),
                                   lesson_json)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_lesson_authorized_not_owner_user(self):
        self.create_and_auth(email='user@gmail.com', password='qwerty_1234')
        response = self.client.put(reverse('lessons-detail', args=(1,)),
                                   lesson_json)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_lesson_authorized_owner_user(self):
        user = self.create_and_auth(email='user@gmail.com',
                                    password='qwerty_1234')
        lesson = Lesson.objects.create(user=user, title='Some title')
        patch_data = {'title': 'New updated title'}

        response = self.client.patch(
            reverse('lessons-detail', args=(lesson.id,)),
            patch_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patched_lesson = Lesson.objects.get(id=lesson.id)
        self.assertEqual(patched_lesson.title, patch_data['title'])
