import math


class ChunkCoords:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        if isinstance(other, ChunkCoords):
            return self.__x == other.get_x() and self.__y == other.get_y()
        return False

    @staticmethod
    def get_distance(chunk1, chunk2):
        return math.sqrt(((chunk2.get_x() - chunk1.get_x()) ** 2) + ((chunk2.get_y() - chunk1.get_y()) ** 2))

    @staticmethod
    def get_possible_coords(current_chunk_coords, r):
        # r = radius
        # this function will generate a "circle" of possible chunk coordinates around a given chunk coordinate
        # this function is used to know which chunks could be generated at at a given time
        coords = []
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                coords.append(ChunkCoords(current_chunk_coords.get_x() + x, current_chunk_coords.get_y() + y))
        return coords

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y
