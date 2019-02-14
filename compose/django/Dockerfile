FROM python:2.7
ENV PYTHONUNBUFFERED 1

# SSH support on Azure
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd
COPY sshd_config /etc/ssh/

#RUN addgroup -S django \
#    && adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

#COPY ./compose/django/entrypoint.sh /entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
#RUN chown django /entrypoint.sh

COPY ./compose/django/start /start
#COPY start.sh /start.sh
RUN sed -i 's/\r//' /start
RUN chmod +x /start
#RUN chown django /start

COPY . /app

#RUN chown -R django /app
#RUN chown -R /app

#USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
