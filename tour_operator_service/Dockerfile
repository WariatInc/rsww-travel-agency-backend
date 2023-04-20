FROM ubuntu:22.04

ENV PYTHON_VERSION="3.9.13"
ENV PYENV_ROOT="/pyenv"
ENV PYENV_SHELL="bash"
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV PATH="/opt/tour_operator/bin:${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/opt/tour_operator"

WORKDIR /opt/tour_operator

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
     && apt-get install --no-install-recommends --assume-yes \
        postgresql-client

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
    && python -m venv /opt/tour_operator

COPY ./requirements /tmp/requirements

RUN set -ex \
	&& pip install -r /tmp/requirements/base.txt \
    && pip install -r /tmp/requirements/dev.txt \
    && pip install -r /tmp/requirements/test.txt

COPY . /opt/tour_operator

RUN set -ex \
    && pip --no-cache-dir --disable-pip-version-check install -e .
