Enov YATA 사용 가이드
=============

## Using Stack List 
<table><tr><td valign="top" width="33%">

### Frontend  
<div align="center">  
<a href="https://en.wikipedia.org/wiki/HTML5" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/html5-original-wordmark.svg" alt="HTML5" height="50" /></a>  
<a href="https://www.w3schools.com/css/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/css3-original-wordmark.svg" alt="CSS3" height="50" /></a>  
<a href="https://www.javascript.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/javascript-original.svg" alt="JavaScript" height="50" /></a>  
<a href="https://www.figma.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/figma-icon.svg" alt="Figma" height="50" /></a>  
</div>
</td><td valign="top" width="33%">

### Backend  
<div align="center">  
<a href="https://www.python.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="50" /></a>  
<a href="https://www.djangoproject.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/django-original.svg" alt="Django" height="50" /></a>  
</div>
</td><td valign="top" width="33%">

### DevOps  
<div align="center">  
<a href="https://go.dev/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/go-original.svg" alt="Go" height="50" /></a>  
<a href="https://www.python.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="50" /></a>  
<a href="https://aws.amazon.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/amazonwebservices-original-wordmark.svg" alt="AWS" height="50" /></a>  
<a href="https://www.docker.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/docker-original-wordmark.svg" alt="Docker" height="50" /></a>  
<a href="https://www.jenkins.io/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/jenkins-icon.svg" alt="Jenkins" height="50" /></a>  
<a href="https://kubernetes.io/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/kubernetes-icon.svg" alt="Kubernetes" height="50" /></a>  
<a href="https://www.nginx.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/nginx-original.svg" alt="Nginx" height="50" /></a>  
<a href="https://www.linux.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/linux-original.svg" alt="Linux" height="50" /></a>  
</div>

</td></tr></table>  

<br/>  

## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (AGPL) <br>
See the [OPEN_SOURCE](OpenSoruce_LICENSE.md) file for license rights and limitations (MIT)

Templates과 Server파일은 저작권 때문에 공개하지 않습니다.

## 디자인
https://www.figma.com/file/gBDXKyEsHgX1iSm2vIt31k/YATA_app?node-id=0-1

개발자
-------------
### 해당 프로젝트는 컴퓨터공학과와 산업 디자인학과의 협업으로 개발되었습니다.

Eno789님은 PM, Devops(Golang, Python, Nginx), Frontend(JS/DTL), Backend(Utils)를 담당했습니다.

<a href="https://github.com/Eno789" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>

wchorong님은 Frontend(JS/DTL), Backend 총괄을 담당했습니다.

<a href="https://github.com/wchorong" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>

Jinho Park님은 Frontend(HTML/CSS/JS/DTL), Design(Figma)을 담당했습니다.

<a href="https://github.com/02wlsh" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>

mmmmmiso님은 Design(Figma)을 담당했습니다.

<a href="https://github.com/mmmmmiso" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>

저작권
-------------
* 해당 오픈소스의 제3자는 필수적으로 LICENSE.txt를 따라야합니다. 
* 해당 오픈소스를 절대 상업적으로 사용해서는 안됩니다.
* 해당 오픈소스 프로젝트를 사용할때에는 아래 개발자를 프로젝트에 필수적으로 명시해야합니다.
  * Eno789 [Github](https://github.com/Eno789)
  * wchorong [Github](https://github.com/wchorong)
  * Jinho Park [Github](https://github.com/02wlsh)
  * mmmmmiso [Github](https://github.com/mmmmmiso)


### AGPLv3가 발동되는 상황
* 수정(modify)
* 전파(propagate)
* 운반(Convey)

자세한 설명은 아래 링크를 참고해주세요

[자세한 설명](https://blog.outsider.ne.kr/1555)

<hr/>


가상환경 생성 가이드
-------------
> ```conda create -n "Django_YATA" python=3.8```

> ```conda activate Django_YATA```

> ```pip install -r requirements.txt```

DB 가이드
-------------
#### 기본적으로 DB는 제공되므로, 오류가 생길시 아래의 프로세스를 진행해주세요.
#### 오류가 없다면, 실행가이드 1번을 진행해주세요.
> ```python manage.py makemigrations accounts```

> ```python manage.py migrate accounts```

> ```python manage.py makemigrations```

> ```python manage.py migrate```
<hr/>

실행 가이드
-------------
### 1. Docker

> ```docker build -t enov_yata/django .```

> ```docker image ls```

> ```docker run enov_yata/django -p 8000:8000 -d ```

##### 1-1 실행 종료 
> ```docker ps```

> ```docker stop "CONTAINER ID"```
### 2. shell or console

> ```python manage.py runserver 8000```

##### 2-1 실행 종료 

> ```Ctr + C ``` or ```Ctr + Z ```

[접속 링크](http://127.0.0.1:8000)


