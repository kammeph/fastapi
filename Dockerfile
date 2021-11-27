FROM python:3.9.2-slim
RUN apt-get update && apt-get install -y

RUN groupadd -r pythonusers && useradd -r -g pythonusers python

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .

USER python

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]