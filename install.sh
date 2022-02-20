ln -s /home/quantum0/metrics-api-gateway/metrics-api-gateway.service /etc/systemd/system/metrics-api-gateway.service
systemctl daemon-reload
systemctl enable metrics-api-gateway
