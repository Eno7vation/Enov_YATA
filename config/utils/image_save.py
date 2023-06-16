import os
from uuid import uuid4
from django.utils import timezone

def rename_image_to_uuid_accounts(instance, filename):
    model_name = instance.__class__.__name__.lower()
    field_name = instance._meta.get_field('avatar').name
    db_name = instance._meta.db_table
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    time = timezone.localtime()
    time = str(time)[5:16]

    if instance:
        filename = f"{instance.nickname}_{uuid[0:10]}.{ext}"
    else:
        filename = f"{uuid[0:10]}.{ext}"

    return f'{model_name}/{db_name}/{field_name}/{instance.nickname}_{time}_{uuid4().hex[0:5]}_{filename}'

def rename_image_to_uuid_license(instance, filename):
    model_name = instance.__class__.__name__.lower()
    field_name = instance._meta.get_field('license_img').name
    db_name = instance._meta.db_table
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    time = timezone.localtime()
    time = str(time)[5:16]

    if instance:
        filename = f"{instance.nickname}_{uuid[0:10]}.{ext}"
    else:
        filename = f"{uuid[0:10]}.{ext}"

    return f'{model_name}/{db_name}/{field_name}/{instance.nickname}_{time}_{uuid4().hex[0:5]}_{filename}'

def rename_image_to_uuid_everything(instance, filename):
    model_name = instance.__class__.__name__.lower()
    db_name = instance._meta.db_table
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    time = timezone.localtime()
    time = str(time)[5:16]

    if instance:
        filename = f"{instance.author}_{uuid[0:10]}.{ext}"
    else:
        filename = f"{uuid[0:10]}.{ext}"

    return f'{model_name}/{db_name}/{instance.author}_{time}_{uuid4().hex[0:5]}_{filename}'