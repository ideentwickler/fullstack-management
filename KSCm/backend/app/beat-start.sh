#! /usr/bin/env bash
set -e

rm -rf celerybeat.pid

python /app/app/celeryworker_pre_start.py

celery beat --app=app.worker -l info
