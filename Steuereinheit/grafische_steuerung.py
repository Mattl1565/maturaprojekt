import threading
import time

import pygame
import pygame_menu as pm
import paho.mqtt.client as mqtt

import Utils.find_ipv4_adress as ip

broker_address = ip.useful_functions.get_ip_address()
port = 1883

start_detection = False
take_fake_video_input = True
take_fake_photo_input = True

check_for_overtakes = False
check_for_direction = False

drone_height = 0
drone_angle = 0


pygame.init()

# Screen
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Standard RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main(client):


    graphics = [("Low", "low"),
                ("Medium", "medium"),
                ("High", "high"),
                ("Ultra High", "ultra high")]

    def printSettings():
        print("\n\n")
        # getting the data using "get_input_data" method of the Menu class
        settingsData = settings.get_input_data()

        for key in settingsData.keys():
            print(f"{key}\t:\t{settingsData[key]}")

    def refreshSettings():
        print("funny mqtt")

    settings = pm.Menu(title="Einstellungen",
                       width=WIDTH,
                       height=HEIGHT,
                       theme=pm.themes.THEME_BLUE)

    # Adjusting the default values
    settings._theme.widget_font_size = 25
    settings._theme.widget_font_color = BLACK
    settings._theme.widget_alignment = pm.locals.ALIGN_CENTER

    # Range slider that lets to choose a value using a slider
    settings.add.range_slider(title="Drone Height[m]", default=5, range_values=(
        0, 10), increment=0.5, value_format=lambda x: str(int(x)), rangeslider_id="drone_height")

    settings.add.range_slider(title="Drone Angle[°]", default=45, range_values=(
       0, 90), increment=0.5, value_format=lambda x: str(int(x)), rangeslider_id="drone_angle")

    settings.add.toggle_switch(
        title="Overtake Detection", default=True, toggleswitch_id="overtake_detection")
    settings.add.toggle_switch(
        title="Ground Camera Usage", default=False, toggleswitch_id="ground_cam_usage")
    settings.add.toggle_switch(
        title="Direction Detection", default=False, toggleswitch_id="direction_detection")
    settings.add.toggle_switch(
        title="Speed Detection", default=False, toggleswitch_id="speed_detection")
    settings.add.toggle_switch(
        title="Store Drone Telemetry", default=False, toggleswitch_id="store_drone_telemetry")
    settings.add.toggle_switch(
        title="Store Criminal Offences", default=False, toggleswitch_id="store_criminal_offences")

    # clock that displays the current date and time
    settings.add.clock(clock_format="%d-%m-%y %H:%M:%S",
                      title_format="Local Time : {0}")

# 3 different buttons each with a different style and purpose
    settings.add.button(title="Print Settings", action=printSettings,
                        font_color=RED, background_color=WHITE)
    settings.add.button(title=" Settings", action=refreshSettings,
                        font_color=RED, background_color=WHITE)
    settings.add.button(title="Restore Defaults", action=settings.reset_value,
                        font_color=RED, background_color=WHITE)
    settings.add.button(title="Return To Main Menu",
                    action=pm.events.BACK, align=pm.locals.ALIGN_CENTER)

    controls = pm.Menu(title="Controls",
                   width=WIDTH,
                   height=HEIGHT,
                   theme=pm.themes.THEME_BLUE)

    controls._theme.widget_font_size = 25
    controls._theme.widget_font_color = BLACK
    controls._theme.widget_alignment = pm.locals.ALIGN_LEFT

    controls.add.toggle_switch(
        title="Go To Position", default=False, toggleswitch_id="take_off")

    controls.add.toggle_switch(
        title="Land", default=False, toggleswitch_id="land")

    controls.add.button(title="Return To Main Menu",
                    action=pm.events.BACK, align=pm.locals.ALIGN_CENTER)

    # Creating the main menu
    mainMenu = pm.Menu(title="Maturaprojekt",
                    width=WIDTH,
                    height=HEIGHT,
                    theme=pm.themes.THEME_BLUE)

    # Adjusting the default values
    mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER

    # Button that takes to the settings menu when clicked
    mainMenu.add.button(title="Settings", action=settings,
                    font_color=WHITE, background_color=BLUE)

    mainMenu.add.button(title="Controls", action=controls,
                    font_color=WHITE, background_color=BLACK)

    #controls.set_controller()

    # An empty label that is used to add a seperation between the two buttons
    mainMenu.add.label(title="")

    # Exit button that is used to terminate the program
    mainMenu.add.button(title="Exit", action=pm.events.EXIT,
                    font_color=WHITE, background_color=RED)

    # Lets us loop the main menu on the screen
    mainMenu.mainloop(screen)

def menu_start(client):
    main(client)
def mqtt_thread():
    client = mqtt.Client("Graphische Steuereinheit", clean_session=True, userdata=None)

    # Set the callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    # Connect to the MQTT broker
    client.connect(broker_address, port, keepalive=120)

    # Start the MQTT loop
    client.loop_forever()
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    menu_thread = threading.Thread(target=menu_start, args=(client,),
                                       daemon=True)
    menu_thread.start()
    menu_thread.run()

# Callback function to handle message reception
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

def on_publish(client, userdata, mid):
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")




# Start the MQTT thread
mqtt_thread = threading.Thread(target=mqtt_thread, daemon=True)
mqtt_thread.start()
mqtt_thread.run()
# Wait for a moment to ensure the MQTT thread has connected
time.sleep(2)

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print("Exiting program.")
