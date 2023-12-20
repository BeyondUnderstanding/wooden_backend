FROM ubuntu:22.04

RUN apt update
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        libbz2-dev \
        wget \
    && export DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tbilisi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt install python3.11 python3-pip -y

WORKDIR /tmp
RUN apt install libssl-dev -y
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb \
    && apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir -r /code/requirements.txt

COPY ./src /code/src
COPY ./.env /code/src
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--proxy-headers", "--forwarded-allow-ips='*'", "--host", "0.0.0.0", "--port", "8000"]