import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from multiselectfield import MultiSelectField

from config.utils.image_save import rename_image_to_uuid_everything
from config.utils.validators import validate_image_extension


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(models.Model):

    Job = (
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Devops', 'Devops'),
        ('PM', 'PM'),
        ('Design', 'Design'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_profile_set',
                               on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)
    name = models.CharField(max_length=100)
    job = MultiSelectField(choices=Job)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.author} : {self.name}, {self.job}"


class Category(models.Model):
    Categorys = (
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Devops', 'Devops'),
        ('Notice', 'Notice'),
        ('Patch', 'Patch'),
    )
    name = models.CharField(max_length=20, choices=Categorys,unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('instagram:detail', args=[self.name])

class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    photo = models.ImageField(blank=True)
    main = models.CharField(max_length=1000)
    caption = models.CharField(max_length=100000)

    CATEGORY_CHOICES = Category.Categorys
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


    tag_set = models.ManyToManyField('Tag', blank=True)
    view_count = models.IntegerField(default=0)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name='like_post_set')

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("tech:post_detail", args=[self.pk])

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ['-id']


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']

class Activity(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def clean(self):
        if len(self.name) > 10:
            raise ValidationError('Name must be less than or equal to 10 characters.')

    class Meta:
        ordering = ['-id']



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Bug(BaseModel):

    Status = (
        ('None', 'None'),
        ('Progress', 'Progress'),
        ('Solve', 'Solve'),
        ('Impossible', 'Impossible'),
    )

    Select = (
        ('Account_Page', '계정페이지'),
        ('Main_Page', '카풀페이지'),
        ('Tech_Page', '테크블로그 페이지'),
        ('Security', '보안 관련(최우선 할당)'),
        ('ETC', '그 외...'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, help_text="사진은 하나만 첨부가능합니다.", validators=[validate_image_extension],
                              max_length=1000, upload_to=rename_image_to_uuid_everything)
    category = models.CharField(choices=Select, blank=True, max_length=100,
                                help_text='<span style="color:red;font-weight:bold;">보안 관련 문제는 최우선으로 개발자에게 할당됩니다. <br> 또한, 매우 심각한 버그를 제보해주실 경우 리워드를 지급해드리겠습니다.</span>')
    description = models.TextField(help_text='<span style="color:red;font-weight:bold;">한번 제보된 버그는 수정과 삭제가 불가능합니다. <br> 신중히 제보해주세요!</span>')
    status = models.CharField(choices=Status, default='None',max_length=100)
    bug_rock = models.IntegerField(default=0)


    class Meta:
        verbose_name_plural = "bugs"
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if 'Solve' in self.status and self.bug_rock > 0:
            self.bug_rock -= 1
        super().save(*args, **kwargs)



    def __str__(self):
        now = timezone.now()
        time = now - self.created_at

        time_days = time.days
        time_hours = time.seconds // 3600

        if "None" in self.status:
            return f"😥해결이 되지 않은 버그입니다. 제보시간으로부터 {time_days}일 {time_hours}시간이 지났습니다.😥"
            if self.category == "Security":
                return "test"
        elif "Progress" in self.status:
            return f"😰해결이 진행 중인 버그입니다. 제보시간으로부터 {time_days}일 {time_hours}시간이 지났습니다.😰"
        elif "Solve" in self.status:
            return f"🥳해결이 된 버그입니다. 제보시간으로부터 {time_days}일 {time_hours}시간이 지났습니다.🥳"
        else:
            return f"🤦🏻‍해결이 불가능한 버그입니다. 제보시간으로부터 {time_days}일 {time_hours}시간이 지났습니다.🤦🏻‍"





