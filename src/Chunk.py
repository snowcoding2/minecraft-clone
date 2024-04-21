class Chunk:

    def __init__(self, coords, blocks=None):
        self.__blocks = blocks
        self.__coords = coords

    def get_coords(self):
        return self.__coords

    def get_blocks(self):
        return self.__blocks

    def add_block(self, block):
        self.__blocks.append(block)

    def remove_block(self, block):
        self.__blocks.remove(block)
