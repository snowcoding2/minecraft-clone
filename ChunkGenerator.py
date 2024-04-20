import ChunkData
import Block


class ChunkGenerator:

    def __init__(self, checker, noises, saver, locator):
        self.checker = checker
        self.__noises = noises
        self.__locator = locator
        self.saver = saver

    def generate(self, coordinates):
        # All the terrain lines of code increase the fps of the program  by about 100.
        # the terrain lines of code stop the individual access of blocks
        if self.checker.has_been_generated(coordinates):
            return self.load(coordinates)
        else:
            # topterrain = Entity(model=None, collider=None)
            # underterrain = Entity(model=None, collider=None)
            chunk_data = ChunkData.ChunkData(coordinates, [])
            depth = 4  # how many blocks are rendered underneath the top block
            # pixel will be the coordinate of the noise for the block, which needs to be adjusted as the coordinates
            # are chunk coordinates
            pixel_x = coordinates.get_x() * 10
            pixel_y = coordinates.get_y() * 10
            height_scale = 30  # how high the blocks will spawn multiplier
            res = 500  # "width" of the noisemap
            for z in range(10):
                for x in range(10):
                    # instantiates a block at the location
                    # the noise refers to a float which will be the height of the block
                    # saving to chunkData allows for the blocks to be changed after being instantiated
                    # saving to ycoordinates so that the chunkdata can be saved
                    y_value = round(self.__noises[0]([(pixel_x + x) / res, (pixel_y + z) / res]) * height_scale)
                    y_value += round(0.5 * self.__noises[1]([(pixel_x + x) / res, (pixel_y + z) / res]) * height_scale)
                    y_value += round(0.25 * self.__noises[2]([(pixel_x + x) / res, (pixel_y + z) / res]) * height_scale)
                    y_value += round(
                        0.125 * self.__noises[3]([(pixel_x + x) / res, (pixel_y + z) / res]) * height_scale)
                    topblock = Block.Block(coordinates, position=(pixel_x + x, y_value, pixel_y + z), block_type='dirt')
                    # topblock.parent = topterrain
                    chunk_data.add_block(topblock)
                    for i in range(1, depth):
                        block = Block.Block(coordinates, position=(pixel_x + x, y_value - i, pixel_y + z), block_type='stone')
                        # block.parent = underterrain
                        chunk_data.add_block(block)
            # topterrain.combine()
            # topterrain.texture = './Textures/grass.png'
            # underterrain.combine()
            # underterrain.texture = './Textures/stone.png'
            self.saver.save_chunk_data(chunk_data)
            return chunk_data

    def load(self, chunk_coords):
        chunk_data = ChunkData.ChunkData(chunk_coords, [])
        for blockData in self.__locator.get_data(chunk_coords).split(":"):
            data = blockData.split(",")
            if data[0] != '\n':
                block = Block.Block(chunk_coords, position=(float(data[0]), float(data[1]), float(data[2])),
                              block_type=data[3])
                chunk_data.add_block(block)
        return chunk_data

