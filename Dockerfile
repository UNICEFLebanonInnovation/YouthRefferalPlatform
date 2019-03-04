FROM python:2.7

<<<<<<< HEAD
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
COPY requirements /code/requirements
RUN pip install -r /code/requirements/production.txt
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
ENTRYPOINT ["init.sh"]
=======
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
>>>>>>> 08767f91becd55152c50018c4f99daf396c461d7
