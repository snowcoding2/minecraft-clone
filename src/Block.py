import BlockType


class Block:

    texture = None

    def __init__(self, chunk_coords, position=(0, 0, 0), block_id=BlockType.BlockType.DIRT):
        self.block_id = block_id
        self.chunk_coords = chunk_coords
        self.position = position
        self.set_texture(block_id)

    def get_id(self):
        return self.block_id

    def get_chunk_coords(self):
        return self.chunk_coords

    def set_texture(self, block_id):
        self.texture = BlockType.BlockType.get_texture(block_id)

    def get_texture(self):
        return self.texture

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_z(self):
        return self.position[2]
