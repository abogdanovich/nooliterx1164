# nooliterx1164
nooliterx1164 usb adapter

- install pyusb 
- download the code into your server folder
- setup rules for noolite USB device

example: /etc/udev/rules.d/50-noolite.rules

ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", SUBSYSTEMS=="usb", ACTION=="add", MODE="0666", GROUP="dialout"
ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05dc", SUBSYSTEMS=="usb", ACTION=="add", MODE="0666", GROUP="dialout"

notes:
05df > PCxxxx usb adapter
05dc > RXxxxx usb adapter

- Add your server-user to dialout group > sudo usermod <user> -a -G dialout

- connect usb stick to your server
- run sript: python nooliterx.py or take the provided code you want

Have a nice day :)
