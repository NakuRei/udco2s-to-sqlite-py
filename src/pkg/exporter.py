import abc
import logging
import sqlite3
from typing import Final

from pkg.parser import UdCo2SDataParser


class Exporter(abc.ABC):
    def __init__(self, logger: logging.Logger | None = None) -> None:
        super().__init__()
        self._logger: Final = logger

    @abc.abstractmethod
    def export(self, data: str) -> None:
        pass


class StdoutExporter(Exporter):
    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:
        super().__init__(logger)

    def export(self, data: str) -> None:
        if self._logger:
            self._logger.info(f"Exporting data: {data}")
        print(data)


class SqliteCreateTableError(Exception):
    pass


class SqliteInsertDataError(Exception):
    pass


class SqliteExporter(Exporter):
    PARSER: Final = UdCo2SDataParser()

    def __init__(
        self,
        db_path: str,
        table_name: str,
        logger: logging.Logger | None = None,
    ) -> None:
        super().__init__(logger)
        self._db_path: Final = db_path
        self._table_name: Final = table_name
        try:
            self._conn = self._initialize_db()
        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to initialize database: {e}")
            raise e

    def __del__(self):
        try:
            if hasattr(self, "_conn") and self._conn:
                self._conn.close()
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error in destructor: {e}")
            # Do not raise exception in destructor

    def _initialize_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        self._create_table(conn)
        return conn

    def _create_table(self, conn: sqlite3.Connection) -> None:
        create_table_sql: Final[str] = (
            f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "co2_ppm INTEGER, "
            "humidity_percentage REAL, "
            "temperature_celsius REAL, "
            "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
            ");"
        )
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
        except sqlite3.Error as e:
            raise SqliteCreateTableError(f"Failed to create table: {e}") from e

    def export(self, data: str) -> None:
        try:
            if self._logger:
                self._logger.info(f"Exporting data: {data}")
            parsed_data = self.PARSER.parse(data)
            insert_sql: Final[str] = (
                f"INSERT INTO {self._table_name} "
                "(co2_ppm, humidity_percentage, temperature_celsius) "
                "VALUES (?, ?, ?)"
            )
            cursor = self._conn.cursor()
            cursor.execute(
                insert_sql,
                (
                    parsed_data.co2_ppm,
                    parsed_data.humidity_percentage,
                    parsed_data.temperature_celsius,
                ),
            )
            self._conn.commit()
        except sqlite3.Error as e:
            raise SqliteInsertDataError(f"Failed to insert data: {e}") from e
