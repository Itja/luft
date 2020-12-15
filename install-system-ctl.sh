#!/bin/bash
systemctl stop luft
cp luft.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable luft
if (systemctl start luft); then
  sleep 2
  if (systemctl is-active luft >/dev/null); then
    echo 'Luft service has been started successfully!'
  else
    echo 'ERROR: Failure after starting.'
  fi
  echo ''
  journalctl -u luft -n 5 -o short --no-pager
else
  echo 'ERROR: The updater service could not be started.'
fi
