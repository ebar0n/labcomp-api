FROM python:3.5-slim
MAINTAINER LabcompTeam


RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY ./requirements/base.pip /requirements/base.pip
COPY ./requirements/development.pip /requirements/development.pip
RUN pip install -r /requirements/development.pip

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
