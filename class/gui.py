import pygame, re
import Buttons, Textinputs

################################
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

###########################################

def setup_screen():
    SCREEN_W = 1280
    SCREEN_H = 800
    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
    pygame.display.set_caption("d[-_-]b's Wireless Gamepad")
    return screen

def joystick_instances(joysticks, event):
    if event.type == pygame.JOYDEVICEADDED:
        print(event)
        joy = pygame.joystick.Joystick(event.device_index)
        joysticks[joy.get_instance_id()] = joy
        print(f"Joystick {joy.get_instance_id()} connencted")

    if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        print(f"Joystick {event.instance_id} disconnected")
    return joysticks

def get_jot_data(Net, event):
    if event.type == pygame.QUIT:
        Net.sent_joy_data("close")
    if event.type == pygame.JOYBUTTONDOWN:
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

def output_joy_data(text_print, screen, joysticks):
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


def connection_screen_setup(_IP, _PORT):
    ClientNetworkButton_image = pygame.image.load("images/ClientNetworkButton.png").convert_alpha()
    ClientNetworkButton = Buttons.Button(640,200, ClientNetworkButton_image, 1, False)
    IPInputBox = Textinputs.Textbox(250, 430, 50, 50, 50, predefined_text=_IP)
    IPlabel = Textinputs.Textlabel(200,440, "IP: ", 50, (0,0,0))
    PortInputBox = Textinputs.Textbox(850, 430, 50,50, 50, predefined_text=_PORT)
    Portlabel = Textinputs.Textlabel(770,440, "Port: ", 50, (0,0,0))
    IPInputBox.visible = True
    PortInputBox.visible = True
    IPlabel.visible = True
    Portlabel.visible = True
    ClientNetworkButton.visible = True
    return (ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel)

def connection_screen_draw(screen, Net, ClientNetworkButton,IPInputBox,IPlabel,PortInputBox,Portlabel,port_regex,ip_regex):
    if ClientNetworkButton.draw(screen):
        if(re.search(ip_regex, IPInputBox.user_text)):
            if(re.search(port_regex, PortInputBox.user_text)):
                if Net.start_client(IPInputBox.user_text, int(PortInputBox.user_text)):
                    IPInputBox.visible = False
                    PortInputBox.visible = False
                    IPlabel.visible = False
                    Portlabel.visible = False
                    ClientNetworkButton.visible = False
                    return True
                else:
                    return False
    IPInputBox.draw(screen)
    PortInputBox.draw(screen)
    IPlabel.draw(screen)
    Portlabel.draw(screen)
    return False

def manual_mode_inputs(event, IPInputBox, PortInputBox):
    if event.type == pygame.KEYDOWN:
        if event.type == pygame.K_BACKSPACE or event.unicode == '\x08':
            IPInputBox.remove_char()
            PortInputBox.remove_char()
        else:
            IPInputBox.add_text(event.unicode)
            PortInputBox.add_text(event.unicode)

def setup_quit():
    Quit_button_image = pygame.image.load("images/QuitButton.png").convert_alpha()
    Quit_button = Buttons.Button((1280/2)-150,650, Quit_button_image, 0.5, True)
    return Quit_button

def draw_quit(screen,Net,Quit_button):
    if Quit_button.draw(screen):
        print("QUIT")
        if Net.connected == True and Net.mode == 0:
            Net.sent_joy_data("close")
        Net.kill_thread()
        return True
    return False
