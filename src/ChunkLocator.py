import ChunkCoords


class ChunkLocator:

    def __init__(self, player, path):
        self.__player = player
        self.__path = path

    @staticmethod
    def locate(coords):
        x = round((coords.get_x() - 5) / 10)
        y = round((coords.get_z() - 5) / 10)
        return ChunkCoords.ChunkCoords(x, y)

    @staticmethod
    def get_data(chunk_coords):
        file = open("ChunkData.txt", 'r')
        data = file.readlines()
        for line in data:
            split_line = line.split(";")
            chunk_data = split_line[1]
            coords = ChunkCoords.ChunkCoords(int(split_line[0].split(",")[0]), int(split_line[0].split(",")[1]))
            if coords == chunk_coords:
                file.close()
                return chunk_data
        file.close()
        raise NameError("Chunk not found in file!")
