import pygame
import random

# Pygame initialisieren
pygame.init()

# Bildschirmgröße und Einstellungen
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Bilder laden
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
kelvin_bird = pygame.transform.scale(bird_image, (50, 50))

# Globale Variablen für die Spielmechanik
y_geschwindigkeit = -4
springt = False
flappybird = True

# Funktion zum Erstellen der Röhren
def random_roehre(last_x_position):
    # Lücke zwischen den Röhren, Breite der Röhren & Position der Röhren
    luecke = 200
    roehre_width = random.randint(150, 200)
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
def start_game():
    global x, y, y_geschwindigkeit, springt, flappybird
    x = screen_width * 0.1  # Feste x-Position für den Vogel
    y = screen_height * 0.45
    y_geschwindigkeit = -4
    springt = False
    flappybird = True

# Spiel-Schleife
def game_loop():
    global x, y, y_geschwindigkeit, flappybird, springt

    roehren = []
    last_roehre_x = screen_width

    while flappybird:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flappybird = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    springt = True
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
            last_roehre_x = roehre_x

        # Röhren nach links verschieben
        new_roehren = []
        for roehre_top, roehre_bottom, roehre_x, y_top, y_bottom in roehren:
            new_x = roehre_x - geschwindigkeit_roehren
            if new_x + roehre_top.get_width() >= 0:
                new_roehren.append((roehre_top, roehre_bottom, new_x, y_top, y_bottom))
                screen.blit(roehre_top, (new_x, y_top))
                screen.blit(roehre_bottom, (new_x, y_bottom))

        roehren = new_roehren

        bird_mask = pygame.mask.from_surface(kelvin_bird)

        for roehre_top, roehre_bottom, roehre_x, y_top, y_bottom in roehren:
            top_mask = pygame.mask.from_surface(roehre_top)
            bottom_mask = pygame.mask.from_surface(roehre_bottom)

            top_offset = (roehre_x - x, y_top - y)
            bottom_offset = (roehre_x - x, y_bottom - y)

            if bird_mask.overlap(top_mask, top_offset) or bird_mask.overlap(bottom_mask, bottom_offset):
                flappybird = False

        if y < 0:
            y = 0
        if y > screen_height - 50:
            y = screen_height - 50

        screen.blit(kelvin_bird, (x, y))

        pygame.display.update()
        clock.tick(60)

    # Nach dem Verlust die Optionen anzeigen
    game_over_menu()

# Anzeige des "Game Over"-Menüs
def game_over_menu():
    font = pygame.font.SysFont("Arial", 50)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Drücke 'R' um nochmal zu spielen", True, (0, 0, 0))
    quit_text = font.render("Drücke 'Q' um das Spiel zu schließen", True, (0, 0, 0))

    # Hintergrund bleibt sichtbar
    # Die Schrift wird nur über den Hintergrund gezeichnet
    screen.blit(background, (0, 0))  # Zeigt den Hintergrund erneut an, ohne ihn zu überschreiben
    screen.blit(game_over_text, (screen_width // 3, screen_height // 3))
    screen.blit(restart_text, (screen_width // 3, screen_height // 2))
    screen.blit(quit_text, (screen_width // 3, screen_height // 1.5))

    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Wenn 'R' gedrückt wird, startet das Spiel neu
                    start_game()
                    game_loop()
                elif event.key == pygame.K_q:  # Wenn 'Q' gedrückt wird, beendet das Spiel
                    pygame.quit()
                    quit()

# Spiel starten
start_game()
game_loop()
