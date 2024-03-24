import dataclasses
import re
from typing import Final


@dataclasses.dataclass
class Udco2sData:
    co2_ppm: int
    humidity_percentage: float
    temperature_celsius: float


class UdCo2SDataParser:
    CO2_REGEX: Final = re.compile(
        r"CO2=(?P<co2>\d+),HUM=(?P<hum>\d+\.\d+),TMP=(?P<tmp>-?\d+\.\d+)"
    )

    def parse(self, data_str: str) -> Udco2sData:
        match = self.CO2_REGEX.match(data_str)
        if match:
            co2_ppm = int(match.group("co2"))
            humidity_percentage = float(match.group("hum"))
            temperature_celsius = float(match.group("tmp"))
            return Udco2sData(co2_ppm, humidity_percentage, temperature_celsius)
        else:
            raise ValueError("Invalid CO2 data format.")
