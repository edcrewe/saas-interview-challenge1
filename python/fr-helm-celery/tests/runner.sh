# Integration tests need celery run up to be there for web API testing

export PID_FILE=/var/run/unit_test_worker.pid
rm -f $PID_FILE
rm -fr $FR_OPS_TEST_WORKER_LOG_PATH
celery multi start -A fr_helm_celery.helm.tasks worker --loglevel=info --logfile=$FR_OPS_TEST_WORKER_LOG_PATH --pidfile=$PID_FILE
cd /opt/fr-helm-celery/tests
pytest --cov=fr_helm_celery
celery multi stop --pidfile=$PID_FILE
kill -9 $(ps aux | grep celery | awk '{print $2}')
