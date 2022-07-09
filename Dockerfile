FROM python:3.9.13-bullseye
RUN mkdir /p
RUN mkdir /p/app
ADD ./app /p/app
ADD ./manage.py /p
ADD ./requirements.txt /p
WORKDIR /p
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "manage.py", "run" ]