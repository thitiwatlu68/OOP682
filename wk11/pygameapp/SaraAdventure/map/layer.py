# map/layer.py
"""MapLayer module.
Provides a simple class to represent a single map layer (ground, path, items).
The layer loads a tileset image and a 2D grid of tile indices.
"""
import pygame
from typing import List, Tuple

class MapLayer:
    def __init__(self, tileset_path: str, tile_width: int, tile_height: int, grid: List[List[int]]):
        """Create a map layer.
        :param tileset_path: Path to the tileset image.
        :param tile_width: Width of a single tile in pixels.
        :param tile_height: Height of a single tile in pixels.
        :param grid: 2D list of tile indices (row‑major).
        """
        self.tileset = pygame.image.load(tileset_path).convert_alpha()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.grid = grid
        # Calculate number of columns in the tileset image
        self.tileset_cols = self.tileset.get_width() // tile_width

    def draw(self, surface: pygame.Surface, offset: Tuple[int, int] = (0, 0), display_tile_size: int = None):
        """Draw the layer onto the given surface.
        :param surface: Target pygame surface.
        :param offset: (x, y) pixel offset for the whole layer (e.g., camera).
        :param display_tile_size: Optional size to scale tiles for display.
        """
        ox, oy = offset
        d_size = display_tile_size if display_tile_size else self.tile_width

        for row_idx, row in enumerate(self.grid):
            for col_idx, tile_data in enumerate(row):
                # Handle both old format (int) and new format (dict with 'id' and 'rot')
                if isinstance(tile_data, dict):
                    tile_idx = tile_data.get("id", -1)
                    tile_rot = tile_data.get("rot", 0)
                else:
                    tile_idx = tile_data
                    tile_rot = 0

                if tile_idx < 0:
                    continue  # -1 means empty/no tile

                # Determine tile position in the tileset and extract it
                ts_col = tile_idx % self.tileset_cols
                ts_row = tile_idx // self.tileset_cols
                tile_rect = pygame.Rect(
                    ts_col * self.tile_width,
                    ts_row * self.tile_height,
                    self.tile_width,
                    self.tile_height,
                )
                
                # Extract tile surface
                tile_surf = self.tileset.subsurface(tile_rect).copy()
                
                # Apply rotation if needed
                if tile_rot != 0:
                    tile_surf = pygame.transform.rotate(tile_surf, -tile_rot)

                # Scale for display
                if d_size != self.tile_width:
                    tile_surf = pygame.transform.scale(tile_surf, (d_size, d_size))

                dest_pos = (ox + col_idx * d_size, oy + row_idx * d_size)
                surface.blit(tile_surf, dest_pos)
