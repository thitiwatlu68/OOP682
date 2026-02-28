import pygame
from pygame.sprite import Sprite

class Hero(Sprite):
    def __init__(self, name, filename, x, y, rows=4, cols=3, target_size=(48, 64)):
        super().__init__()
        self.name = name
        # Load and convert to per-pixel alpha
        raw_sheet = pygame.image.load(filename).convert_alpha()
        
        # Manually create a clean sheet by making white-ish pixels transparent
        # This is more robust against noise in the background
        self.sheet = pygame.Surface(raw_sheet.get_size(), pygame.SRCALPHA)
        for ix in range(raw_sheet.get_width()):
            for iy in range(raw_sheet.get_height()):
                color = raw_sheet.get_at((ix, iy))
                # If pixel is very close to white, make it transparent
                if color.r > 240 and color.g > 240 and color.b > 240:
                    self.sheet.set_at((ix, iy), (0, 0, 0, 0))
                else:
                    self.sheet.set_at((ix, iy), color)

        self.rows = rows
        self.cols = cols
        sheet_w, sheet_h = self.sheet.get_size()
        
        # The spritesheet has some noise/text at the very top. 
        # We'll skip the first few pixels and calculate frames accordingly.
        self.top_offset = 5 
        self.frame_width = sheet_w // cols
        self.frame_height = (sheet_h - self.top_offset) // rows
        
        self.row = 0
        self.col = 0
        self.elapsed_time = 0
        self.target_size = target_size
        self.rect = pygame.Rect(x, y, target_size[0], target_size[1])

    def update(self, elapsed_time):
        self.elapsed_time += elapsed_time
        if self.elapsed_time > 150:
            self.col = (self.col + 1) % self.cols
            self.elapsed_time -= 150

    def left(self): 
        self.rect.x -= 5
        self.row = 2 
    def right(self): 
        self.rect.x += 5
        self.row = 3 
    def up(self): 
        self.rect.y -= 5
        self.row = 1 
    def down(self): 
        self.rect.y += 5
        self.row = 0 

    def draw(self, surface):
        # Extract frame with offset to avoid top noise
        frame_rect = pygame.Rect(
            self.col * self.frame_width, 
            self.top_offset + self.row * self.frame_height, 
            self.frame_width, 
            self.frame_height
        )
        # Check if rect is within sheet bounds to avoid errors
        if self.sheet.get_rect().contains(frame_rect):
            frame = self.sheet.subsurface(frame_rect).copy()
            scaled_frame = pygame.transform.scale(frame, self.target_size)
            surface.blit(scaled_frame, self.rect)