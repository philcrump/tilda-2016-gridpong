### Author: Phil Crump
### Description: Pong Control for The Grid
### Category: comms
### License: MIT
### Appname : TheGrid_Pong

import dialogs
from database import *
import buttons
import ugfx
from http_client import *
import wifi

ugfx.init()
width = ugfx.width()
height = ugfx.height()
buttons.init()

win_header = ugfx.Container(0,0,width,33)
win_main = ugfx.Container(0,35,width,height-35)

components = [win_header, win_main]
ugfx.set_default_font(ugfx.FONT_TITLE)
components.append(ugfx.Label(3,3,width-10,29,"The·Grid Pong",parent=win_header))

win_main.show()
win_header.show()

ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
label_player_id = ugfx.Label(30,10+35,240,25,"Set Player Id (left/right):")
label_auth_code = ugfx.Label(30,35+35,240,25,"Set Auth Code (up/down):")
field_connecting_status = ugfx.Label(30,60+35,240,25,"Press A to connect")

player_id = 0 # 0=Left, 1=Right
auth_code = 0

ugfx.set_default_font(ugfx.FONT_MEDIUM)
field_player_id = ugfx.Label(250,10+35,100,25,"LEFT")
field_auth_code = ugfx.Label(250,35+35,100,25,str(auth_code))

def http_assoc():
    urlparams = "app=pong&player="+str(player_id)+"&auth="+str(auth_code)
    while True:
        wifi_spinner = "-"
        while not wifi.nic().is_connected():
            field_connecting_status.destroy()
            field_connecting_status = ugfx.Label(30,60+35,85,25,"Waiting for WiFi.. "+wifi_spinner)
            if(wifi_spinner=="-"):
                wifi_spinner = "|"
            else:
                wifi_spinner = "-"
            pyb.wfi()
            pyb.delay(500)
        try:
            with post("http://control.thegrid.fish/api/ui", urlencoded=urlparams) as response:
	            if response.status==200:
	                return 0
	            elif response.status==403:
	                #Access Denied
	                return 1
	            elif response.status==400:
	                #Bad Request
	                return 2
	            else:
	                return 99
        except:
            field_connecting_status.destroy()
            field_connecting_status = ugfx.Label(30,60+35,85,25,"HTTP Error! Retrying..")

def http_move(direction):
    urlparams = "app=pong&player="+str(player_id)+"&auth="+str(auth_code)+"&move="+direction
    while True:
        wifi_spinner = "-"
        while not wifi.nic().is_connected():
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Waiting for WiFi.. "+wifi_spinner)
            if(wifi_spinner=="-"):
                wifi_spinner = "|"
            else:
                wifi_spinner = "-"
            pyb.wfi()
            pyb.delay(500)
        try:
            with post("http://control.thegrid.fish/api/ui", urlencoded=urlparams) as response:
	            if response.status==200:
	                return 0
	            elif response.status==403:
	                #Access Denied
	                return 1
	            elif response.status==400:
	                #Bad Request
	                return 2
	            else:
	                return response.status
        except:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"HTTP Error! Retrying..")

connecting_state = 1
while connecting_state:
    if buttons.is_triggered("JOY_LEFT"):
        if player_id >0:
            player_id = 0
            field_player_id.destroy()
            field_player_id = ugfx.Label(250,10+35,100,25,"LEFT")
    elif buttons.is_triggered("JOY_RIGHT"):
        if player_id <1:
            player_id = 1
            field_player_id.destroy()
            field_player_id = ugfx.Label(250,10+35,100,25,"RIGHT")
    elif buttons.is_triggered("JOY_UP"):
        if auth_code <6:
            auth_code = auth_code + 1
            field_auth_code.destroy()
            field_auth_code = ugfx.Label(250,35+35,100,25,str(auth_code))
    elif buttons.is_triggered("JOY_DOWN"):
        if auth_code >1:
            auth_code = auth_code - 1
            field_auth_code.destroy()
            field_auth_code = ugfx.Label(250,35+35,100,25,str(auth_code))
    elif buttons.is_triggered("BTN_A"):
        ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
        wifi_spinner = "-"
        while not wifi.nic().is_connected():
            field_connecting_status.destroy()
            field_connecting_status = ugfx.Label(30,60+35,250,25,"Waiting for WiFi.. "+wifi_spinner)
            if(wifi_spinner=="-"):
                wifi_spinner = "|"
            else:
                wifi_spinner = "-"
            pyb.delay(500)
        field_connecting_status.destroy()
        field_connecting_status = ugfx.Label(30,60+35,250,25,"Connecting to Grid..")
        assoc_return = http_assoc()
        if assoc_return == 0:
            #Connected!
            field_connecting_status.destroy()
            field_connecting_status = ugfx.Label(30,60+35,240,25,"Connected!")
            connecting_state = 0
            pyb.delay(750)
        else:
            ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            # Failed
            if assoc_return == 1:
                field_connecting_status.destroy()
                field_connecting_status = ugfx.Label(30,60+35,240,25,"Access Denied")
            elif assoc_return == 2:
                field_connecting_status.destroy()
                field_connecting_status = ugfx.Label(30,60+35,240,25,"Bad Request")
            else:
                field_connecting_status.destroy()
                field_connecting_status = ugfx.Label(30,60+35,240,25,"Unknown Error: "+assoc_return)
            pyb.delay(1000)
            field_connecting_status.destroy()
            field_connecting_status = ugfx.Label(30,60+35,240,25,"Press A to connect")

label_player_id.destroy()
field_player_id.destroy()
label_auth_code.destroy()
field_auth_code.destroy()
field_connecting_status.destroy()

label_instructions = ugfx.Label(30,10+35,300,25,"Joystick up/down to move paddle")
label_exit = ugfx.Label(30,35+35,250,25,"Press B twice to exit")
field_connection = ugfx.Label(30,60+35,85,25,"-")

run = 1
b_presses = 0
while run:
    if buttons.is_triggered("JOY_UP"):
        if b_presses:
            b_presses = 0
            label_exit.destroy()
            label_exit = ugfx.Label(30,35+35,250,25,"Press B twice to exit")
        move_return = http_move("UP")
        ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
        if move_return == 0:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"-")
        elif move_return == 1:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Access Denied")
        elif move_return == 2:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Bad Request")
        elif move_return == 99:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Unknown Error")
    elif buttons.is_triggered("JOY_DOWN"):
        if b_presses:
            b_presses = 0
            label_exit.destroy()
            label_exit = ugfx.Label(30,35+35,250,25,"Press B twice to exit")
        move_return = http_move("DOWN")
        ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
        if move_return == 0:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"/")
        elif move_return == 1:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Access Denied")
        elif move_return == 2:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Bad Request")
        else:
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Unknown Error: "+move_return)
    elif buttons.is_triggered("BTN_B"):
        if b_presses:
            move_return = http_move("DISCONNECT")
            ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            field_connection.destroy()
            field_connection = ugfx.Label(30,60+35,85,25,"Exiting..")
            run = 0
        else:
            b_presses = 1
            label_exit.destroy()
            label_exit = ugfx.Label(30,35+35,250,25,"Press B again to exit!")

label_instructions.destroy()
label_exit.destroy()
field_connection.destroy()
for component in components:
	component.destroy()
