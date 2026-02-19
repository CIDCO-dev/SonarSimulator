# SonarSimulator

NMEA-0183 depth simulator for serial-connected systems.

## Features
- Generates `SDDPT` or `SDDBT` frames once per second by default.
- Uses a deterministic depth pattern based on current second (`10 + second`).
- Sends data over a serial port (`/dev/ttyUSB0` and `9600` by default).
- Can run manually or as a `systemd` service (`nmea.service`).

## Repository Layout
- `Script/sonar_simulator.py`: simulator entrypoint.
- `Script/autolaunch.sh`: launcher used by systemd.
- `Script/sonar_simulator_unittest.py`: unit tests.
- `Script/unittest.sh`: test runner.
- `Install/install.sh`: service installation script.
- `BOM.txt`: hardware bill of materials.

## Requirements
- Ubuntu (tested workflow targets Raspberry Pi with Ubuntu Server).
- Python 3.
- `pyserial` (`python3-serial` package).

## Manual Run
From repository root:

```bash
python3 Script/sonar_simulator.py /dev/ttyUSB0 9600
```

Optional arguments:

```bash
python3 Script/sonar_simulator.py /dev/ttyUSB0 9600 --sentence-type dbt --interval 0.5 --iterations 10
```

## Install as Service
From repository root:

```bash
bash Install/install.sh
```

This installs and starts `nmea.service` with default environment values:
- `SONAR_SERIAL_PORT=/dev/ttyUSB0`
- `SONAR_BAUD_RATE=9600`
- `SONAR_SENTENCE_TYPE=dpt`

Service commands:

```bash
sudo systemctl status nmea
sudo systemctl restart nmea
sudo systemctl stop nmea
```

## Change Serial Port, Baud Rate, or Sentence Type
Option 1 (recommended): override service environment values in the unit file.

```bash
sudo systemctl edit --full nmea
# Update SONAR_SERIAL_PORT, SONAR_BAUD_RATE, and SONAR_SENTENCE_TYPE (dpt or dbt)
sudo systemctl daemon-reload
sudo systemctl restart nmea
```

Option 2: export environment values before running manually.

```bash
SONAR_SERIAL_PORT=/dev/ttyUSB1 SONAR_BAUD_RATE=115200 SONAR_SENTENCE_TYPE=dbt bash Script/autolaunch.sh
```

## Run Tests
From repository root:

```bash
bash Script/unittest.sh
```

## Notes
- The simulator writes one frame per cycle terminated by `\r\n`.
- If serial opening fails, the script logs the error and exits cleanly.
