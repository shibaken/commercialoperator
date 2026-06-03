# Prepare the base environment.
FROM ubuntu:24.04 as builder_base_cols
MAINTAINER asi@dbca.wa.gov.au
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBUG=True
ENV TZ=Australia/Perth
ENV EMAIL_HOST="smtp.corporateict.domain"
ENV DEFAULT_FROM_EMAIL='no-reply@dbca.wa.gov.au'
ENV NOTIFICATION_EMAIL=''
ENV NON_PROD_EMAIL=''
ENV PRODUCTION_EMAIL=True
ENV EMAIL_INSTANCE='DEV'
ENV SECRET_KEY="ThisisNotRealKey"
ENV SITE_PREFIX='cols'
ENV SITE_DOMAIN='dbca.wa.gov.au'
ENV OSCAR_SHOP_NAME='Parks & Wildlife'
ENV BPAY_ALLOWED=False
ENV NODE_MAJOR=20

RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install --no-install-recommends -y wget git libmagic-dev gcc binutils libproj-dev gdal-bin python3-setuptools python3-pip tzdata cron rsyslog gunicorn libreoffice virtualenv
RUN apt-get install --no-install-recommends -y libpq-dev patch
RUN apt-get install --no-install-recommends -y postgresql-client mtr htop vim ssh 
RUN apt-get install --no-install-recommends -y python3-gevent software-properties-common imagemagick curl bzip2 npm vim

RUN groupadd -g 5000 oim 
RUN useradd -g 5000 -u 5000 oim -s /bin/bash -d /app
RUN mkdir /app 
RUN chown -R oim.oim /app 

# nvm env vars
#RUN mkdir -p /usr/local/nvm
#ENV NVM_DIR /usr/local/nvm
#ENV NODE_VERSION v10.19.0
#RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
#RUN /bin/bash -c ". $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
#ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/bin
#ENV PATH $NODE_PATH:$PATH

# Default Scripts
RUN wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/default_script_installer.sh -O /tmp/default_script_installer.sh
RUN chmod 755 /tmp/default_script_installer.sh
RUN /tmp/default_script_installer.sh

RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs


RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
#RUN apt-get install --no-install-recommends -y python3.7 python3.7-dev python3.7-distutils

#RUN ln -s /usr/bin/python3.7 /usr/bin/python 
#RUN python3.7 -m pip install --upgrade pip
ENV TZ=Australia/Perth
COPY timezone /etc/timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python libs from requirements.txt.
FROM builder_base_cols as python_libs_cols
WORKDIR /app
USER oim
RUN virtualenv /app/venv
ENV PATH=/app/venv/bin:$PATH
RUN git config --global --add safe.directory /app

COPY --chown=oim:oim  requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN  rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*

#COPY libgeos.py.patch /app/
#RUN patch /usr/local/lib/python3.7/dist-packages/django/contrib/gis/geos/libgeos.py /app/libgeos.py.patch
#RUN rm /app/libgeos.py.patch

# Install the project (ensure that frontend projects have been built prior to this step).
FROM python_libs_cols
COPY --chown=oim:oim  gunicorn.ini.py manage.py ./
RUN touch /app/.env
COPY .git ./.git
COPY --chown=oim:oim commercialoperator ./commercialoperator
RUN cd /app/commercialoperator/frontend/commercialoperator; npm install
RUN cd /app/commercialoperator/frontend/commercialoperator; npm run build
RUN python manage.py collectstatic --noinput

RUN mkdir /app/tmp/
RUN chmod 777 /app/tmp/
COPY --chown=oim:oim  python-cron ./
COPY --chown=oim:oim startup.sh /
RUN chmod 755 /startup.sh
# Cron start
#RUN service rsyslog start
#RUN chmod 0644 /etc/cron.d/dockercron
#RUN crontab /etc/cron.d/dockercron
#RUN touch /var/log/cron.log
#RUN service cron start
#RUN chmod 755 /startup.sh
# cron end

# IPYTHONDIR - Will allow shell_plus (in Docker) to remember history between sessions
# 1. will create dir, if it does not already exist
# 2. will create profile, if it does not already exist
#RUN mkdir /app/logs/.ipython
#RUN export IPYTHONDIR=/app/logs/.ipython/
#RUN python profile create 

# Health checks for kubernetes 
#RUN wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/health_check.sh -O /bin/health_check.sh
#RUN chmod 755 /bin/health_check.sh

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]
#CMD ["gunicorn", "commercialoperator.wsgi", "--bind", ":8080", "--config", "gunicorn.ini.py"]
