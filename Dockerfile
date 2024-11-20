FROM python:3.10.12

ENV HOME=/home/app

RUN apt update -y && apt upgrade -y

WORKDIR $HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . $HOME

RUN pip install -r requirements.txt

# RUN apt install -y apt-transport-https
# RUN apt install -y playwright

RUN playwright install-deps
RUN playwright install chromium

RUN chmod -R u+rwx $HOME/*

ENTRYPOINT ["/home/app/entrypoint.sh"]