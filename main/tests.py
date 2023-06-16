from django.test import TestCase
from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model

from .models import Post, user_reservation
from datetime import datetime, time, date

class UserReservationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Users = get_user_model()
        test_user = Users.objects.create(username="testuser")
        test_post = Post.objects.create(
            date=datetime.today().date(),
            time=datetime.today().time(),
            money=10000,
            address_kakao_start="서울시 강남구 역삼동",
            address_kakao_end="서울시 강남구 신사동",
            user_limit=4,
            car_user=test_user,
        )
        user_reservation.objects.create(
            user=test_user,
            address_kakao_start="서울시 강남구 역삼동",
            address_kakao_end="서울시 강남구 신사동",
            reservation_date=datetime.today().date(),
            min_money=8000,
            max_money=12000,
            max_time=datetime.now().time(),
            min_time=datetime.now().time(),
        )

    def test_user_label(self):
        user_reservation_obj = user_reservation.objects.get(id=1)
        field_label = user_reservation_obj._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "user")

    def test_reservation_date(self):
        user_reservation_obj = user_reservation.objects.get(id=1)
        reservation_date = user_reservation_obj.reservation_date
        self.assertEquals(reservation_date, datetime.today().date())

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트에 필요한 객체 생성
        Users = get_user_model()
        user = Users.objects.create(username='test_user')
        Post.objects.create(
            date=date.today(),
            time=time(14, 30),
            money=5000,
            car_num='12가3456',
            start_region='홍대역',
            end_region = '한서대',
            start_detail='출발지 상세',
            end_detail='도착지 상세',
            address_kakao_start='출발지',
            address_kakao_end='도착지',
            car_user=user,
            user_limit=3,
            user_num=2,
            post_premium=True
        )

    def test_date_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    # def test_money_max_digits(self):
    #     post = Post.objects.get(id=1)
    #     max_digits = post._meta.get_field('money').max_digits
    #     self.assertEqual(max_digits, 6)

    def test_car_num_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('car_num').max_length
        self.assertEqual(max_length, 200)

    def test_user_limit_default(self):
        post = Post.objects.get(id=1)
        user_limit = post._meta.get_field('user_limit').default
        self.assertEqual(user_limit, 0)

    def test_post_premium_default(self):
        post = Post.objects.get(id=1)
        post_premium = post._meta.get_field('post_premium').default
        self.assertFalse(post_premium)