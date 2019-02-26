#FROM python:3.4
FROM python:2.7

ARG REQUIREMENTS_FILE=production.txt

RUN mkdir /code
WORKDIR /code

COPY requirements /code/requirements
RUN pip install -r /code/requirements/$REQUIREMENTS_FILE

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
#COPY gunicorn.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
#RUN chmod u+x /usr/local/bin/gunicorn.sh
#EXPOSE 8080 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8080"]
ENTRYPOINT ["init.sh"]

#COPY entrypoint.sh /code/entrypoint.sh
#RUN chmod +x /code/entrypoint.sh
#ENTRYPOINT ["/code/entrypoint.sh"]

#CMD ["/code/gunicorn.sh"]
