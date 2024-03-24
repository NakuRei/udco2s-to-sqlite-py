import logging
import sys
from typing import Final

import serial

from pkg.exporter import Exporter


class SerialPortOpenException(Exception):
    pass


class DeviceNotReadyException(Exception):
    pass


class DataReadTimeoutException(Exception):
    pass


class SerialPortCloseException(Exception):
    pass


class UdCo2S:
    def __init__(
        self,
        exporter: Exporter,
        port: str = "/dev/ttyACM0",
        baudrate: int = 115200,
        time_out_sec: int = 10,
        logger: logging.Logger | None = None,
    ):
        super().__init__()
        self._exporter: Final = exporter
        self._port: Final = port
        self._baudrate: Final = baudrate
        self._time_out_sec: Final = time_out_sec
        self._logger: Final = logger

    def read(self, is_once: bool = False) -> None:
        sp = None
        try:
            sp = self._open_serial_port()
            self._check_device_ready(sp)

            if is_once:
                self._read_once(sp)
            else:
                self._read_continuously(sp)
        except Exception as e:
            if self._logger:
                self._logger.error(e)
            raise e
        finally:
            if sp:
                self._close_serial_port(sp)

    def _open_serial_port(self) -> serial.Serial:
        try:
            sp = serial.Serial(
                port=self._port,
                baudrate=self._baudrate,
                timeout=self._time_out_sec,
            )
            sp.reset_input_buffer()
            return sp
        except serial.SerialException as e:
            raise SerialPortOpenException(
                f"Failed to open serial port: {e}"
            ) from e

    def _check_device_ready(self, sp: serial.Serial) -> None:
        sp.write(b"STA\r\n")
        response = sp.readline().decode("utf-8").strip()
        if self._logger:
            self._logger.debug(f"Device ready: {response}")
        if response != "OK STA":
            raise DeviceNotReadyException(f"Device is not ready: {response}")

    def _close_serial_port(self, sp: serial.Serial) -> None:
        if sp and sp.is_open:
            try:
                sp.write(b"STP\r\n")
                response = sp.readline().decode("utf-8").strip()
                sp.close()
                if self._logger:
                    self._logger.debug(f"Device stopped: {response}")
                if response != "OK STP":
                    raise SerialPortCloseException(
                        f"Device is not stopped: {response}"
                    )
            except Exception as e:
                raise SerialPortCloseException(
                    f"Failed to close serial port: {e}"
                ) from e

    def _read_once(self, sp: serial.Serial) -> None:
        self._read_data(sp, is_continuously=False)

    def _read_continuously(self, sp: serial.Serial) -> None:
        try:
            self._read_data(sp, is_continuously=True)
        except KeyboardInterrupt:
            if self._logger:
                self._logger.info("Stopped reading data by user's request")
            else:
                print("Stopped reading data by user's request")
        except Exception as e:
            if self._logger:
                self._logger.error(e)
            else:
                print(e, file=sys.stderr)
            # Do not raise exception in _read_continuously

    def _read_data(self, sp: serial.Serial, is_continuously: bool) -> None:
        while True:
            response = sp.readline().decode("utf-8").strip()
            if self._logger:
                self._logger.debug(f"Received data: {response}")
            if response:
                self._exporter.export(response)
                if not is_continuously:
                    break
            else:
                raise DataReadTimeoutException("Data read timeout")
