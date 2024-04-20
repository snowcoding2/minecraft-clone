from ursina import *


class Block(Entity):
    blockType = {
        'stone': 0,
        'dirt': 1,
        'cobble': 3
    }

    blockTypeTextures = {
        'stone': './textures/stone.png',
        'dirt': './textures/dirt.png',
        'cobble': './textures/cobblestone.png'
    }

    def __init__(self, chunk_coords, position=(0, 0, 0), block_type='stone', ):
        super().__init__(
            position=position,
            model='cube',
            origin_y=0.5,
            texture=self.blockTypeTextures.get(block_type),
            color=color.white,
            collider='box'
        )
        self.blockType = block_type
        self.chunkCoordinates = chunk_coords

    def get_type(self):
        return self.blockType

    def get_chunk_coords(self):
        return self.chunkCoordinates
    