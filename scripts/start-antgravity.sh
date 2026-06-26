#!/usr/bin/env bash
# If the Antigravity systemd unit is not active, start it
if ! systemctl is-active --quiet antgravity.service; then
    sudo systemctl start antgravity.service
fi

# Wait until the HTTP health endpoint answers
until curl -s http://127.0.0.1:4242/status > /dev/null; do
    sleep 0.5
done

echo "Antigravity is up"
