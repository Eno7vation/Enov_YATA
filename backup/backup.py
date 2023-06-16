import os
import datetime

#crontab -e
#0 4 * * * python /root/enov/CI-CD-Pipeine-YAYA-/backup/backup.py
#매일 새벽 4시 마다 백업

PATH = r"/root/enov/CI-CD-Pipeine-YAYA-"

MAX_FILE_COUNT = 10
BACKUP_DIR = "backup"

time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

#backup으로 시작하면서 .json으로 끝나는 파일의 합계를 구하는 로직
backup_count = sum(
    1 for file_name in os.listdir(BACKUP_DIR)
    if file_name.startswith("backup_") and file_name.endswith(".json")
)

#backup_count의 크기가 MAX_FILE_COUNT이상일 경우 폴더를 생성하고 분리하는 로직입니다. 즉 10일마다
#backup_1, backup_2와 같은 형태로 폴더를 생성하고, 저장하는 로직입니다.
if backup_count >= MAX_FILE_COUNT:
    backup_dirs = [
        dir_name for dir_name in os.listdir()
        if dir_name.startswith("backup_")
    ]
    new_dir_name = f"{BACKUP_DIR}_{len(backup_dirs) + 1}"
    os.makedirs(new_dir_name)
    backup_dir = new_dir_name
else:
    backup_dir = BACKUP_DIR

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.strftime('%H')
minute = now.minute

weekday = now.strftime('%A')


backup_file_path = os.path.join(os.getcwd(), backup_dir, f"{year}년_{month}월{day}일_{hour}시{minute}분_{weekday}.json")

os.system(f"python -Xutf8 {PATH}/manage.py dumpdata --indent 4 > {backup_file_path}")
# os.system(f"git add .")
# os.system(f"git commit -m asdasd")
# os.system(f"git push -u origin main")
