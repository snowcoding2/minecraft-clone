class ChunkSaver:

    def __init__(self, path, locator):
        self.__path = path
        self.__locator = locator

    def save_chunk_data(self, chunk_data):
        # format of data being stored is as follows {chunkCoordinate.X},{chunkCoordinate.Y};block1.x,block1.y,
        # block1.z,block1.type:block2.x,block2.y,block2.z,block2.type: and so on before the semicolon are the chunk
        # coordinates after the semicolon and inbetween each colon are 3 coordinates and the type one for the x,
        # y and z coordinates respectively and the last is the block type.
        blocks = chunk_data.get_blocks()
        file = open(self.__path, 'a')
        try:
            line = str(chunk_data.get_coords().get_x()) + "," + str(chunk_data.get_coords().get_y()) + ";"
            for block in blocks:
                line += str(block.X) + "," + str(block.Y) + "," + str(block.Z) + "," + str(block.get_type()) + ":"
            file.write(line + "\n")
        finally:
            file.close()
