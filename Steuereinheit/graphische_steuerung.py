import json
import sys
import threading
import time

import pygame
import pygame_menu as pm
import paho.mqtt.client as mqtt

broker_address = "localhost"
port = 1883
graphical_steuereinheit_topic = "Steuereinheit/graphic_control"
START_topic = "Steuereinheit/start"
drone_topic = "Steuereinheit/drone_control"

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

def main():
    def printSettings():
        print("\n\n")
        settingsData = settings.get_input_data()
        for key in settingsData.keys():
            print(f"{key}\t:\t{settingsData[key]}")

    def refreshSettings():
        settingsData = settings.get_input_data()
        jsonMessage = json.dumps(settingsData)
        client.publish(graphical_steuereinheit_topic, jsonMessage, qos=1)

    def publishLand():
        client.publish(drone_topic, "LAND", qos=1)
    def publishStart():
        client.publish(drone_topic, "POS", qos=1)

    def start():
        client.publish(START_topic, "START", qos=1)

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
        title="Ground Camera Usage", default=True, toggleswitch_id="ground_cam_usage")
    settings.add.toggle_switch(
        title="Direction Detection", default=True, toggleswitch_id="direction_detection")
    settings.add.toggle_switch(
        title="Speed Detection", default=False, toggleswitch_id="speed_detection")
    settings.add.toggle_switch(
        title="Take Fake Video Input", default=True, toggleswitch_id="fake_vid_input")
    settings.add.toggle_switch(
        title="GTA Effects", default=True, toggleswitch_id="gta_effects")

    settings.add.button(title="Save Settings", action=refreshSettings,
                        font_color=RED, background_color=WHITE)

    # clock that displays the current date and time
    settings.add.clock(clock_format="%d-%m-%y %H:%M:%S",
                      title_format="Local Time : {0}")

    settings.add.button(title="Return To Main Menu",
                        action=pm.events.BACK, align=pm.locals.ALIGN_CENTER)

    controls = pm.Menu(title="Controls",
                   width=WIDTH,
                   height=HEIGHT,
                   theme=pm.themes.THEME_BLUE)

    controls._theme.widget_font_size = 25
    controls._theme.widget_font_color = BLACK
    controls._theme.widget_alignment = pm.locals.ALIGN_LEFT



    controls.add.button(
        title="Go To Position", action=publishStart,align=pm.locals.ALIGN_CENTER, font_color=BLACK, background_color=WHITE)

    controls.add.button(title="Land", action=publishLand,
            font_color=BLACK, background_color=WHITE, align=pm.locals.ALIGN_CENTER)


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

    mainMenu.add.button(title="Start", action=start, font_color=WHITE, background_color=BLACK)

    # An empty label that is used to add a seperation between the two buttons
    mainMenu.add.label(title="")

    # Exit button that is used to terminate the program
    mainMenu.add.button(title="Exit", action=pm.events.EXIT,
                    font_color=WHITE, background_color=RED)

    mainMenu.mainloop(screen)

def menu_start():
    main()
def mqtt_thread():
    global client
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

# Callback function to handle message reception
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

def on_publish(client, userdata, mid):
    print("Graphische Steuereinheit published message with id " + str(mid) + "\n")


# Start the MQTT thread
mqtt_thread = threading.Thread(target=mqtt_thread, daemon=True)
mqtt_thread.start()

menu_thread = threading.Thread(target=menu_start,
                               daemon=True)


menu_thread.run()
# Wait for a moment to ensure the MQTT thread has connected
time.sleep(2)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Your other main loop code goes here

        #pygame.display.flip()
        pygame.time.Clock().tick(30)

except KeyboardInterrupt:
    pass
finally:
    # Join the threads before exiting
    menu_thread.join()
    mqtt_thread.join()
    print("Exiting program.")
