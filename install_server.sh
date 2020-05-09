#!/bin/bash

read -r -d '' VAR << EOM
[Unit]
Description=Sensor connector to DB
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=8
User=pi
ExecStart=python3 /home/.sensors_python/script.py

[Install]
WantedBy=multi-user.target
EOM

mkdir /home/.sensors_python/script.py
cp server.py /home/.sensors_python/

echo "$VAR" > /etc/systemd/system/sensor_logger.service
cd /etc/systemd/system
chmod 644 sensor_logger.service
systemctl enable sensor_logger.service
systemctl stop sensor_logger.service
systemctl start sensor_logger.service
