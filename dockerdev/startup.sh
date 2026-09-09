#!/bin/bash
  
# Start the first process
openssl rand -hex 32 > /app/git_hash

if [ $ENABLE_CRON == "True" ];
then

    #service cron start &
    echo "Starting Python Cron"
    python /bin/scheduler.py /app/python-cron /app/logs/python-cron.log &
    status=$?
    if [ $status -ne 0  ]; then
      echo "Failed to start cron: $status"
        exit $status
    fi

fi

if [ $ENABLE_WEB == "True" ];
then
    echo "Starting Gunicorn"

    # Start the second process
    gunicorn commercialoperator.wsgi --bind :8080 --config /app/gunicorn.ini.py
    status=$?
    if [ $status -ne 0  ]; then
          echo "Failed to start gunicorn: $status"
            exit $status
    fi
fi

if [ $CODE_SERVER_PASSWORD_ENABLED == "True" ];
    then
echo "Starting code server"
# Start the second process
if [ -n "$CODE_SERVER_PASSWORD" ]; then
  PASSWORD="$CODE_SERVER_PASSWORD" code-server --bind-addr 0.0.0.0:8443 --auth password /data/data/projects/commercialoperator
fi
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start code server: $status"
  exit $status
fi
else
   echo "CODE_SERVER_PASSWORD_ENABLED environment vairable not set to True, code server is not starting."
   /bin/bash
fi
