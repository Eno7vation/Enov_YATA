from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser

from config.utils.image_save import rename_image_to_uuid_accounts, rename_image_to_uuid_license
from config.utils.validators import validate_image_extension


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, first_name, password, username, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, first_name, password, username, **other_fields)

    def create_user(self, email, name, first_name, password, username, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, username=username,
                          first_name = first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Users(AbstractBaseUser, PermissionsMixin):  # @수정
    email = models.EmailField(_('이메일'), unique=True)
    name = models.CharField(max_length=150, blank=True)
    start = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=180)
    first_name = models.CharField(max_length=180, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    friends = models.ManyToManyField("self", blank=True)
    car = models.BooleanField(default=False)
    post_num = models.IntegerField(default=0)
    post_limit = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, blank=True)
    car_num = models.CharField(validators=
                               [RegexValidator(regex=r'^\d{1,3}[가-힣]{1}\d{4}$', message="'123가1234 또는 12가 1234와 같은 형태로 입력해주세요.'")],
                               max_length=200, blank=True)  # 차 번호
    major = models.CharField(max_length=20, blank=True)
    premium = models.BooleanField(default=False) # @ 수정 프리미엄
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)' ),)
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS, blank=True)
    license_img = models.ImageField(blank=True, upload_to=rename_image_to_uuid_license, null=True,
                                    validators=[validate_image_extension])
    phone_num = models.CharField(validators=
                                 [RegexValidator(regex=r'^010-?\d{4}-?\d{4}$', message="'010-1234-5678' 또는 '01012345678'의 형태로 입력해주세요.")],
                                 max_length=13, blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to=rename_image_to_uuid_accounts,
                               validators=[validate_image_extension])




    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'first_name', 'username']

    def __str__(self):
        if self.nickname == '':
            return self.email
        else:
            return self.nickname


class Suspension(models.Model):

    # Categorys = (
    #     ('Suspension', 'Suspension'),
    #     ('Backend', 'Backend'),
    # )
    # name = models.CharField(max_length=20, choices=Categorys, unique=True)

    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    period = models.DateTimeField()
    caption = models.TextField()

    def status_period(self):
        time= timezone.now()
        if self.status == True:
            period = self.period - time
        return period

    class Meta:
        ordering = ['-id']