import sys, os
import pygame

from chars.sara import Hero
from map.map_loader import load_map

class SaraAdventure(object):
    def __init__(self):
        pygame.init()
        # Scale window to match the actual map data (20x20 grid)
        self.tile_size = 48
        self.map_width = 20
        self.map_height = 20
        self.screen_width = self.tile_size * self.map_width
        self.screen_height = self.tile_size * self.map_height
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.caption = 'Sara Adventure'
        pygame.display.set_caption(self.caption)
        
        # Load map layers
        map_json_path = os.path.join('map', 'sample_map.json')
        try:
            self.layers = load_map(map_json_path)
        except Exception as e:
            print(f"Error loading map: {e}")
            self.layers = {}

        # Initialize Hero
        hero_sprite_path = os.path.join('assets', 'sara', 'sara_spritesheet.png')
        self.hero = Hero('Sara', hero_sprite_path, 48, 48, target_size=(48, 64))
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def handle_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def draw_text(self, text, position, color=(255, 255, 255)):
        surface = self.font.render(text, True, color)
        # Add a small shadow/background for better visibility on tiles
        shadow = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (position[0]+1, position[1]+1))
        self.screen.blit(surface, position)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: 
            self.hero.left()
        if keys[pygame.K_RIGHT]: 
            self.hero.right()
        if keys[pygame.K_UP]: 
            self.hero.up()
        if keys[pygame.K_DOWN]: 
            self.hero.down()

    def start(self):
        while True:
            self.handle_close()
            self.handle_input()
            elapsed_time = self.clock.tick(60)
            
            # 1. Clear screen
            self.screen.fill((0, 0, 0))
            
            # 2. Draw ALL layers in order
            for layer_name, layer_obj in self.layers.items():
                layer_obj.draw(self.screen, display_tile_size=self.tile_size)
            
            # 3. Update and Draw Hero
            self.hero.update(elapsed_time)
            self.hero.draw(self.screen)
            
            # HUD/Text
            self.draw_text("Sara Adventure - Forest Map", (10, 10))
            
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = SaraAdventure()
    game.start()
