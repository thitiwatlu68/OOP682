import pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True
sara_sheet = pygame.image.load("sara/sara-cal1.png")
sara_rect = pygame.Rect(0, 0, 34, 56) # Assuming each frame is 64x64 pixels
sara_pos = pygame.Rect(50, 50, 34, 56) # Position to draw Sara on the screen
clock = pygame.time.Clock() # Create a clock object to control frame rate
while running: # Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT] and sara_pos.x+sara_rect.width < 400:
        sara_pos.x += 5
    elif key[pygame.K_LEFT] and sara_pos.x > 0:
        sara_pos.x -= 5
    elif key[pygame.K_DOWN] and sara_pos.y+sara_rect.height < 300:
        sara_pos.y += 5
    elif key[pygame.K_UP] and sara_pos.y > 0:
        sara_pos.y -= 5
    clock.tick(90) # Limit the frame rate to 60 FPS
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Arial", 36)
    text = font.render(f"{clock.get_fps():.2f}", True, (0, 0, 0))
    screen.blit(sara_sheet, sara_pos, sara_rect)
    screen.blit(text, (300, 230))
    pygame.display.update() # Update the display
pygame.quit()