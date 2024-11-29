## 利用Docker部署基于Streamlit搭建的Web系统
1.添加Dockerfile文件
2.设置具体参数
FROM python:3.9

WORKDIR /myproject

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY  / ./

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

3.命令行输入Docker指令打包镜像
docker build ./myproject -t streamlit

4.命令行输入Docker指令运行镜像
docker run -p 8501:8501 streamlit

5.参考文档
https://docs.streamlit.io/deploy/tutorials/docker