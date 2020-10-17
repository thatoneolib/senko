#!/bin/bash
cd "$(dirname "$0")"
sudo python3.9 launch.py
ret=$?

if [ $ret -eq 25 ]; then
	git pull
fi

exit $ret
