#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo apt update
sudo apt install -y python3 python3-pip python3-serial

sudo tee /etc/systemd/system/nmea.service >/dev/null <<EOF
[Unit]
Description=Launch NMEA Simulator on boot.
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${PROJECT_ROOT}
Environment=SONAR_SERIAL_PORT=/dev/ttyUSB0
Environment=SONAR_BAUD_RATE=9600
Environment=SONAR_SENTENCE_TYPE=dpt
ExecStart=${PROJECT_ROOT}/Script/autolaunch.sh
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

sudo chmod 644 /etc/systemd/system/nmea.service
sudo systemctl daemon-reload
sudo systemctl enable nmea
sudo systemctl restart nmea
sudo systemctl --no-pager --full status nmea
