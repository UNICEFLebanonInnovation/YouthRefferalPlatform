FROM python:2.7
RUN mkdir /code

ADD . /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /code/
COPY requirements /code/requirements
RUN pip install --no-cache-dir -r /code/requirements/production.txt
ADD . /code/

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "$SSH_PASSWD" | chpasswd

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
CMD exec gunicorn djangoapp.wsgi:application --bind 0.0.0.0:8000 --workers 3
ENTRYPOINT ["init.sh"]

