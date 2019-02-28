FROM python:2.7

RUN mkdir /code
WORKDIR /code
ADD . /code/
COPY requirements /code/requirements
RUN pip install -r /code/requirements/local.txt

#RUN sed -i 's/\r//' gunicorn.sh
#RUN chmod +x gunicorn.sh

EXPOSE 5000
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:5000"]
