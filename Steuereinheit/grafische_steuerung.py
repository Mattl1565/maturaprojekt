import pygame
import sys

drone_height = 0
drone_angle = 0
fake_video_inputs = False

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphische Steuerung")

# Create a font object
font = pygame.font.Font(None, FONT_SIZE)

##DRONE HEIGHT BOX
drone_height_input = pygame.Rect(50, 100, 125, 32)
drone_height_color_inactive = pygame.Color('lightskyblue3')
drone_height_color_active = pygame.Color('dodgerblue2')
drone_height_color = drone_height_color_inactive
text_height = str(drone_height)  # Update text with initial drone_height
active_height = False

##DRONE ANGLE BOX
drone_angle_input = pygame.Rect(50, 200, 125, 32)
drone_angle_color_inactive = pygame.Color('lightskyblue3')
drone_angle_color_active = pygame.Color('dodgerblue2')
drone_angle_color = drone_angle_color_inactive
text_angle = str(drone_angle)  # Update text with initial drone_height
active_angle = False

##TAKE FAKE VIDEO INPUTS DROPDOWN
fake_video_inputs_rect = pygame.Rect(50, 300, 200, 40)
fake_video_inputs_color_inactive = pygame.Color('lightskyblue3')
fake_video_inputs_color_active = pygame.Color('dodgerblue2')
fake_video_inputs_color = fake_video_inputs_color_inactive
text_fake_video_inputs = "Choose Option"
active_fake_video_inputs = False
fake_video_inputs_options = ["True", "False"]
selected_fake_video_input = None

# Set up the clock
clock = pygame.time.Clock()

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if drone_height_input.collidepoint(event.pos):
                active_height = not active_height
                active_angle = False
                active_fake_video_inputs = False
            elif drone_angle_input.collidepoint(event.pos):
                active_angle = not active_angle
                active_height = False
                active_fake_video_inputs = False
            elif fake_video_inputs_rect.collidepoint(event.pos):
                active_fake_video_inputs = not active_fake_video_inputs
                active_height = False
                active_angle = False
            else:
                active_height = False
                active_angle = False
                active_fake_video_inputs = False

            drone_height_color = drone_height_color_active if active_height else drone_height_color_inactive
            drone_angle_color = drone_angle_color_active if active_angle else drone_angle_color_inactive
            fake_video_inputs_color = fake_video_inputs_color_active if active_fake_video_inputs else fake_video_inputs_color_inactive


        if event.type == pygame.KEYDOWN:
            if active_height:
                if event.key == pygame.K_RETURN:
                    drone_height = int(text_height)
                    print("New Drone Height:", drone_height)
                elif event.key == pygame.K_BACKSPACE:
                    text_height = text_height[:-1]
                else:
                    text_height += event.unicode

            elif active_angle:
                if event.key == pygame.K_RETURN:
                    drone_angle = int(text_angle)
                    print("New Drone Angle:", drone_angle)
                elif event.key == pygame.K_BACKSPACE:
                    text_angle = text_angle[:-1]
                else:
                    text_angle += event.unicode

            # Check if an option is selected in the fake video inputs dropdown
            elif active_fake_video_inputs and event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(fake_video_inputs_options):
                    option_rect = fake_video_inputs_rect.move(0, fake_video_inputs_rect.height + 40 * i)
                    if option_rect.collidepoint(event.pos):
                        selected_fake_video_input = option
                        text_fake_video_inputs = selected_fake_video_input
                        fake_video_inputs = (
                                    selected_fake_video_input == "True")  # Update the fake_video_inputs variable
                        print("Fake Video Inputs:", fake_video_inputs)
                        active_fake_video_inputs = False  # Close the dropdown after selecting an option
    # Fill the background
    screen.fill(WHITE)

    pygame.draw.rect(screen, drone_height_color, drone_height_input, 2)
    draw_text(screen, "Drone Height", font, BLACK, drone_height_input.x, drone_height_input.y - 20)
    draw_text(screen, text_height, font, BLACK, drone_height_input.x + 5, drone_height_input.y + 5)
    draw_text(screen, "m", font, BLACK, drone_height_input.x + 30, drone_height_input.y + 5)

    pygame.draw.rect(screen, drone_angle_color, drone_angle_input, 2)
    draw_text(screen, "Drone Angle", font, BLACK, drone_angle_input.x, drone_angle_input.y - 20)
    draw_text(screen, text_angle, font, BLACK, drone_angle_input.x + 5, drone_angle_input.y + 5)
    draw_text(screen, "°", font, BLACK, drone_angle_input.x + 30, drone_angle_input.y + 5)

    pygame.draw.rect(screen, fake_video_inputs_color, fake_video_inputs_rect, 2)
    draw_text(screen, "Take Fake Video Inputs", font, BLACK, fake_video_inputs_rect.x, fake_video_inputs_rect.y - 20)
    draw_text(screen, text_fake_video_inputs, font, BLACK, fake_video_inputs_rect.x + 5, fake_video_inputs_rect.y + 5)

    # Draw the fake video inputs dropdown options if the menu is active
    if active_fake_video_inputs:
        for i, option in enumerate(fake_video_inputs_options):
            option_rect = fake_video_inputs_rect.move(0, 40 * i + fake_video_inputs_rect.height)
            pygame.draw.rect(screen, fake_video_inputs_color_active, option_rect, 2)
            draw_text(screen, option, font, BLACK, option_rect.x + 5, option_rect.y + 5)

    # Update the display
    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
