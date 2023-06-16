from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Users
from .models import Profile, Category, Comment, Activity, Tag, Post, Bug


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = Users.objects.create_user(
            username='Test_User', email='test_user@example.com', password='password', name='Test_User', first_name='Test_User')
        self.profile = Profile.objects.create(
            author=self.user,
            avatar='path/to/image',
            name='Test_User',
            job=['Frontend', 'Design'],
            text='Some text here'
        )

    def test_str_representation(self):
        self.assertEqual(str(self.profile), f"{self.user} : {self.profile.name}, {self.profile.job}")

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Frontend')

    def test_str_representation(self):
        self.assertEqual(str(self.category), self.category.name)

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create_user(
            username='Test_User', email='test_user@example.com', password='password', name='Test_User',
            first_name='Test_User')
        self.post = Post.objects.create(
            title='Test Post', author=self.user, caption='Test Content')
        self.comment = Comment.objects.create(
            author=self.user, post=self.post, message='This is a test comment')
        self.users = [self.user]

    def test_comment_model(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.message, 'This is a test comment')

class Activity_Tag_ModelTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create_user(
            username='Test_User', email='test_user@example.com', password='password', name='Test_User',
            first_name='Test_User')
        self.activity = Activity.objects.create(
            author=self.user,
            name='Test activity'
        )
        self.tag = Tag.objects.create(
            name='Test tag'
        )

    def test_activity_model(self):
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.author, self.user)
        self.assertEqual(activity.name, 'Test activity')

    def test_tag_model(self):
        tag = Tag.objects.get(id=1)
        self.assertEqual(tag.name, 'Test tag')

class BugModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Users.objects.create_user(
            username='Test_User', email='test_user@example.com', password='password', name='Test_User',
            first_name='Test_User')

        cls.bug = Bug.objects.create(
            author=cls.user,
            title='Test Bug',
            description='This is a test bug',
            category='ETC',
            status='None',
            bug_rock=0
        )

    def test_str_method(self):
        expected_output = '😥해결이 되지 않은 버그입니다. 제보시간으로부터 0일 0시간이 지났습니다.😥'
        self.assertEqual(str(self.bug), expected_output)

    def test_bug_rock_subtract(self):
        self.bug.status = 'Solve'
        self.bug.bug_rock = 1
        self.bug.save()
        self.assertEqual(self.bug.bug_rock, 0)