FROM python:3.10.12

ENV HOME=/home/app

RUN addgroup --system app && adduser --system app --ingroup app

RUN apt update -y && apt upgrade -y

RUN apt install libxext6 \
    libnss3 libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libdrm2  -y

WORKDIR $HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY ./requirements.txt $HOME

RUN pip install -r requirements.txt

COPY . $HOME
RUN chmod ug+x  $HOME/*

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

ENTRYPOINT ["python3", "main.py"]