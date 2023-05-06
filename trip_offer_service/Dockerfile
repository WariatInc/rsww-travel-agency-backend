FROM ubuntu:20.04

ENV PYTHON_VERSION="3.9.13"
ENV PYENV_ROOT="/pyenv"
ENV PYENV_SHELL="bash"
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV PATH="/opt/reservation_service/bin:${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/opt/reservation_service"

WORKDIR /opt/trip_offer_service

RUN set -ex \
    && apt-get update \
    && apt-get install --no-install-recommends --assume-yes \
        ca-certificates \
        libc6-dev \
        libpq-dev \
        libssl-dev \
        libffi-dev \
        libncurses5-dev \
        zlib1g \
        zlib1g-dev \
        libreadline-dev \
        libbz2-dev \
        libsqlite3-dev \
        gnupg \
        gnupg2 \
        openssl \
        gcc \
        make \
        git \
        wget \
        python3-pip \
        unzip

RUN set -ex \
    && wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list \
    && apt-get update \
    && apt-get install -y mongodb-mongosh mongodb-database-tools


RUN set -ex \
    && git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
    && pyenv install $PYTHON_VERSION \
    && echo "$PYTHON_VERSION" > ./.python-version \
    && pyenv rehash

RUN set -ex \
    && wget "https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh" -O /usr/bin/wait-for-it \
    && chmod +x /usr/bin/wait-for-it

RUN set -ex \
    && pip --no-cache-dir --disable-pip-version-check install --upgrade pip setuptools wheel

RUN set -ex \
    && [ "$(python --version)" = "Python $PYTHON_VERSION" ] \
    && python -m venv /opt/trip_offer_service

COPY ./requirements /tmp/requirements

RUN set -ex \
	&& pip install -r /tmp/requirements/base.txt \
    && pip install -r /tmp/requirements/dev.txt \
    && pip install -r /tmp/requirements/test.txt

COPY . /opt/trip_offer_service

RUN set -ex \
    && pip --no-cache-dir --disable-pip-version-check install -e .

