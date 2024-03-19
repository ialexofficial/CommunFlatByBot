FROM python:3.10.12

ENV HOME=/home/app

RUN addgroup --system app && adduser --system app --ingroup app

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