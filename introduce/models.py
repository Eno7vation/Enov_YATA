import re

from django.conf import settings
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.db import models

from config.utils.image_save import rename_image_to_uuid_everything
from main.models import BaseModel


class Apply(BaseModel):
    class DepartmentChoices(models.TextChoices):
        Aeronautical_Science = "항공학부", "항공학부"
        Transdisciplinary_Aeronautical = "항공융합학부", "항공융합학부"
        Health_Science = "보건학부", "보건학부"
        Design_Media = "디자인학부", "디자인학부"

    class MajorChoices(models.TextChoices):
        Frontend = "프론트엔드(웹 디자인)", "프론트엔드(웹 디자인)"
        Backend = "백엔드(DRF를 통한 API서버 구축 및 최적화)", "백엔드(DRF를 통한 API 구축 및 최적화)"
        App = "Application 개발", "Application"
        Design = "디자인(UI/UX)", "디자인(UI/UX)"
        AI = "AI", "인공지능(Computer Vison, Numerical Predict), 데이터과학(데이터 정제)"

    class Level(models.TextChoices):
        Low = "Juinor", "주니어 개발자"
        High = "Senior", "시니어 개발자"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Apply_post', on_delete=models.PROTECT)

    caption = models.TextField(help_text="　　• 자기소개와 실력을 적어주세요. <br/>"
                                                         "　　• ex) 필수양식: 학과_학번_이름_나이")
    phone_number = models.CharField(max_length=15, blank=True,
                                    validators=[RegexValidator(r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})')],
                                    help_text='　　• 010-1234-5678 또는 0101234567의 형태로 입력해주세요')

    grade = models.FileField(blank=True, null=True,
                              help_text='<b><span style="background-color: #FFFFFF; color: #FF0000;">　　• 한서포탈 -> 교육통합정보시스템 -> 전체성적 조회 -> 성적 확인서')

    campus = models.CharField(max_length=50, blank=True, choices=DepartmentChoices.choices)

    apply_part = models.CharField(max_length=50, blank=True, choices=MajorChoices.choices,
                                  help_text='　　• 지원하고싶은 분야를 선택해주세요!')

    level = models.CharField(max_length=50, blank=True, choices=Level.choices,
                             help_text='　　• 레벨을 선택해주세요!')

    def __str__(self):
        return f"{self.author}의 지원 : {self.apply_part}"
    def save(self, *args, **kwargs):
        cache.delete('apply')
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        cache.delete('apply')
        super().delete(self, *args, **kwargs)


class DriverApply(BaseModel):
    class DepartmentChoices(models.TextChoices):
        Aeronautical_Science = "항공학부", "항공학부"
        Transdisciplinary_Aeronautical = "항공융합학부", "항공융합학부"
        Health_Science = "보건학부", "보건학부"
        Design_Media = "디자인학부", "디자인학부"
        Sport_Sciences = "스포츠학부", "스포츠학부"
        Liberal_Arts = "융합교양학부", "융합교양학부"

    class Choices(models.TextChoices):
        Driver = "Driver", "운전자"
        User = "User", "사용자"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='DriveApply_post', on_delete=models.PROTECT)

    caption = models.TextField(help_text='<b><span style="background-color: #FFFFFF; color: #FF0000;">　　• ex) 필수양식: 학과_학번_이름_나이_운전기간_주에 카풀을 이용하는 횟수(1주 3번 -> 1/3)')

    phone_number = models.CharField(max_length=15, blank=True,
                                    validators=[RegexValidator(r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})')],
                                    help_text='　　• 010-1234-5678 또는 0101234567의 형태로 입력해주세요')

    campus = models.CharField(max_length=50, blank=True, choices=DepartmentChoices.choices)

    apply_part = models.CharField(max_length=50, blank=True, choices=Choices.choices,
                                  help_text='　　• 지원하고싶은 분야를 선택해주세요!')
    driver_license = models.ImageField(help_text='<b><span style="background-color: #FFFFFF; color: #FF0000;">　　• 개인정보를 가려서 올려주세요!, 사용자의 경우 학생증을 올려주세요',
                                       upload_to=rename_image_to_uuid_everything)

    file = models.FileField(help_text='<b><span style="background-color: #FFFFFF; color: #FF0000;">　　• 티맵 좌측상단 메뉴 -> 카라이프 -> 운전점수 첨부',
                            upload_to=rename_image_to_uuid_everything)

    def __str__(self):

        return f"{self.author}의 지원 : {self.apply_part}"

    class Meta:
        ordering = ['-id']

class Level(BaseModel):
    level = models.IntegerField(default=13)

    def __str__(self):
        return f"{self.level}"
