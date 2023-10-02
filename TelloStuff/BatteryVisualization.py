import telnetlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

battery_history = []


def get_battery_level():
    try:
        input_integer = int(input("Bitte geben Sie die Batterieladung des Tello-Drohne ein (0-100): "))
        if 0 <= input_integer <= 100:
            return input_integer
        else:
            print("Ungültige Eingabe. Die Batterieladung muss zwischen 0 und 100 liegen.")
            return None
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine Ganzzahl ein.")
        return None


def get_color(battery_level):
    if battery_level >= 50:
        return 'darkgreen'
    elif battery_level >= 25:
        return 'lightgreen'
    elif battery_level >= 15:
        return 'orange'
    else:
        return 'darkred'


def update_battery_level(frame):
    battery_level = get_battery_level()
    if battery_level is not None:
        # Hinzufügen des aktuellen Akkustands und des Zeitpunkts zur Liste
        current_time = datetime.now().strftime('%H:%M:%S')
        battery_history.append((current_time, battery_level))

        # Begrenzen der Liste auf die letzten 50 Werte
        if len(battery_history) > 50:
            battery_history.pop(0)

        # Aktualisieren des Diagramms mit den gespeicherten Werten
        ax.clear()
        ax.set_ylim(0, 100)
        ax.set_ylabel('Battery Level')
        ax.set_xlabel('Time')
        ax.set_title('Tello Drone Battery Level')

        # Extrahieren von Zeit und Akkustand aus der Liste für die Darstellung
        times, levels = zip(*battery_history)

        # Bestimmen der Farbe basierend auf dem Akkustand
        colors = [get_color(level) for level in levels]

        # Zeichnen einer durchgezogenen Linie, die die Farbwerte befolgt
        for i in range(len(times) - 1):
            ax.plot(times[i:i + 2], levels[i:i + 2], color=colors[i], marker='o', linewidth=2)

        ax.set_xticks(range(len(battery_history)))

        # Ersetzen der x-Achsenbeschriftungen durch die entsprechenden Uhrzeiten
        ax.set_xticklabels(times, rotation=45, ha="right")


fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_battery_level, interval=1000)
plt.tight_layout()
plt.show()
