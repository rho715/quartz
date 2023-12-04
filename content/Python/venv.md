---
title: 🐍 파이썬 가상환경 설정하기
tags:
  - python
  - anaconda
  - venv
---

# Why virtual environment?
>[!info]
> Creating a virtual environment in Python is essential to:
> 1. Isolate projects: It prevents conflicts by segregating dependencies and packages, ensuring one project doesn't interfere with another.
> 2. Manage dependencies: Virtual environments let you control project-specific dependencies, aiding in clean, organized development and simplified sharing with others.
> 
> *answer from chatGPT*

# venv vs conda env 차이점

- venv
	- 가상환경이 프로젝트 폴더에 생성 됨 
- conda env
	- `anaconda3 > envs`

프로젝트 폴더에 가상환경이 만들어지기 원하지 않은 분들은 다 conda env를 사용하고 있음.   
나중에 생성한 가상환경을 찾기에는 conda 가상환경이 편리하지만 conda 자체를 사용안한다면 venv
# venv
## environment 생성하기
```console
python3 -m venv {env}
```

## activate virtual environment
```console
source {env}/bin/activate
```

# conda env
## environment 생성하기
```console
conda create -n {env_name} python=3.#
``` 

## environment 리스트 보기 
```console
conda env list
``` 

## environment 활성화 
```console
conda activate {env_name}
``` 

## environment 비활성화
```console
conda deactivate {env_name}
``` 

## environment 삭제
```console
conda env remove -n {env_name}
``` 

## environment 클론
```console
conda create -n {new_env} --clone {org_env}
``` 

## get installed packages list
```console
conda list 
``` 

## install a package
```
conda install pandas 
``` 

## install packages 
```console
conda install pandas numpy 
``` 

## update a package 
```console
conda update pandas 
``` 

## update a package 
```console
conda upgrade --all 
``` 

## delete a package 
```console
conda remove pandas 
``` 

# 공동

## install packages 
```console
pip install {p1} {p2}
```

## environment freeze 
```console
pip freeze > requirements.txt
```

## install requirements.txt
```console
pip install -r requirements.txt
``` 

## uninstall requirements.txt 
```console
pip uninstall -r  requirements.txt
``` 


# 출처 
- [https://teddylee777.github.io/python/anaconda-%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD%EC%84%A4%EC%A0%95-%ED%8C%81-%EA%B0%95%EC%A2%8C/](https://teddylee777.github.io/python/anaconda-%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD%EC%84%A4%EC%A0%95-%ED%8C%81-%EA%B0%95%EC%A2%8C/)
- [https://yganalyst.github.io/basic/anaconda_env_1/](https://yganalyst.github.io/basic/anaconda_env_1/)
- https://www.youtube.com/watch?v=CzAyaSolZjY