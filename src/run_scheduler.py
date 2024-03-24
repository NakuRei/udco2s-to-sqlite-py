import argparse
import json
import logging
import logging.config
import time

import schedule

from pkg.udco2s import UdCo2S
from pkg.create_exporter import create_exporter, ExporterType


def parse_arguments() -> argparse.Namespace:
    perser = argparse.ArgumentParser(description="Stores CO2 level from sensor")
    perser.add_argument(
        "--port",
        type=str,
        default="/dev/ttyACM0",
        help="Serial port to connect to the CO2 sensor (default: /dev/ttyACM0)",
    )
    perser.add_argument(
        "--db_path",
        type=str,
        default="./db/udco2s_data.db",
        help="Path to the database file (default: ./db/udco2s_data.db)",
    )
    perser.add_argument(
        "--table_name",
        type=str,
        default="sensor_data",
        help="Name of the table to store CO2 level (default: sensor_data)",
    )
    perser.add_argument(
        "--interval_sec",
        type=int,
        default=10,
        help="Interval to read CO2 level in seconds (default: 10)",
    )
    perser.add_argument(
        "--logging_config_path",
        type=str,
        default="./src/logging_config.json",
        help=(
            "Path to the logging config file "
            "(default: ./src/logging_config.json)"
        ),
    )

    return perser.parse_args()


def setup_logging(config_json_path: str):
    with open(config_json_path, "r") as f:
        config = json.load(f)
        logging.config.dictConfig(config)


def run_scheduler(
    port: str,
    db_path: str,
    table_name: str,
    interval_sec: int,
    logger: logging.Logger | None = None,
):
    exporter = create_exporter(
        exporter_type=ExporterType.SQLITE,
        logger=logger,
        db_path=db_path,
        table_name=table_name,
    )
    co2_sensor = UdCo2S(exporter=exporter, port=port, logger=logger)

    schedule.every(interval_sec).seconds.do(
        lambda: co2_sensor.read(is_once=True)
    )
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    args = parse_arguments()

    setup_logging(args.logging_config_path)
    logger = logging.getLogger(__name__)

    try:
        run_scheduler(
            port=args.port,
            db_path=args.db_path,
            table_name=args.table_name,
            interval_sec=args.interval_sec,
            logger=logger,
        )
    except Exception as e:
        logger.error(f"Error: {e}")
