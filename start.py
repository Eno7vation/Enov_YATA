import os
import subprocess
import sys

#자동화 스크립트입니다.
#python start.py로 실행하면 됩니다.

#Migrate 설정 Default = False임.
MIGRATE = True

#자신이 사용하고싶은 Env로 바꾸세요. 만약 있다면 현재 있는 환경으로 변경하세요.
env_name = 'Django_test'

#이거 from django.conf import settings에서 가져다가 쓸려했는데, 보안문제 때문에 할 수가 없음
PROJECT_INSTALLED_APPS = [
    'accounts',
    'main',
    'introduce',
    'tech',
]
#색깔 아스키 코드
COLOR_RED = "\033[91m"; COLOR_YELLOW = "\033[43m"; COLOR_RESET = "\033[0m"







#아래부터는 수정하지마세요.
try:
    activate_cmd = f'conda activate {env_name}'
    subprocess.check_call(activate_cmd.split(), shell=True)
    print(f'Activated conda environment: {env_name}')
    print(f"{COLOR_YELLOW} {env_name} : Activate Success!!! {COLOR_RESET}")


    if MIGRATE == False:
        for i in range(len(PROJECT_INSTALLED_APPS)):
            os.system(f"python manage.py makemigrations {PROJECT_INSTALLED_APPS[i]}")
            print(f"{COLOR_YELLOW}{PROJECT_INSTALLED_APPS[i]} DONE!{COLOR_RESET}")
        for i in range(len(PROJECT_INSTALLED_APPS)):
            os.system(f"python manage.py migrate {PROJECT_INSTALLED_APPS[i]}")
            print(f"{COLOR_YELLOW}{PROJECT_INSTALLED_APPS[i]} DONE!{COLOR_RESET}")
        os.system(f"python manage.py migrate")
    else:
        print(f"{COLOR_YELLOW}ALL MIGRATE DONE!!!{COLOR_RESET}")

    try:
        print(f"{COLOR_YELLOW}Making Docker Image...{COLOR_RESET}")
        # subprocess.check_call(['docker', 'build', '-t', 'testyata/django', '.'])
        print(f"{COLOR_YELLOW}SUCCESS!!!{COLOR_RESET}")
        print(f"{COLOR_YELLOW}Runing Docker Image...{COLOR_RESET}")
        # subprocess.check_call(['docker', 'run', '-p', '8000:8000', '-d', 'testyata/django'])
        print(f"{COLOR_YELLOW}SUCCESS!!!{COLOR_RESET}")
        print(f"{COLOR_RED}You Can Access location -> http://127.0.0.1:8000 {COLOR_RESET}")
        os.system(f"python manage.py runserver")
    except subprocess.CalledProcessError:
        print(f"{COLOR_RED}Error Connection!! {COLOR_RESET}")
        print(f"{COLOR_RED}Please Check Docker, Your Computer are Not Open Port {COLOR_RESET}")
        print(f"{COLOR_RED}############################################################")
        print(f"{COLOR_RED} I don't know if I can do it. {COLOR_RESET}")
        os.system(f"python manage.py runserver")



except subprocess.CalledProcessError:
    print(f'Could not activate conda environment: {env_name}')
    print('Making Virtual Env...')
    try:
        subprocess.check_call(['conda', 'create', '-n', f'{env_name}', 'python =3.8'])
    except subprocess.CalledProcessError:
        print(f'Could not create conda environment: {env_name}')
    else:
        print('activate Virtual Env...')
        subprocess.check_call(['conda', 'activate', f'{env_name}'])
        print('Installing requirements...')
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])


#리눅스감지 됐을때 아래의 코드를 실행합니다.

primary_loc = "/root/enov/CI-CD-Pipeine-YAYA-/"

if sys.platform == "linux":
    print("개발중입니다.")


