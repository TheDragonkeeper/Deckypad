#!/usr/bin/env python

import sys, os, re, time
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/class/")

import Network
Net = Network.Manage()
import signal

port_regex = "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

import pygame
import Textoutputs
pygame.init()
import gui

def signal_handler(sig, frame):
    print('\n\nYou pressed Ctrl+C\nDeckypad has stopped')
    os._exit(0)

def _help():
    print("This is the client side of Deckypad")
    print("----------------------------------")
    print("Usage:  python3 Deckypad-client.py <Host IP>:<Port Number>\n")
    sys.exit(0)



def main(_manual):
    global Net
    joysticks = {}
    screen = gui.setup_screen()
    clock = pygame.time.Clock()
    fps = 90
    text_print = Textoutputs.TextPrint()
    print("Running Deckypad , connecting to "+str(Net.HOST)+":"+str(Net.PORT))
    print('\nSend SIGINT or Press Ctrl+C at anytime to quit')
    signal.signal(signal.SIGINT, signal_handler)
    ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel = None,None,None,None,None
    Quit_button = gui.setup_quit()
    if _manual == 0: ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel = gui.connection_screen_setup(str(Net.HOST),str(Net.PORT))
    while True:
        try:
            for event in pygame.event.get():
                screen.fill((202,228,241))
                joysticks = gui.joystick_instances(joysticks, event)
                if gui.draw_quit(screen, Net, Quit_button):
                    return
                if _manual == 0:
                    if gui.connection_screen_draw(screen,Net,ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel, port_regex, ip_regex):
                        _manual = 1
                    gui.manual_mode_inputs(event, IPInputBox, PortInputBox)
                else:
                    gui.get_jot_data(Net, event)
                    gui.get_mouse_events(Net, event)
                    gui.output_joy_data(text_print, screen, joysticks)
        except Exception as ex:
            print(ex)
            _manual = 0
            Net.mode = -1
            Net.connected = False
            ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel = gui.connection_screen_setup(str(Net.HOST),str(Net.PORT))
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    help = ["-h", "-?", "/?", "/h", "--help", "-help", "help"]
    if len(sys.argv) > 2:
        _help()
    else:
        for x in sys.argv:
            if x in help:
                _help()
    if len(sys.argv) == 2:
        good = True
        if not ":" in sys.argv[1]:
            _help()
        host = sys.argv[1].split(":")
        if not re.search(port_regex, host[1]):
            print("invalid port number\n")
            good = False
        else:
            Net.PORT = host[1]
        if not re.search(ip_regex, host[0]):
            print("invalid IP\n")
            good = False
        else:
            Net.HOST = host[0]
        if not good:
            _help()
        Net.start_client(str(Net.HOST), int(Net.PORT))
        main(1)
    else:
        main(0)
        os._exit(0)
