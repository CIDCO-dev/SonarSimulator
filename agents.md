# agents.md - Contributor and Operator Guide (SonarSimulator)

This guide targets contributors (humans or agents) working in SonarSimulator.

## Goals
- Documentation policy: English only across repository docs.
- Track all notable changes in `version.md`, grouped by date.
- Keep contributor docs aligned with real behavior (`agents.md`, `README.md`, `version.md`).
- Make minimal and safe changes, then validate with executable checks.

## Tech Context
- Runtime: Python 3
- Serial I/O: `pyserial`
- Deployment: `systemd` service (`nmea.service`)
- Target platform: Ubuntu Server on Raspberry Pi (and compatible Linux hosts)

## Working Layout
- Simulator code: `Script/sonar_simulator.py`
- Service launcher: `Script/autolaunch.sh`
- Unit tests: `Script/sonar_simulator_unittest.py`
- Test runner: `Script/unittest.sh`
- Install script: `Install/install.sh`
- Hardware BOM: `BOM.txt`

## Development Rules
- Keep Python code PEP 8 compatible and easy to test.
- Avoid hard-coded assumptions when possible; use env vars for runtime config.
- Keep shell scripts POSIX/Bash-safe (`set -euo pipefail` for bash scripts).
- Use ASCII-only text in source/docs unless file already requires Unicode.

## Validation
- Run unit tests before finalizing:
  - `bash Script/unittest.sh`
- Validate Python syntax when touching scripts:
  - `python3 -m py_compile Script/sonar_simulator.py Script/sonar_simulator_unittest.py`

## Service Behavior
- `Install/install.sh` writes `/etc/systemd/system/nmea.service`.
- Default runtime values are configured by service env vars:
  - `SONAR_SERIAL_PORT=/dev/ttyUSB0`
  - `SONAR_BAUD_RATE=9600`
  - `SONAR_SENTENCE_TYPE=dpt` (`dpt` or `dbt`)
- After service changes always run:
  - `sudo systemctl daemon-reload`
  - `sudo systemctl restart nmea`

## Versioning Policy
- `VERSION` stores the current semantic version.
- `version.md` stores dated change history.
- New notes must be added under the current date section.

## Review Checklist
- [ ] Unit tests pass (`bash Script/unittest.sh`)
- [ ] README commands match current scripts/paths
- [ ] Service install flow tested or reason documented
- [ ] `version.md` updated for notable behavior changes
- [ ] `agents.md` updated if contributor workflow changed
