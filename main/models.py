from django.db import models
from accounts.models import Users
from config.utils.validators import MinValueValidator, MaxValueValidator


class BaseModel(models.Model):
    modify_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Post(BaseModel): # @수정
    date = models.DateField() # 예약 시간
    time = models.TimeField() # 예약 시간
    money = models.IntegerField(default=0)  # 카풀 금액
    car_num = models.CharField(max_length=200, blank=True)
    end_region = models.CharField(max_length=50, blank=True)  # 지역 @수정
    start_region = models.CharField(max_length=50, blank=True)  # 지역 @수정
    start_detail = models.CharField(max_length=200, blank=True) # 카카오 맵 출발지 세부 주소
    end_detail = models.CharField(max_length=200, blank=True) # 카카오 맵 도착지 세부 주소
    address_kakao_start = models.CharField(max_length=200) # 시작 장소
    address_kakao_end = models.CharField(max_length=200) # 도착 장소
    car_user = models.ForeignKey(Users,   # 차주
                               on_delete=models.CASCADE,
                               related_name="car_pool_user",
                               null=True, blank=True)
    users = models.ManyToManyField(Users, # 이용자
                                  blank=True,
                                  related_name="users")
    Done = models.BooleanField(default=False, db_index=True) # 예약 유저 만석 True
    user_limit = models.IntegerField(default=0) # 유저 인원 제한설정
    user_num = models.IntegerField(default=0) #예약 유저 인원
    clear = models.BooleanField(default=False, db_index=True) # 게시글 이행 완료
    remove = models.BooleanField(default=False, db_index=True) # 게시글 삭제 True
    post_premium = models.BooleanField(default=False) # 게시글 프리미엄 여부 @ 수정
    gender = models.CharField(max_length=10, blank=True) # 게시글 성별 @ 수정



class user_reservation(BaseModel): # 검색 겸 예약 유저
    user = models.ForeignKey(Users,   # 예약 유저
                               on_delete=models.CASCADE,
                               null=True, blank=True)
    address_kakao_start = models.CharField(max_length=200)  # 시작 장소
    address_kakao_end = models.CharField(max_length=200)  # 도착 장소
    end_region = models.CharField(max_length=50, blank=True)  # 지역 @수정
    start_region = models.CharField(max_length=50, blank=True)  # 지역 @수정
    start_detail = models.CharField(max_length=200, blank=True)  # 카카오 맵 출발지 세부 주소
    end_detail = models.CharField(max_length=200, blank=True)  # 카카오 맵 도착지 세부 주소
    reservation_date = models.DateField() #예약 날짜
    min_money = models.IntegerField(default=0)  # 카풀 최저 금액
    max_money = models.IntegerField(default=0)  # 카풀 최대 금액
    max_time = models.TimeField()  # 예약 최대 시간
    min_time = models.TimeField()  # 예약 최소 시간
    remove = models.BooleanField(default=False, db_index=True)  # 게시글 삭제 True
    comment_user = models.ManyToManyField(Post,
                                          blank=True, related_name="comment_user")

class Road(BaseModel):
    user = models.ForeignKey(Users,
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    road = models.CharField(max_length=500, default="로그인")
    road_num = models.IntegerField(default=0)
    road_check = models.BooleanField(default=False)

class Level(models.Model):  # @ 수정
    level_num = models.DecimalField(default=0, max_digits=4, decimal_places=1)