---
title: PyCharm Docker Connection
tags:
  - pycharm
  - docker
  - ide
  - "#check"
---
# PyCharm using Docker Compose as Interpreter

> [!warning]
> `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

- **Problem:** Airflow 라이브러리를 사용하고 싶어서 PyCharm Interpreter로 Docker Compose를 사용하려고 했는데 실제로 도커 데스크톱은 실행되지만 connect이 안되는 에러 발생 
- **Solution:** MacBooc Pro M1 사용하고 있는데 `Docker Desktop no longer places the socket at /var/run but ~/.docker/run.` 이라고 해서 2가지 솔루션 시도 
	1. use "TCP socket" with "Enging API URL": `unix:///Users/your_name/.docker/run/docker.sock`
	2. or symlink the socket to the expected position: `sudo ln -s /Users/your_name/.docker/run/docker.sock /var/run/`
- 1번 실패, 2번 성공! (Thank you Martin Meier 🙏🏻 [링크](https://youtrack.jetbrains.com/issue/IDEA-258012/Cannot-connect-to-the-Docker-daemon-at-unix-var-run-docker.sock.-Is-the-docker-daemon-running))
