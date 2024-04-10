#!/usr/bin/python3
import sys, os, time, re
sys.path.append(os.path.dirname(sys.argv[0])+"/class/")
import pygame
import Buttons, Textinputs
pygame.init()


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

ButtonMap = {
    "0": "JA",
    "1": "JB",
    "2": "JX",
    "3": "JY",
    "4": "L1",
    "5": "R1",
    "6": "Se",
    "7": "St",
    "8": "Gu",
    "9": "R3",
    "10": "L3",
    "A0": "LH",
    "A1": "LV",
    "A2": "LT",
    "A3": "RH",
    "A4": "RV",
    "A5": "RT"
}
Axis = {
 "LS": [0.0,0.0],
 "RS": [0.0,0.0],
 "RT": 0.0,
 "LT": 0.0
}
axis_ = 0.05
def axis_tres(new, old):
    test = new - old
    if test > axis_ or test < -axis_:
        return True
    return False

def main():
    SRCREEN_W = 1280
    SCREEN_H = 800

    screen = pygame.display.set_mode((SRCREEN_W,SCREEN_H))
    pygame.display.set_caption("d[-_-]b's Wireless Gamepad")

    Wifi_button_image = pygame.image.load("images/WifiStartButton.png").convert_alpha()
    Bluetooth_button_image = pygame.image.load("images/BluetoothStartButton.png").convert_alpha()
    Quit_button_image = pygame.image.load("images/QuitButton.png").convert_alpha()
    Wifi_button = Buttons.Button(140,200, Wifi_button_image, 1, True)
    Bluetooth_button = Buttons.Button(640,200, Bluetooth_button_image, 1, True)
    Quit_button = Buttons.Button((1280/2)-150,650, Quit_button_image, 0.5, True)

    HostNetworkButton_image = pygame.image.load("images/HostNetworkButton.png").convert_alpha()
    ClientNetworkButton_image = pygame.image.load("images/ClientNetworkButton.png").convert_alpha()
    HostNetworkButton = Buttons.Button(140,200, HostNetworkButton_image, 1, False)
    ClientNetworkButton = Buttons.Button(640,200, ClientNetworkButton_image, 1, False)

    network_pressed = False
    Net = None
    IPInputBox = Textinputs.Textbox(250, 430, 50, 50, 50, predefined_text="192.168.1.203")
    IPlabel = Textinputs.Textlabel(200,440, "IP: ", 50, (0,0,0))
    PortInputBox = Textinputs.Textbox(850, 430, 50,50, 50, predefined_text="666")
    Portlabel = Textinputs.Textlabel(770,440, "Port: ", 50, (0,0,0))
    ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    port_regex = "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"

    clock = pygame.time.Clock()
    text_print = TextPrint()
    joysticks = {}
    while True:
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if Net != None:
                    if Net.connected == True and Net.mode == 0:
                        Net.sent_joy_data("close")
                    Net.kill_thread()
                return

            if Net != None:
                if Net.connected == True and Net.mode == 0:
                #     Net.sent_joy_data(event)
                    if event.type == pygame.JOYBUTTONDOWN:
                        #joystick = joysticks[event.instance_id]
                        # if event.button == 0:
                        #     if joystick.rumble(0, 0.7, 500): pass
                        Net.sent_joy_data("D:"+ButtonMap[str(event.button)]+"|")
                    elif event.type == pygame.KEYDOWN:
                        Net.sent_joy_data("K:"+ButtonMap[str(event.key)]+"|")

                    elif event.type == pygame.JOYBUTTONUP  or event.type == pygame.KEYUP:
                        Net.sent_joy_data("R:"+ButtonMap[str(event.button)]+"|")
                    elif event.type == pygame.JOYHATMOTION:
                        Net.sent_joy_data("H:"+str(event.hat)+":"+str(event.value[0])+","+str(event.value[1])+"|")
                    elif event.type == pygame.JOYAXISMOTION:
                        if ButtonMap["A"+str(event.axis)] == "LV":
                            if axis_tres(event.value, Axis["LS"][1]):
                                Axis["LS"][1] = event.value
                                Net.sent_joy_data("A:"+"LS"+":"+str(Axis["LS"][0])+","+str(Axis["LS"][1])+"|")
                        elif ButtonMap["A"+str(event.axis)] == "LH":
                            if axis_tres(event.value, Axis["LS"][0]):
                                Axis["LS"][0] = event.value
                                Net.sent_joy_data("A:"+"LS"+":"+str(Axis["LS"][0])+","+str(Axis["LS"][1])+"|")
                        elif ButtonMap["A"+str(event.axis)] == "RV":
                            if axis_tres(event.value, Axis["RS"][1]):
                                Axis["RS"][1] = event.value
                                Net.sent_joy_data("A:"+"RS"+":"+str(Axis["RS"][0])+","+str(Axis["RS"][1])+"|")
                        elif ButtonMap["A"+str(event.axis)] == "RH":
                            if axis_tres(event.value, Axis["RS"][0]):
                                Axis["RS"][0] = event.value
                                Net.sent_joy_data("A:"+"RS"+":"+str(Axis["RS"][0])+","+str(Axis["RS"][1])+"|")
                        elif ButtonMap["A"+str(event.axis)] == "RT":
                            if axis_tres(event.value, Axis["RT"]):
                                Axis["RT"] = event.value
                                Net.sent_joy_data("T:"+"RT"+":"+str(event.value)+"|")
                        elif ButtonMap["A"+str(event.axis)] == "LT":
                            if axis_tres(event.value, Axis["LT"]):
                                Axis["LT"] = event.value
                                Net.sent_joy_data("T:"+"LT"+":"+str(event.value)+"|")

                elif event.type == pygame.KEYDOWN:
                    print("menu")
                    if event.type == pygame.K_BACKSPACE or event.unicode == '\x08':
                        IPInputBox.remove_char()
                        PortInputBox.remove_char()
                    else:
                        IPInputBox.add_text(event.unicode)
                        PortInputBox.add_text(event.unicode)

            if event.type == pygame.JOYDEVICEADDED:
                print(event)
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")


        screen.fill((202,228,241))
        if Net != None:
            if Net.connected == True and Net.mode == 0:
                text_print.reset()
                joystick_count = pygame.joystick.get_count()
                text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
                text_print.indent()
                for joystick in joysticks.values():
                    jid = joystick.get_instance_id()
                    text_print.tprint(screen, f"Joystick {jid}")
                    text_print.indent()
                    name = joystick.get_name()
                    text_print.tprint(screen, f"Joystick name: {name}")
                    guid = joystick.get_guid()
                    text_print.tprint(screen, f"GUID: {guid}")
                    power_level = joystick.get_power_level()
                    text_print.tprint(screen, f"Joystick's power level: {power_level}")
                    axes = joystick.get_numaxes()
                    text_print.tprint(screen, f"Number of axes: {axes}")
                    text_print.indent()
                    for i in range(axes):
                        axis = joystick.get_axis(i)
                        text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
                    text_print.unindent()
                    buttons = joystick.get_numbuttons()
                    text_print.tprint(screen, f"Number of buttons: {buttons}")
                    text_print.indent()
                    for i in range(buttons):
                        button = joystick.get_button(i)
                        text_print.tprint(screen, f"Button {i:>2} value: {button}")
                    text_print.unindent()
                    hats = joystick.get_numhats()
                    text_print.tprint(screen, f"Number of hats: {hats}")
                    text_print.indent()
                    for i in range(hats):
                        hat = joystick.get_hat(i)
                        text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
                    text_print.unindent()
                    text_print.unindent()

        if not network_pressed:
            if Bluetooth_button.draw(screen):
                print("pressed Bluetooth")
        else:
            if HostNetworkButton.draw(screen):
                if Net != None:
                    if(re.search(port_regex, PortInputBox.user_text)):
                        if Net.start_host(int(PortInputBox.user_text)):
                            IPInputBox.visible = False
                            PortInputBox.visible = False
                            IPlabel.visible = False
                            Portlabel.visible = False
                            HostNetworkButton.visible = False
                            ClientNetworkButton.visible = False
                            print("host okay")
                        else:
                            print("hostfailed")
            if ClientNetworkButton.draw(screen):
                if Net != None:
                    if(re.search(ip_regex, IPInputBox.user_text)):
                        if(re.search(port_regex, PortInputBox.user_text)):
                            if Net.start_client(IPInputBox.user_text, int(PortInputBox.user_text)):
                                IPInputBox.visible = False
                                PortInputBox.visible = False
                                IPlabel.visible = False
                                Portlabel.visible = False
                                HostNetworkButton.visible = False
                                ClientNetworkButton.visible = False
                                print("client okay")
                            else:
                                print("client failed")
            IPInputBox.draw(screen)
            PortInputBox.draw(screen)
            IPlabel.draw(screen)
            Portlabel.draw(screen)
        if Wifi_button.draw(screen):
            print("pressed WIFI")
            network_pressed = True
            pygame.mouse.set_pos(0,0)
            import Network
            Net = Network.Manage()
            IPInputBox.visible = True
            PortInputBox.visible = True
            IPlabel.visible = True
            Portlabel.visible = True

        if Quit_button.draw(screen):
            print("QUIT")
            if Net != None:
                if Net.connected == True and Net.mode == 0:
                    Net.sent_joy_data("close")
                Net.kill_thread()
            return


        pygame.display.flip()

        clock.tick(90)


if __name__ == "__main__":
    main()
    sys.exit()
    pygame.quit()
