# udco2s-to-sqlite-py

A Docker-based system for capturing and storing CO2 sensor data from the IO-DATA [UD-CO2S](https://www.iodata.jp/product/tsushin/iot/ud-co2s/) device into a SQLite database.

## Description

This project enables the automated collection of CO2 sensor data through a Dockerized Python application. It is specifically tailored to work with the UD-CO2S sensor, reading data at user-defined intervals and storing it in a SQLite database for persistence. The application runs within a Docker container, utilizing Docker Compose for easy deployment and management.

## Requirement

- Docker Engine (>= 25.0.3) and Docker Compose (>= 2.24.7) installed on your system.
- An IO-DATA [UD-CO2S](https://www.iodata.jp/product/tsushin/iot/ud-co2s/) CO2 sensor connected to the system via a serial port (default `/dev/ttyACM0`).

## Installation

1. Clone this repository to your local machine.
2. Ensure Docker and Docker Compose are installed on your system.
3. Navigate to the project directory where the `compose.yaml` file is located.

## Usage

### Starting the Application

To start the CO2 Level Monitoring System, run the following command in the terminal:

```bash
docker compose up -d
```

This command builds the Docker image and starts the container as defined in the `compose.yaml` file. The system will begin collecting data from the CO2 sensor and storing it in the SQLite database at specified intervals.

### Stopping the Application

To stop the application and the container, you can use the following Docker Compose command in the terminal:

```shell
docker compose down
```

This command will stop and remove the containers, networks, and volumes created by `docker compose up`.

## Custom Configuration

You can customize the configuration by modifying the `compose.yaml` and `entrypoint.sh` files. Key variables include:

- `DEVICE_PORT`: The serial port connected to the CO2 sensor.
- `DB_PATH`: The path to the SQLite database file.
- `TABLE_NAME`: The name of the database table where data is stored.
- `INTERVAL_SEC`: The interval, in seconds, at which data is collected from the sensor.

## Author

- Nakurei
    - [GitHub](https://github.com/NakuRei)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
