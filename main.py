import pygame
import random

# Pygame initialisieren
pygame.init()

# Pygame initialisieren & Grundlegende Einstellungen
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Bilder laden & Fenster benennen
background = pygame.image.load("background.png")
bird_image = pygame.image.load("bird.png")
roehre = pygame.image.load("röhre.png")
pygame.display.set_caption("Flappy Bird")

# Geschwindigkeit der Röhren & Frame-Rate festlegen
geschwindigkeit_roehren = 2

# Schwerkraft & Sprungkraft festlegen
schwerkraft = 0.5
sprungkraft = -10
sprung_verlangsamerung = 0.95

clock = pygame.time.Clock()

# Position des Vogels & Größe des Vogels
x = screen_width * 0.1  # Feste x-Position für den Vogel
y = screen_height * 0.45
kelvin_bird = pygame.transform.scale(bird_image, (100, 100))

# Sprunglogik
y_geschwindigkeit = -4
springt = False

# Funktion zum Erstellen der Röhren
def random_roehre(last_x_position):
    # Lücke zwischen den Röhren, Breite der Röhren & Position der Röhren
    luecke = 200
    roehre_width = random.randint(100, 150)  
    x_position = last_x_position + random.randint(200, 300)  # Mindestabstand von 200-300 Pixeln zu vorheriger Röhre

    # Höhe der Röhren zufällig festlegen
    roehre_height = random.randint(100, 400) 
    y_position_top = 0  # obere Röhre bleibt immer oben am Bildschirmrand

    # Die untere Röhre wird unterhalb der oberen Röhre mit der Lücke platziert
    y_position_bottom = roehre_height + luecke

    # Sicherstellen, dass die untere Röhre nicht den unteren Bildschirmrand überschreitet
    if y_position_bottom > screen_height:
        y_position_bottom = screen_height - roehre_height - luecke

    # obere und untere Röhren skalieren
    roehre_top = pygame.transform.scale(roehre, (roehre_width, roehre_height))  
    roehre_bottom = pygame.transform.scale(roehre, (roehre_width, screen_height - y_position_bottom))  

    return roehre_top, roehre_bottom, x_position, y_position_top, y_position_bottom

# Flappy Bird starten, Röhren erstellen & Startposition der ersten Röhre festlegen
flappybird = True
roehren = []
last_roehre_x = screen_width

# Spiel-Schleife
while flappybird:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flappybird = False
        
        # Sprunglogik:
        # Wenn die Leertaste gedrückt wird, springt der Vogel nach oben
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                y_geschwindigkeit = sprungkraft

    # Schwerkraft auf den Vogel anwenden
    if springt:
        y_geschwindigkeit += schwerkraft * sprung_verlangsamerung
    else:
        y_geschwindigkeit += schwerkraft

    y += y_geschwindigkeit

    # Hintergrund zeichnen
    screen.blit(background, (0, 0))

    # Röhren erstellen & zufällig platzieren
    if random.random() < 0.02:
        roehre_top, roehre_bottom, roehre_x, y_top, y_bottom = random_roehre(last_roehre_x)
        roehren.append((roehre_top, roehre_bottom, roehre_x, y_top, y_bottom))
        last_roehre_x = roehre_x  # Update der Position der letzten Röhre

    # Röhren nach links verschieben
    new_roehren = []  # Eine neue Liste für Röhren, die nicht entfernt wurden
    for roehre_top, roehre_bottom, roehre_x, y_top, y_bottom in roehren:
        new_x = roehre_x - geschwindigkeit_roehren  # Röhren bewegen sich auch mit der Geschwindigkeit der Röhren
        if new_x + roehre_top.get_width() >= 0:  # Nur Röhren zeichnen, die noch im Bildschirmbereich sind
            new_roehren.append((roehre_top, roehre_bottom, new_x, y_top, y_bottom))
            screen.blit(roehre_top, (new_x, y_top))
            screen.blit(roehre_bottom, (new_x, y_bottom))
    
    # Ersetzen die alte Röhrenliste durch die neue Liste
    roehren = new_roehren  

    # Bildschirmbegrenzung (wird jetzt nicht mehr unbedingt benötigt)
    if y < 0:
        y = 0
    if y > screen_height - 50:
        y = screen_height - 50

    # Vogel zeichnen (x bleibt konstant)
    screen.blit(kelvin_bird, (x, y))

    # Bildschirm aktualisieren & Frame-Rate festlegen
    pygame.display.update()
    clock.tick(60)

pygame.quit()
