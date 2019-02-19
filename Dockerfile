FROM python:3.4

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

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8080 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8080"]
ENTRYPOINT ["init.sh"]
