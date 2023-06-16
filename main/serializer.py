from rest_framework import serializers
from main.models import Post, user_reservation
from accounts.models import Users
from rest_framework.exceptions import ValidationError

class Account_check(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('nickname', 'car', 'car_num', 'gender', 'phone_num')

    def validate(self, data):
        nick = Users.objects.filter(nickname=data['nickname']).exists()
        if nick == True:
            raise ValidationError("닉네임 중복")
        else:
            return data

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.car = validated_data.get('car', instance.car)
        instance.car_num = validated_data.get('car_num', instance.car_num)
        instance.phone_num = validated_data.get('phone_num', instance.phone_num)
        instance.gender = 'M' # html에서 값을 가져올 수 있으면 수정 예정
        instance.save()
        return instance

class Post_check(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def validate(self, data):
        user = self.context.get("request").user
        users = Users.objects.get(nickname=user)
        if self.context.get("Revise") == 1:
            return data
        if users.post_limit == False:
            return data
        else:
            raise ValidationError("예약 게시판은 2개이상 만들 수 없습니다.")

    def create(self, validated_data):  # @수정 완
        user = self.context.get("request").user
        users = Users.objects.get(nickname=user)
        num = int(users.post_num)
        car_number = users.car_num
        gender_ckeck = users.gender
        end_region_check = validated_data['address_kakao_end'].split() # @수정 완
        start_region_check = validated_data['address_kakao_start'].split()
        users.post_num = num + 1
        if users.post_num == 2:
            users.post_limit = True
        users.save()
        bool = Post.objects.create(money=validated_data['money'],
                                   car_user=user,
                                   car_num=car_number,
                                   gender=gender_ckeck,
                                   start_detail=validated_data['start_detail'],
                                   end_detail=validated_data['end_detail'],
                                   time=validated_data["time"],
                                   date=validated_data['date'],
                                   end_region=end_region_check[0],
                                   start_region=start_region_check[0],
                                   address_kakao_start=validated_data['address_kakao_start'],
                                   address_kakao_end=validated_data['address_kakao_end'],
                                   user_limit=validated_data['user_limit'],
                                   post_premium=users.premium,   # @수정
                                       )
        bool.users.add(user)
        return bool

    def update(self, instance, validated_data): # @수정
        end_region_check = validated_data['address_kakao_end'].split()
        start_region_check = validated_data['address_kakao_start'].split()
        instance.start_detail = validated_data.get('start_detail', instance.start_detail)
        instance.end_detail = validated_data.get('end_detail', instance.end_detail)
        instance.time = validated_data.get('time', instance.time)
        instance.date = validated_data.get('date', instance.date)
        instance.end_region = end_region_check[0]
        instance.start_region = start_region_check[0]
        instance.address_kakao_start = validated_data.get('address_kakao_start', instance.address_kakao_start)
        instance.address_kakao_end = validated_data.get('address_kakao_end', instance.address_kakao_end)
        instance.money = validated_data.get('money', instance.money)
        instance.user_limit = validated_data.get('user_limit', instance.user_limit)
        instance.save()
        return instance


class user_reservation_check(serializers.ModelSerializer):
    class Meta:
        model = user_reservation
        fields = '__all__'

    def validate(self, data):
        return data

        raise ValidationError("Duplicated title.")

    def create(self, validated_data):
        request_user = self.context.get("request_user")
        end_region_check = validated_data['address_kakao_end'].split()  # @수정 완
        start_region_check = validated_data['address_kakao_start'].split()
        bool = user_reservation.objects.create(min_money=validated_data['min_money'],
                                               max_money=validated_data['max_money'],
                                               user=request_user,
                                               start_detail=validated_data['start_detail'],
                                               end_detail=validated_data['end_detail'],
                                               reservation_date=validated_data['reservation_date'],
                                               address_kakao_start=validated_data['address_kakao_start'],
                                               address_kakao_end=validated_data['address_kakao_end'],
                                               max_time=validated_data['max_time'],
                                               min_time=validated_data['min_time'],
                                               start_region=start_region_check[0],
                                               end_region=end_region_check[0]
                                               )
        return bool


    def update(self, instance, validated_data):
        end_region_check = validated_data['address_kakao_end'].split()
        start_region_check = validated_data['address_kakao_start'].split()
        instance.start_detail = validated_data.get('start_detail', instance.start_detail)
        instance.end_detail = validated_data.get('end_detail', instance.end_detail)
        instance.reservation_date = validated_data.get('reservation_date', instance.reservation_date)
        instance.min_money = validated_data.get('min_money', instance.min_money)
        instance.max_money = validated_data.get('max_money', instance.max_money)
        instance.end_region = end_region_check[0]
        instance.start_region = start_region_check[0]
        instance.address_kakao_start = validated_data.get('address_kakao_start', instance.address_kakao_start)
        instance.address_kakao_end = validated_data.get('address_kakao_end', instance.address_kakao_end)
        instance.max_time = validated_data.get('max_time', instance.max_time)
        instance.min_time = validated_data.get('min_time', instance.min_time)
        instance.save()
        return instance


class search(serializers.ModelSerializer):
    class Meta:
        model = user_reservation
        fields = ("reservation_date", "min_money", "max_money", "max_time", "min_time")


