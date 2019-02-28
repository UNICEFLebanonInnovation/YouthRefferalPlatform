FROM python:2.7

ENV PYTHONUNBUFFERED 1

# SSH support on Azure
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd
COPY ./sshd_config /etc/ssh/

ARG REQUIREMENTS_FILE=production.txt

RUN mkdir /code
WORKDIR /code
COPY requirements /code/requirements
RUN pip install -r /code/requirements/$REQUIREMENTS_FILE

ADD . /code/

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN python manage.py collectstatic --noinput --settings=config.settings.test

# uWSGI will listen on this port
EXPOSE 2222 80

#COPY entrypoint.sh /entrypoint.sh
#RUN sed -i 's/\r//' /entrypoint.sh
#RUN chmod +x /entrypoint.sh

#COPY Procfile /Procfile
#RUN sed -i 's/\r//' /Procfile
#RUN chmod +x /Procfile

#COPY gunicorn.sh /gunicorn.sh
#RUN sed -i 's/\r//' /gunicorn.sh
#RUN chmod +x /gunicorn.sh

RUN service ssh start

# Start
#ENTRYPOINT ["/entrypoint.sh"]

#CMD ["/gunicorn.sh"]
CMD honcho start
