import pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True
clock = pygame.time.Clock() # Create a clock object to control frame rate
while running: # Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(90) # Limit the frame rate to 60 FPS
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Arial", 36)
    text = font.render(f"{clock.get_fps():.2f}", True, (0, 0, 0))
    screen.blit(text, (300, 230))
    pygame.display.update() # Update the display
pygame.quit()
