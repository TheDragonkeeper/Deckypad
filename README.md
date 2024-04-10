# Deckypad
Primarily made for use with the Steam Deck to allow its gamepad to be used on another PC remotely over wifi/bluetooth
but can be used on other PCs as well. This needs to be running on both machines.

pip requirements:
-  vgamepad - install on host only
-  pygame - install on host and client

Usage:
- run Deckypad.py in your preferred python enviroment
- Select WIFI
- Assign a port and select Host on the gaming device
- Assign IP for gaming device, use the same port and select Client on the client device

Works with steam input the best on steam deck for the built in controller but can work for other devices attached.

its locked to 90fps but the steam deck can limit this lower if needed. The more fps the lower the input latancy but also the higher network traffic. I found that 90 was smooth, 60 was good enough, 30 can start getting some noticable delays.

# What works:
- Network connection: client to server
- Gamepad detection and hotplugging
- Xbox360 Gamepad Emulation

# TODO:
- Make a Virtual Playstation controller
- Create Bluetooth setup and network
- Finish the players section so multiple controllers can be used on the same PC without interference
- Add option to blackout screen
- Add Keyboard inputs
- Add mouse inputs
- Add touchscreen inputs
