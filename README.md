# Deckypad
Primarily made for use with the Steam Deck to allow its gamepad to be used on another PC remotely over a network.
You can use any network interface, be it Wifi/Ethernet/Bluetooth  but if you use bluetooth it much be setup to have a IP address.

This can be used on other PCs as well, they just need to have the requirement installed:

### Decky-client.py is used for the client side (deck):
pip requirements:
- pygame

### Decky-host.py is used for the server side (windows/linux):
pip requirements:
-  vgamepad
-  mouse
-  keyboard
  
# Usage:
### Client
#### method 1
- run Decky-client.py in your preferred python enviroment that has the requirement
- Insert your Hosts IP and Port into the input boxes
- click Connect
#### method 2
- run Decky-client.py in your preferred python enviroment that has the requirement
- assign an argument to the script,  Deckypad-client.py <Host IP>:<Port Number>
  this can also be achieved in gamemode,
- example:
  ```
  python  Deckypad-client.py 192.168.1.100:9090
  ```
### Host
#### method 1
- just run the script as
```
python Deckypad-host.py
```
- this runs on all interfaces and port 9090
#### method 2
- assign an interface and port using script arguments
```
python Deckypad-host.py <Port Number> <Host interface IP>
```


# What works:
- Network connection: client to server
- Gamepad detection and hotplugging
- Xbox360 Gamepad Emulation
- Mouse Emulation
- Keyboard Emulation

# TODO:
- Make a Virtual Playstation controller
- Create Bluetooth setup and network
- Finish the players section so multiple controllers can be used on the same PC without interference
- Add option to blackout screen
