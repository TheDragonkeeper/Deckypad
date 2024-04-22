import vgamepad as vg
import time
import mouse
import keyboard

class Gamepad():
    def __init__(self):
        self.mouseleft = 0
        self.displayscale = 1.7777
        self.pads = {}
        self.ButtonMap = { "xbox": {
            "JA": self.useA,
            "JB": self.useB,
            "JX": self.useX,
            "JY": self.useY,
            "L1": self.useL1,
            "R1": self.useR1,
            "Se": self.useSe,
            "St": self.useSt,
            "Gu": self.useGu,
            "R3": self.useR3,
            "L3": self.useL3,
            "LS": self.useLS,
            "LT": self.useLT,
            "RS": self.useRS,
            "RT": self.useRT,
            "DL": self.useDL,
            "DR": self.useDR,
            "DU": self.useDU,
            "DD": self.useDD
        },
        "ds4": {
            "JA": self.ds4useA,
            "JB": self.ds4useB,
            "JX": self.ds4useX,
            "JY": self.ds4useY,
            "L1": self.ds4useL1,
            "R1": self.ds4useR1,
            "Se": self.ds4useSe,
            "St": self.ds4useSt,
            "Gu": self.ds4useGu,
            "R3": self.ds4useR3,
            "L3": self.ds4useL3,
            "LS": self.ds4useLS,
            "LT": self.ds4useLT,
            "RS": self.ds4useRS,
            "RT": self.ds4useRT,
            "DP": self.ds4useDP
        },
        }

    def init_pad(self, player, controller):
        self.pads[player] = {}
        if controller == "xbox":
            self.pads[player]["pad"] = vg.VX360Gamepad()
            self.pads[player]["type"] = "xbox"
        elif controller == "ds4":
            self.pads[player]["pad"] = vg.VDS4Gamepad()
            self.pads[player]["type"] = "ds4"
        self.wake(self.pads[player]["pad"])
        self.wake(self.pads[player]["pad"])
        self.wake(self.pads[player]["pad"])

    def wake(self, player):
        player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        player.update()
        time.sleep(0.5)
        player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        player.update()
        time.sleep(0.5)
        player.left_trigger_float(float(1))
        player.left_trigger_float(float(0))

    def killpad(self, player):
        if player in self.pads:
            self.pads.pop(player, None)

    def handle_reciecved(self, player, netrequest):
        padtype = self.pads[player]["type"]
        player = self.pads[player]["pad"]
        requests = str(netrequest).split("|")
        for request in requests:
            action = request.split(":")
            if len(action) == 2:
                if str(action[0]) == "D":
                    if str(action[1]) in self.ButtonMap[padtype]:
                        self.ButtonMap[padtype][str(action[1])](player,1)
                elif str(action[0]) == "R":
                    if str(action[1]) in self.ButtonMap[padtype]:
                        self.ButtonMap[padtype][str(action[1])](player,0)
            elif len(action) == 3:
                if str(action[0]) == "K":
                    if action[2] == "1":
                        keyboard.write(str(action[1]).upper())
                    else:
                        keyboard.write(action[1])
                elif str(action[0]) == "A":
                    if str(action[1]) in self.ButtonMap[padtype]:
                        values = str(action[2]).split(",")
                        if len(values) == 2:
                            if values[0] != "" and values[1] != "" and values[0] != "-" and values[1] != "-" and values[0] != "0." and values[1] != "0.":
                                self.ButtonMap[padtype][str(action[1])](player,[float(values[0]),float(values[1])])
                elif str(action[0]) == "T":
                    if str(action[1]) in self.ButtonMap[padtype]:
                        if str(action[2]) != "-" and str(action[2]) != "" and str(action[2]) != "0.":
                            self.ButtonMap[padtype][str(action[1])](player,float(action[2]))
                elif str(action[0]) == "H":
                    hat = str(action[1])
                    value = str(action[2]).split(",")
                    if padtype == "ds4":
                        self.ButtonMap[padtype]["DP"](player,value)
                    elif value == ["1","1"]:
                        self.ButtonMap[padtype]["DR"](player,1)
                        self.ButtonMap[padtype]["DU"](player,1)
                        self.ButtonMap[padtype]["DL"](player,0)
                        self.ButtonMap[padtype]["DD"](player,0)
                    elif value == ["0","1"]:
                        self.ButtonMap[padtype]["DU"](player,1)
                        self.ButtonMap[padtype]["DL"](player,0)
                        self.ButtonMap[padtype]["DD"](player,0)
                        self.ButtonMap[padtype]["DR"](player,0)
                    elif value == ["-1","1"]:
                        self.ButtonMap[padtype]["DR"](player,0)
                        self.ButtonMap[padtype]["DL"](player,1)
                        self.ButtonMap[padtype]["DD"](player,0)
                        self.ButtonMap[padtype]["DU"](player,1)
                    elif value == ["-1","0"]:
                        self.ButtonMap[padtype]["DL"](player,1)
                        self.ButtonMap[padtype]["DD"](player,0)
                        self.ButtonMap[padtype]["DU"](player,0)
                        self.ButtonMap[padtype]["DR"](player,0)
                    elif value == ["-1","-1"]:
                        self.ButtonMap[padtype]["DD"](player,1)
                        self.ButtonMap[padtype]["DL"](player,1)
                        self.ButtonMap[padtype]["DU"](player,0)
                        self.ButtonMap[padtype]["DR"](player,0)
                    elif value == ["0","-1"]:
                        self.ButtonMap[padtype]["DL"](player,0)
                        self.ButtonMap[padtype]["DD"](player,1)
                        self.ButtonMap[padtype]["DU"](player,0)
                        self.ButtonMap[padtype]["DR"](player,0)
                    elif value == ["0","0"]:
                        self.ButtonMap[padtype]["DL"](player,0)
                        self.ButtonMap[padtype]["DD"](player,0)
                        self.ButtonMap[padtype]["DU"](player,0)
                        self.ButtonMap[padtype]["DR"](player,0)
                    elif value == ["1","-1"]:
                        self.ButtonMap[padtype]["DL"](player,0)
                        self.ButtonMap[padtype]["DD"](player,1)
                        self.ButtonMap[padtype]["DU"](player,0)
                        self.ButtonMap[padtype]["DR"](player,1)
                    elif value == ["1","0"]:
                        self.ButtonMap[padtype]["DL"](player,0)
                        self.ButtonMap[padtype]["DD"](player,0)
                        self.ButtonMap[padtype]["DU"](player,0)
                        self.ButtonMap[padtype]["DR"](player,1)
            elif len(action) == 4:
                if str(action[0]) == "M":
                    if str(action[1]) == "M":
                        try:
                            x = float(action[2]) * self.displayscale
                            y = float(action[3]) * self.displayscale
                            mouse.move(x, y, absolute=True)
                        except: pass
                    if str(action[1]) == "B":
                        if action[2] == "1":
                            if action[3] == "0":
                                self.mouseleft = 0
                                mouse.release(button='left')
                            else:
                                self.mouseleft = 1
                                mouse.press(button='left')
                        elif action[2] == "2":
                            if action[3] == "0":
                                mouse.release(button='middle')
                            else:
                                mouse.press(button='middle')
                        elif action[2] == "3":
                            if action[3] == "0":
                                mouse.release(button='right')
                            else:
                                mouse.press(button='right')
                        elif action[2] == "4":
                            if action[3] == "1":
                                mouse.wheel(1)
                        elif action[2] == "5":
                            if action[3] == "1":
                                mouse.wheel(-1)
        player.update()
    def useA(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    def useB(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    def useX(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X )
    def useY(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y )
    def useL1(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER )
    def useR1(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER )
    def useSe(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK )
    def useSt(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START )
    def useGu(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE )
    def useR3(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB )
    def useL3(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB )
    def useLS(self, player, values):
        player.left_joystick_float(x_value_float=float(values[0]), y_value_float=float(values[1]))
    def useLT(self, player, value):
        player.left_trigger_float(value_float=float(value))
    def useRS(self, player, values):
        player.right_joystick_float(x_value_float=float(values[0]), y_value_float=float(values[1]))
    def useRT(self, player, value):
        player.right_trigger_float(value_float=float(value))
    def useDL(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT )
    def useDR(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT )
    def useDU(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP )
    def useDD(self, player, state):
        if state == 1: player.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN )
        else: player.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN )


    def ds4useA(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS )
    def ds4useB(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE )
    def ds4useX(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE  )
    def ds4useY(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE )
    def ds4useL1(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT  )
    def ds4useR1(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT  )
    def ds4useSe(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE  )
    def ds4useSt(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS  )
    def ds4useGu(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS  )
    def ds4useR3(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT  )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT )
    def ds4useL3(self, player, state):
        if state == 1: player.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT )
        else: player.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT  )
    def ds4useLS(self, player, values):
        player.left_joystick_float(float(values[0]), float(values[1]))
    def ds4useLT(self, player, value):
        player.left_trigger_float(float(value))
    def ds4useRS(self, player, values):
        player.right_joystick_float(float(values[0]), float(values[1]))
    def ds4useRT(self, player, value):
        player.right_trigger_float(float(value))
    def ds4useDP(self, player, value):
        if value == ["1","1"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST )
        elif value == ["0","1"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH )
        elif value == ["-1","1"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST )
        elif value == ["-1","0"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST)
        elif value == ["-1","-1"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST )
        elif value == ["0","-1"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH )
        elif value == ["0","0"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE )
        elif value == ["1","-1"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST )
        elif value == ["1","0"]:
            player.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST )
