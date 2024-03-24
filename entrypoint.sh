#!/bin/sh
set -eu

readonly DEVICE_PORT="${DEVICE_PORT:-/dev/ttyACM0}"
readonly DB_PATH="${DB_PATH:-./db/udco2s_data.db}"
readonly TABLE_NAME="${TABLE_NAME:-sensor_data}"
readonly INTERVAL_SEC="${INTERVAL_SEC:-10}"

python src/run_scheduler.py \
  --port ${DEVICE_PORT} \
  --db_path ${DB_PATH} \
  --table_name ${TABLE_NAME} \
  --interval_sec ${INTERVAL_SEC}
