# Version History (English)

## 2026-02-19
- docs: rewrote `README.md` with accurate manual run, service install, configuration, and test instructions.
- docs: added `agents.md` contributor/operator guide with validation and versioning policy.
- versioning: added `VERSION` file to store current semantic version.
- simulator: refactored `Script/sonar_simulator.py` for safer serial handling, CLI arguments (`--interval`, `--iterations`), and testable loop behavior.
- tests: fixed and expanded `Script/sonar_simulator_unittest.py` to validate emitted frames and serial-open failure handling.
- scripts: updated `Script/autolaunch.sh`, `Script/unittest.sh`, and `Install/install.sh` for robust bash usage and reliable systemd deployment.
- repo: updated `.gitignore` to ignore Python cache artifacts (`__pycache__/`, `*.pyc`).
- simulator: added NMEA sentence selection (`--sentence-type dpt|dbt`) and DBT frame generation support.
- scripts/service: added `SONAR_SENTENCE_TYPE` support in `Script/autolaunch.sh` and `Install/install.sh`.
- tests: added DBT coverage and sentence-type validation in `Script/sonar_simulator_unittest.py`.
- repo: renamed files to remove `DPT` from filenames (`Script/sonar_simulator.py`, `Script/sonar_simulator_unittest.py`).
