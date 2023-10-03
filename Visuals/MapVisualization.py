import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Leere Listen für X- und Y-Koordinaten erstellen
x_coords = []
y_coords = []


# Funktion, um Daten zu aktualisieren und das Diagramm zu zeichnen
def update(frame):
    # Koordinaten von der Kommandozeile einlesen (Beispielwerte)
    try:
        x, y, z = map(float, input("Gib die X-, Y- und Z-Koordinaten (getrennt durch Leerzeichen) ein: ").split())
    except ValueError:
        print("Ungültige Eingabe. Beispiel: '1.0 2.0 3.0'")
        return

    # Koordinaten zur Liste hinzufügen
    x_coords.append(x)
    y_coords.append(y)

    # Diagramm zeichnen
    plt.cla()  # Aktuelles Diagramm löschen, um fließende Animation zu erstellen
    plt.plot(x_coords, y_coords, marker='o', color='b')

    # Den aktuellen Punkt (letzte hinzugefügte Koordinate) rot einzeichnen
    plt.plot(x_coords[-1], y_coords[-1], marker='o', markersize=8, color='r')

    # Text "Drohne 1" zentriert über dem aktuellen Punkt anzeigen
    plt.text(x_coords[-1], y_coords[-1], 'Drohne 1', fontsize=10, ha='center', va='bottom')

    plt.xlabel('X-Koordinate')
    plt.ylabel('Y-Koordinate')
    plt.title('Drohnen-Koordinaten')
    plt.grid(True)


# Animation erstellen
ani = FuncAnimation(plt.gcf(), update, interval=1000)  # Aktualisierung alle 1 Sekunde

# Diagramm anzeigen
plt.show()