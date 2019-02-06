FROM python:2.7
ENV PYTHONUNBUFFERED 1

# SSH support on Azure
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd
COPY sshd_config /etc/ssh/

ARG REQUIREMENTS_FILE=production.txt

RUN mkdir /app/
WORKDIR /app/
COPY requirements /app/requirements
RUN pip install -r /app/requirements/$REQUIREMENTS_FILE

ADD . /app/

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN python manage.py collectstatic --noinput --settings=config.settings.test

# uWSGI will listen on this port
EXPOSE 2222 80

RUN service ssh start

# Start
COPY entrypoint.sh /app/compose/django/entrypoint.sh
RUN chmod +x /app/compose/django/entrypoint.sh
#RUN ["chmod", "+x", "/app/compose/django/entrypoint.sh"]

ENTRYPOINT ["sh", "/app/compose/django/entrypoint.sh"]

COPY gunicorn.sh /app/compose/django/gunicorn.s
RUN chmod +x /app/compose/django/gunicorn.sh
#RUN ["chmod", "+x", "/app/compose/django/gunicorn.sh"]
CMD ["sh", "/app/compose/django/gunicorn.sh"]
