#!/bin/bash

# 자동화 스크립트입니다.
# start.sh로 실행하면 됩니다.

# Migrate 설정 Default = False임.
MIGRATE=false

# 자신이 사용하고싶은 Env로 바꾸세요. 만약 있다면 현재 있는 환경으로 변경하세요.
env_name="Django_test"

# 이거 from django.conf import settings에서 가져다가 쓸려했는데, 보안문제 때문에 할 수가 없음
PROJECT_INSTALLED_APPS=(
    "accounts"
    "main"
    "introduce"
    "tech"
)
# 색깔 아스키 코드
COLOR_RED="\033[91m"
COLOR_YELLOW="\033[43m"
COLOR_RESET="\033[0m"



# 아래부터는 수정하지마세요.

if [ -z "$CONDA_EXE" ]; then
    conda init bash
    eval "$(conda shell.bash hook)"
    if ! conda activate $env_name; then
    conda create -y -n $env_name python=3.8
    conda activate $env_name
    pip install -r requirements.txt
    fi
fi

if ! conda activate $env_name; then
    conda create -y -n $env_name python=3.8
    pip install -r requirements.txt
fi

activate_cmd="conda activate $env_name"
eval "$activate_cmd"
echo "Activated conda environment: $env_name"
echo -e "${COLOR_YELLOW} $env_name : Activate Success!!! ${COLOR_RESET}"


if [[ "$MIGRATE" == false ]]; then
    for app in "${PROJECT_INSTALLED_APPS[@]}"
    do
        python manage.py makemigrations $app
        echo -e "${COLOR_YELLOW}$app DONE!${COLOR_RESET}"
    done
    for app in "${PROJECT_INSTALLED_APPS[@]}"
    do
        python manage.py migrate $app
        echo -e "${COLOR_YELLOW}$app DONE!${COLOR_RESET}"
    done
    python manage.py migrate
else
    echo -e "${COLOR_YELLOW}ALL MIGRATE DONE!!!${COLOR_RESET}"
fi

echo -e "${COLOR_YELLOW}Making Docker Image...${COLOR_RESET}"
#docker build -t testyata/django .
echo -e "${COLOR_YELLOW}SUCCESS!!!${COLOR_RESET}"
echo -e "${COLOR_YELLOW}Runing Docker Image...${COLOR_RESET}"
#docker run -p 8000:8000 -d testyata/django
echo -e "${COLOR_YELLOW}SUCCESS!!!${COLOR_RESET}"
echo -e "${COLOR_RED}You Can Access location -> http://127.0.0.1:8000 ${COLOR_RESET}"
python manage.py runserver || {
    echo -e "${COLOR_RED}Error Connection!! ${COLOR_RESET}"
    echo -e "${COLOR_RED}Please Check Docker, Your Computer are Not Open Port ${COLOR_RESET}"
    echo -e "${COLOR_RED}############################################################${COLOR_RESET}"
    echo -e "${COLOR_RED} I don't know if I can do it. ${COLOR_RESET}"
    python manage.py runserver
}