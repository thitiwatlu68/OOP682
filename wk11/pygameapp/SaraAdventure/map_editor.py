import pygame
import sys
import os
import json

# Configuration
TILE_SOURCE_SIZE = 80  # The actual size in the tileset image
TILE_DISPLAY_SIZE = 48 # Smaller size to fit on 1080p and lower resolutions
GRID_SIZE = 12
SIDEBAR_WIDTH = 250
FOOTER_HEIGHT = 160 
SCREEN_WIDTH = TILE_DISPLAY_SIZE * GRID_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = TILE_DISPLAY_SIZE * GRID_SIZE + FOOTER_HEIGHT
MAP_FILE = os.path.join('map', 'sample_map.json')
TILESET_PATH = os.path.join('assets', 'maps', 'forest_tileset.png')

class MapEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Map Editor - Wheel: Tile, [key +/ -]: Layer, N: New Layer, S: Save")
        
        # Load Tileset
        try:
            self.tileset = pygame.image.load(TILESET_PATH).convert_alpha()
        except Exception as e:
            print(f"Error loading tileset: {e}")
            pygame.quit()
            sys.exit()
            
        self.tileset_width = self.tileset.get_width()
        self.tileset_height = self.tileset.get_height()
        self.tileset_cols = self.tileset_width // TILE_SOURCE_SIZE
        self.tileset_rows = self.tileset_height // TILE_SOURCE_SIZE
        self.total_tiles = self.tileset_cols * self.tileset_rows
        
        # Grid Data
        self.current_layer_index = 0
        self.layers = self.load_existing_map()
        
        self.selected_tile = 0
        self.current_rotation = 0 # 0, 90, 180, 270 degrees
        self.sidebar_scroll = 0 # Vertical scroll offset for palette
        self.clock = pygame.time.Clock()
        
        # Tile costs and names (Mock data)
        self.tile_info = {}
        for i in range(self.total_tiles):
            self.tile_info[i] = {
                "name": f"Tile {i}",
                "cost": (i % 10) * 10 + 5 # Dynamic mock cost
            }
            if i == 0: self.tile_info[i]["name"] = "Grass"
            if i == 1: self.tile_info[i]["name"] = "Dirt"
    def load_existing_map(self):
        if os.path.exists(MAP_FILE):
            try:
                with open(MAP_FILE, 'r') as f:
                    data = json.load(f)
                    layers = data['layers']
                    # Normalize grid: ensure every cell is a dict with 'id' and 'rot'
                    for layer in layers:
                        grid = layer['grid']
                        for y in range(len(grid)):
                            for x in range(len(grid[y])):
                                tile = grid[y][x]
                                if isinstance(tile, int):
                                    grid[y][x] = {"id": tile, "rot": 0}
                    return layers
            except Exception as e:
                print(f"Error reading JSON: {e}")
        
        # Fallback empty map with objects
        initial_map = []
        for name, fill_id in [("ground", 0), ("path", -1), ("items", -1)]:
            initial_map.append({
                "name": name,
                "tileset": "../assets/maps/forest_tileset.png",
                "grid": [[{"id": fill_id, "rot": 0} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            })
        return initial_map

    def save_map(self):
        data = {
            "tile_width": TILE_SOURCE_SIZE,
            "tile_height": TILE_SOURCE_SIZE,
            "layers": self.layers
        }
        try:
            with open(MAP_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Map saved to {MAP_FILE}")
        except Exception as e:
            print(f"Error saving map: {e}")

    def get_tile_surface(self, tile_index, size=None, rotation=0):
        if tile_index < 0: return None
        tx = (tile_index % self.tileset_cols) * TILE_SOURCE_SIZE
        ty = (tile_index // self.tileset_cols) * TILE_SOURCE_SIZE
        surf = self.tileset.subsurface((tx, ty, TILE_SOURCE_SIZE, TILE_SOURCE_SIZE)).copy()
        
        # Apply rotation (pygame rotate is CCW, so we use -rotation for clockwise feel)
        if rotation != 0:
            surf = pygame.transform.rotate(surf, -rotation)
            
        if size:
            return pygame.transform.scale(surf, (size, size))
        return surf

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Mouse Wheel interaction
                if event.type == pygame.MOUSEWHEEL:
                    # Check if mouse is over Sidebar or Grid
                    m_pos = pygame.mouse.get_pos()
                    grid_px_w = TILE_DISPLAY_SIZE * GRID_SIZE
                    if m_pos[0] >= grid_px_w and m_pos[1] < SCREEN_HEIGHT - FOOTER_HEIGHT:
                        # Scroll Palette
                        self.sidebar_scroll -= event.y * 30 
                        # Clamp scroll
                        max_scroll = max(0, (self.total_tiles // 4) * 48 - (SCREEN_HEIGHT - FOOTER_HEIGHT - 60))
                        self.sidebar_scroll = max(0, min(self.sidebar_scroll, max_scroll))
                    else:
                        # Change Tile Brush
                        self.selected_tile = (self.selected_tile + event.y) % self.total_tiles
                        if self.selected_tile < 0: self.selected_tile += self.total_tiles

                # Keyboard shortcuts
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_map()
                    if event.key == pygame.K_1: self.current_layer_index = 0
                    if event.key == pygame.K_2: self.current_layer_index = 1
                    if event.key == pygame.K_3: self.current_layer_index = 2
                    
                    # New shortcuts for dynamic layers
                    if event.key == pygame.K_n:
                        # Add new layer
                        new_layer_name = f"layer_{len(self.layers)}"
                        self.layers.append({
                            "name": new_layer_name,
                            "tileset": "../assets/maps/forest_tileset.png",
                            "grid": [[{"id": -1, "rot": 0} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                        })
                        self.current_layer_index = len(self.layers) - 1
                        print(f"Added new layer: {new_layer_name}")
                    
                    if event.key == pygame.K_EQUALS: # Plus key without shift
                        self.current_layer_index = (self.current_layer_index + 1) % len(self.layers)
                    if event.key == pygame.K_MINUS:
                        self.current_layer_index = (self.current_layer_index - 1) % len(self.layers)
                    
                    if event.key == pygame.K_x:
                        # Delete current layer (ensure at least one layer remains)
                        if len(self.layers) > 1:
                            deleted = self.layers.pop(self.current_layer_index)
                            self.current_layer_index = max(0, self.current_layer_index - 1)
                            print(f"Deleted layer: {deleted['name']}")
                        else:
                            print("Cannot delete the last layer.")
                            
                    if event.key == pygame.K_SPACE:
                        # Rotate brush
                        self.current_rotation = (self.current_rotation + 90) % 360
                        print(f"Rotation: {self.current_rotation} deg")

                    if event.key == pygame.K_r:
                        # Rename current layer (using a simple prompt might freeze, but keeping for now per logic)
                        # Changed key to F2 for rename to free up R if needed, but keeping R as per user's current setup
                        print(f"Current name: {self.layers[self.current_layer_index]['name']}")
                        # In a real app we'd use a pygame text input, but for this exercise:
                        new_name = f"Layer_{len(self.layers)}" # Default to avoid hang
                        # new_name = input("Enter new layer name: ") 
                        self.layers[self.current_layer_index]['name'] = new_name
                        print(f"Renamed to: {new_name}")

            # Mouse input
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            
            # Local grid dimensions for easier calculation
            grid_px_width = TILE_DISPLAY_SIZE * GRID_SIZE
            grid_px_height = TILE_DISPLAY_SIZE * GRID_SIZE

            # Initialize grid_x, grid_y to avoid UnboundLocalError
            grid_x, grid_y = -1, -1

            # Check if mouse is in the grid area
            if mouse_pos[0] < grid_px_width and mouse_pos[1] < grid_px_height:
                grid_x = mouse_pos[0] // TILE_DISPLAY_SIZE
                grid_y = mouse_pos[1] // TILE_DISPLAY_SIZE
                
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    active_grid = self.layers[self.current_layer_index]['grid']
                    if grid_y < len(active_grid) and grid_x < len(active_grid[grid_y]):
                        if mouse_buttons[0]: # Left Click
                            old_tile = active_grid[grid_y][grid_x]
                            new_tile = {"id": self.selected_tile, "rot": self.current_rotation}
                            if old_tile != new_tile:
                                active_grid[grid_y][grid_x] = new_tile
                        elif mouse_buttons[2]: # Right Click
                            active_grid[grid_y][grid_x] = {"id": -1, "rot": 0}
            
            # Sidebar clicking should be allowed anywhere in the sidebar width
            if mouse_pos[0] >= grid_px_width and mouse_pos[1] < SCREEN_HEIGHT - FOOTER_HEIGHT:
                if mouse_buttons[0]:
                    # Clicked in sidebar to select tile
                    sidebar_tile_size = 40
                    padding = 8
                    cols_in_sidebar = max(1, (SIDEBAR_WIDTH - 20) // (sidebar_tile_size + padding))
                    
                    sx = (mouse_pos[0] - grid_px_width - 10) // (sidebar_tile_size + padding)
                    sy = (mouse_pos[1] - 50 + self.sidebar_scroll) // (sidebar_tile_size + padding)
                    
                    if 0 <= sx < cols_in_sidebar:
                        clicked_tile = sy * cols_in_sidebar + sx
                        if 0 <= clicked_tile < self.total_tiles:
                            if self.selected_tile != clicked_tile:
                                self.selected_tile = clicked_tile
                                # print(f"Selected tile {self.selected_tile}")

            # Drawing
            self.screen.fill((50, 50, 50))
            
            # Draw layers in order
            for idx, layer in enumerate(self.layers):
                is_current = (idx == self.current_layer_index)
                grid = layer['grid']
                # Draw only what's visible within GRID_SIZE boundaries
                for y in range(min(GRID_SIZE, len(grid))):
                    row = grid[y]
                    for x in range(min(GRID_SIZE, len(row))):
                        tile_data = row[x]
                        tile_id = tile_data["id"] if isinstance(tile_data, dict) else tile_data
                        tile_rot = tile_data["rot"] if isinstance(tile_data, dict) else 0
                        
                        if tile_id != -1:
                            surf = self.get_tile_surface(tile_id, TILE_DISPLAY_SIZE, tile_rot)
                            if surf:
                                surf.set_alpha(255) # Always fully opaque
                                self.screen.blit(surf, (x * TILE_DISPLAY_SIZE, y * TILE_DISPLAY_SIZE))

            # Draw grid lines
            for i in range(GRID_SIZE + 1):
                pygame.draw.line(self.screen, (100, 100, 100), (i * TILE_DISPLAY_SIZE, 0), (i * TILE_DISPLAY_SIZE, grid_px_height))
                pygame.draw.line(self.screen, (100, 100, 100), (0, i * TILE_DISPLAY_SIZE), (grid_px_width, i * TILE_DISPLAY_SIZE))

            # Draw preview under mouse
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                preview = self.get_tile_surface(self.selected_tile, TILE_DISPLAY_SIZE, self.current_rotation)
                if preview:
                    preview.set_alpha(150) # Maintain semi-transparency for the brush preview
                    self.screen.blit(preview, (grid_x * TILE_DISPLAY_SIZE, grid_y * TILE_DISPLAY_SIZE))
                    # Draw highlight box
                    pygame.draw.rect(self.screen, (255, 255, 255), (grid_x * TILE_DISPLAY_SIZE, grid_y * TILE_DISPLAY_SIZE, TILE_DISPLAY_SIZE, TILE_DISPLAY_SIZE), 1)
            
            # Draw sidebar (Right)
            sidebar_rect = pygame.Rect(grid_px_width, 0, SIDEBAR_WIDTH, grid_px_height)
            pygame.draw.rect(self.screen, (40, 40, 45), sidebar_rect)
            pygame.draw.line(self.screen, (200, 200, 200), (grid_px_width, 0), (grid_px_width, grid_px_height), 2)
            
            sidebar_font = pygame.font.SysFont(None, 24)
            title = sidebar_font.render("Tile Palette", True, (255, 255, 255))
            self.screen.blit(title, (grid_px_width + 20, 10))
            
            # Draw tile grid in sidebar (with clipping and scroll)
            sidebar_tile_size = 40
            padding = 8
            cols_in_sidebar = max(1, (SIDEBAR_WIDTH - 20) // (sidebar_tile_size + padding))
            
            # Surface for clipping palette
            palette_height = (TILE_DISPLAY_SIZE * GRID_SIZE) - 60
            palette_surf = pygame.Surface((SIDEBAR_WIDTH - 10, palette_height))
            palette_surf.fill((40, 40, 45))

            for i in range(self.total_tiles):
                row_in_sidebar = i // cols_in_sidebar
                col_in_sidebar = i % cols_in_sidebar
                tx = col_in_sidebar * (sidebar_tile_size + padding)
                ty = row_in_sidebar * (sidebar_tile_size + padding) - self.sidebar_scroll
                
                # Only draw if visible in palette area
                if -sidebar_tile_size <= ty <= palette_height:
                    # Highlight selected
                    if i == self.selected_tile:
                        pygame.draw.rect(palette_surf, (255, 255, 0), (tx - 2, ty - 2, sidebar_tile_size + 4, sidebar_tile_size + 4), 2)
                    
                    # Get tile surface and scale it
                    scaled_tile = self.get_tile_surface(i, sidebar_tile_size)
                    if scaled_tile:
                        palette_surf.blit(scaled_tile, (tx, ty))
            
            self.screen.blit(palette_surf, (grid_px_width + 10, 50))

            # Draw a simple scrollbar indicator
            total_rows = (self.total_tiles + cols_in_sidebar - 1) // cols_in_sidebar
            content_h = total_rows * (sidebar_tile_size + padding)
            if content_h > palette_height:
                sb_h = max(10, (palette_height / content_h) * palette_height)
                sb_y = 50 + (self.sidebar_scroll / content_h) * palette_height
                pygame.draw.rect(self.screen, (100, 100, 100), (SCREEN_WIDTH - 8, sb_y, 5, sb_h))

            # Draw Footer (Bottom)
            footer_rect = pygame.Rect(0, grid_px_height, SCREEN_WIDTH, FOOTER_HEIGHT)
            pygame.draw.rect(self.screen, (30, 30, 35), footer_rect)
            pygame.draw.line(self.screen, (200, 200, 200), (0, grid_px_height), (SCREEN_WIDTH, grid_px_height), 2)

            footer_font = pygame.font.SysFont(None, 28)
            small_font = pygame.font.SysFont(None, 20)

            # Show selected tile in footer
            preview_rect = pygame.Rect(20, grid_px_height + 20, 100, 100)
            pygame.draw.rect(self.screen, (100, 100, 100), preview_rect, 1)
            
            scaled_preview = self.get_tile_surface(self.selected_tile, 100, self.current_rotation)
            if scaled_preview:
                self.screen.blit(scaled_preview, (20, grid_px_height + 20))

            # --- Section 1: Selected Tile Info ---
            selected_info = self.tile_info.get(self.selected_tile, {"name": "Unknown", "cost": 0})
            detail_x = 140
            detail_y = grid_px_height + 25
            
            name_text = footer_font.render(f"{selected_info['name']}", True, (255, 255, 255))
            id_text = small_font.render(f"ID: {self.selected_tile} | Rot: {self.current_rotation}°", True, (180, 180, 180))
            cost_text = footer_font.render(f"Cost: {selected_info['cost']} Coins", True, (255, 255, 100))
            
            self.screen.blit(name_text, (detail_x, detail_y))
            self.screen.blit(id_text, (detail_x, detail_y + 25))
            self.screen.blit(cost_text, (detail_x, detail_y + 45))

            # Layer Info
            layer_name = self.layers[self.current_layer_index]['name']
            layer_text = small_font.render(f"Active Layer: {layer_name}", True, (200, 255, 200))
            self.screen.blit(layer_text, (detail_x, detail_y + 85))

            # --- Section 2: Controls & Shortcuts ---
            ctrl_x = 340
            help_title = small_font.render("CONTROLS & SHORTCUTS", True, (200, 200, 200))
            pygame.draw.line(self.screen, (100, 100, 100), (ctrl_x, detail_y + 18), (ctrl_x + 160, detail_y + 18), 1)
            self.screen.blit(help_title, (ctrl_x, detail_y))
            
            mouse_instr = ["[L] Place", "[R] Erase", "[W] Select"]
            key_instr = ["[Space] Rotate", "[1-3] Layers", "[+/-] Cycle", "[N/X] Add/Del", "[S] Save"]
            
            # Column 1
            for idx, instr in enumerate(mouse_instr):
                text = small_font.render(instr, True, (160, 160, 160))
                self.screen.blit(text, (ctrl_x, detail_y + 25 + idx * 18))
            # Column 2
            for idx, instr in enumerate(key_instr):
                text = small_font.render(instr, True, (160, 160, 160))
                self.screen.blit(text, (ctrl_x + 100, detail_y + 25 + idx * 18))

            # --- Section 3: Map Budget & Warnings ---
            budget_x = SCREEN_WIDTH - 240
            
            # Total cost calculation
            total_cost = 0
            for layer in self.layers:
                for row in layer['grid']:
                    for t in row:
                        t_id = t["id"] if isinstance(t, dict) else t
                        if t_id != -1:
                            total_cost += self.tile_info.get(t_id, {"cost": 0})["cost"]
            
            total_text = footer_font.render(f"Total Cost: {total_cost}", True, (255, 100, 100))
            self.screen.blit(total_text, (budget_x, detail_y))

            hint_text = small_font.render("Press 'S' to Save", True, (255, 255, 0))
            self.screen.blit(hint_text, (budget_x, detail_y + 100))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()