class ChunkChecker:

    def __init__(self, path):
        self.__path = str(path)

    def has_been_generated(self, chunk_coords):
        # Will check the file of the world save (ChunkData.txt) if the coordinates passed to it exist in the file.
        # And therefore if the chunk has been generated there before.
        try:
            file = open(self.__path, 'r')
        except FileNotFoundError:
            file = open(self.__path, 'x')
            return False
        data = file.readlines()
        for line in data:
            x = line.split(";")[0].split(",")[0]  # returns the x coordinate of a bit of chunk data from file
            y = line.split(";")[0].split(",")[1]  # returns the y coordinate
            if (chunk_coords.get_x() == int(x)) and (chunk_coords.get_y() == int(y)):
                file.close()
                return True
        file.close()
        return False
