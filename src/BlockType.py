class BlockType:
    STONE = 0
    GRASS = 1
    DIRT = 3

    @staticmethod
    def get_texture(block_id):
        if block_id == BlockType.STONE or 0:
            return '../textures/stone.png'
        elif block_id == BlockType.GRASS or 1:
            return '../textures/grass.png'
        elif block_id == BlockType.DIRT or 3:
            return '../textures/dirt.png'
