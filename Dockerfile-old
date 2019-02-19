FROM python:2.7

# SSH support on Azure
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd
COPY ./compose/django/sshd_config /etc/ssh/

ARG REQUIREMENTS_FILE=production.txt

RUN mkdir /code/
WORKDIR /code/
COPY requirements /code/requirements
RUN pip install -r /code/requirements/$REQUIREMENTS_FILE

ADD . /code/

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN python manage.py collectstatic --noinput --settings=config.settings.test

# uWSGI will listen on this port
EXPOSE 2222 80

RUN service ssh start

# Start
ENTRYPOINT ["/code/compose/django/entrypoint.sh"]

CMD ["/code/compose/django/gunicorn.sh"]
