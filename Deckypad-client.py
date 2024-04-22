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
    Blackout_button = gui.setup_blackout()
    _bg = gui.setup_bg()
    blackout = False
    if _manual == 0:
        ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel = gui.connection_screen_setup(str(Net.HOST),str(Net.PORT))
        Blackout_button.visible = False
    while True:
        try:
            for event in pygame.event.get():
                if not blackout and _manual == 1: screen.blit(_bg[0],_bg[1])
                else:
                    screen.fill((0,0,0))
                    if _manual == 1:
                        if gui.look_for_screen_tap(event):
                            blackout = False
                            Quit_button.visible = True
                            Blackout_button.visible = True
                            break
                joysticks = gui.joystick_instances(joysticks, event)
                if gui.draw_quit(screen, Net, Quit_button):
                    return
                if gui.draw_blackout(screen,Blackout_button):
                    blackout = True
                    Quit_button.visible = False
                    Blackout_button.visible = False
                    break
                if _manual == 0:
                    if gui.connection_screen_draw(screen,Net,ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel, port_regex, ip_regex):
                        _manual = 1
                        Blackout_button.visible = True
                    gui.manual_mode_inputs(event, IPInputBox, PortInputBox)
                else:
                    gui.get_jot_data(Net, event)
                    gui.get_mouse_events(Net, event)
                    gui.get_keyboard_events(Net, event)
                    gui.output_joy_data(text_print, screen, joysticks)
        except Exception as ex:
            print(ex)
            _manual = 0
            Net.mode = -1
            Net.connected = False
            ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel = gui.connection_screen_setup(str(Net.HOST),str(Net.PORT))
            Quit_button.visible = True
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    help = ["-h", "-?", "/?", "/h", "--help", "-help", "help"]
    if len(sys.argv) > 3:
        _help()
    else:
        for x in sys.argv:
            if x in help:
                _help()
    if len(sys.argv) >= 2:
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
        if len(sys.argv) == 2:
            Net.start_client(str(Net.HOST), int(Net.PORT))
        else:
            controlelrs_valid = ["xbox", "ds4"]
            if sys.argv[2] in controlelrs_valid:
                Net.start_client(str(Net.HOST), int(Net.PORT), controller=sys.argv[2])
            else:
                print("\nInvalid controller selection\n- you can select from : \n"+str(controlelrs_valid)+"\n Defaults to 'xbox'")
                os._exit(0)
        main(1)
    else:
        main(0)
        os._exit(0)
