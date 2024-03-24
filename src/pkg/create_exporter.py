import enum
import logging
from typing import Any

from pkg.exporter import Exporter, StdoutExporter, SqliteExporter


class ExporterType(enum.Enum):
    STDOUT = "stdout"
    SQLITE = "sqlite"


def create_exporter(
    exporter_type: ExporterType,
    logger: logging.Logger | None = None,
    **kwargs: Any,
) -> Exporter:
    if exporter_type == ExporterType.STDOUT:
        return StdoutExporter(logger=logger)
    elif exporter_type == ExporterType.SQLITE:
        return SqliteExporter(logger=logger, **kwargs)
    else:
        raise ValueError(f"Unknown exporter type: {exporter_type}")
