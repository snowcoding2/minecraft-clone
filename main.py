from perlin_noise import PerlinNoise
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math


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


class ChunkLocator:

    def __init__(self, player, path):
        self.__player = player
        self.__path = path

    @staticmethod
    def locate(coords):
        x = round((coords.get_x() - 5) / 10)
        y = round((coords.get_z() - 5) / 10)
        return ChunkCoords(x, y)

    @staticmethod
    def get_data(chunk_coords):
        file = open("ChunkData.txt", 'r')
        data = file.readlines()
        for line in data:
            split_line = line.split(";")
            chunk_data = split_line[1]
            coords = ChunkCoords(int(split_line[0].split(",")[0]), int(split_line[0].split(",")[1]))
            if coords == chunk_coords:
                file.close()
                return chunk_data
        file.close()
        raise NameError("Chunk not found in file!")


class ChunkSaver:

    def __init__(self, path, locator):
        self.__path = path
        self.__locator = locator

    def save_chunk_data(self, chunk_data):
        # format of data being stored is as follows {chunkCoordinate.X},{chunkCoordinate.Y};block1.x,block1.y,
        # block1.z,block1.type:block2.x,block2.y,block2.z,block2.type: and so on before the semi-colon are the chunk
        # coordinates after the semi-colon and inbetween each colon are 3 coordinates and the type one for the x,
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
            chunk_data = ChunkData(coordinates, [])
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
                    topblock = Block(coordinates, position=(pixel_x + x, y_value, pixel_y + z), block_type='dirt')
                    # topblock.parent = topterrain
                    chunk_data.add_block(topblock)
                    for i in range(1, depth):
                        block = Block(coordinates, position=(pixel_x + x, y_value - i, pixel_y + z), block_type='stone')
                        # block.parent = underterrain
                        chunk_data.add_block(block)
            # topterrain.combine()
            # topterrain.texture = './Textures/grass.png'
            # underterrain.combine()
            # underterrain.texture = './Textures/stone.png'
            self.saver.save_chunk_data(chunk_data)
            return chunk_data

    def load(self, chunk_coords):
        chunk_data = ChunkData(chunk_coords, [])
        for blockData in self.__locator.get_data(chunk_coords).split(":"):
            data = blockData.split(",")
            if data[0] != '\n':
                block = Block(chunk_coords, position=(float(data[0]), float(data[1]), float(data[2])),
                              block_type=data[3])
                chunk_data.add_block(block)
        return chunk_data


class Block(Entity):
    blockType = {
        'stone': 0,
        'dirt': 1,
        'cobble': 3
    }

    blockTypeTextures = {
        'stone': './Textures/stone.png',
        'dirt': './Textures/dirt.png',
        'cobble': './Textures/cobblestone.png'
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


class ChunkData:

    def __init__(self, coords, blocks=None):
        # list of Block entities
        self.__blocks = blocks
        # chunk coords

        self.__coords = coords

    def get_coords(self):
        return self.__coords

    def get_blocks(self):
        return self.__blocks

    def add_block(self, block):
        self.__blocks.append(block)

    def remove_block(self, block):
        self.__blocks.remove(block)


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


class UserCoords:

    def __init__(self, x, z):
        self.__x = x
        self.__z = z

    def get_x(self):
        return self.__x

    def get_z(self):
        return self.__z


class MovementHandler:

    def __init__(self, locator):
        self.__locator = locator
        self.currentChunk = ChunkCoords(0, 0)
        self.previousChunkCoords = ChunkCoords(0, 0)
        self.userCoords = UserCoords(0, 0)
        self.previousUserCoords = UserCoords(0, 0)

    def chunk_changed(self):
        return True if self.currentChunk != self.previousChunkCoords else False

    def change_coords(self, new_coords):
        self.previousUserCoords = self.userCoords
        self.userCoords = new_coords

    def change_chunk_coords(self, new_coords):
        self.previousChunkCoords = self.currentChunk
        self.currentChunk = new_coords


class Game:

    def __init__(self, player, noises):
        self.player = player
        self.noises = noises
        self.locator = ChunkLocator(player, "ChunkData.txt")
        self.movementHandler = MovementHandler(ChunkLocator(player, "ChunkData.txt"))  # Initiates movement handler.
        self.generator = ChunkGenerator(ChunkChecker("ChunkData.txt"), noises,
                                        ChunkSaver("ChunkData.txt", self.locator), self.locator)
        self.chunk_data_list = []
        self.__renderDistance = 5

    def start(self):
        # creates starting chunk for the player to see
        self.chunk_data_list.append(self.generator.generate(self.movementHandler.currentChunk))
        self.update_chunks()

    def update(self):
        self.culling()
        self.update_coords()
        if self.movementHandler.chunk_changed():
            self.update_chunks()

        self.handle_input()

    def update_chunks(self):
        # creates chunks in a 3x3 grid around the player
        current_chunk = self.movementHandler.currentChunk
        x = current_chunk.get_x()
        y = current_chunk.get_y()

        # 0 1 2
        # 3 4 5
        # 6 7 8
        new_chunks = [ChunkCoords(x - 1, y + 1), ChunkCoords(x, y + 1), ChunkCoords(x + 1, y + 1),
                      ChunkCoords(x - 1, y), ChunkCoords(x + 1, y), ChunkCoords(x - 1, y - 1), ChunkCoords(x, y - 1),
                      ChunkCoords(x + 1, y - 1)]

        for i in range(len(self.chunk_data_list)):
            if self.chunk_data_list[i].get_coords() in new_chunks:
                new_chunks.remove(self.chunk_data_list[i].get_coords())
        for i in range(len(new_chunks)):
            self.chunk_data_list.append(self.generator.generate(new_chunks[i]))

    def delete_chunk(self, index):
        # index refers to the index of the chunk in the chunkDataList array
        chunk_data_object = self.chunk_data_list[index]
        for block in chunk_data_object.getBlocks():
            block.disable()
            del block
        del self.chunk_data_list[index]

    def update_coords(self):
        self.movementHandler.change_coords(UserCoords(self.player.x, self.player.z))
        self.movementHandler.change_chunk_coords(self.locator.locate(UserCoords(self.player.x, self.player.z)))

    def save(self):
        for chunkData in self.chunk_data_list:
            if not self.generator.checker.has_been_generated(chunkData.get_coords()):
                self.generator.saver.save_chunk_data(chunkData)
            chunk_data_file = open("ChunkData.txt", "r")
            data = chunk_data_file.readlines()
            line_number = 0
            for i in range(len(data)):
                x = data[i].split(";")[0].split(",")[0]  # returns the x coordinate of a bit of chunk data from file
                y = data[i].split(";")[0].split(",")[1]  # returns the y coordinate
                if (chunkData.get_coords().get_x() == int(x)) and (chunkData.get_coords().get_y() == int(y)):
                    line_number = i
                    break
            data[line_number] = str(chunkData.get_coords().get_x()) + "," + str(chunkData.get_coords().get_y()) + ";"
            for block in chunkData.get_blocks():
                data[line_number] += str(block.X) + "," + str(block.Y) + "," + str(block.Z) + "," + str(
                    block.get_type()) + ":"
            data[line_number] = data[line_number] + "\n"
            chunk_data_file = open("ChunkData.txt", "w")
            chunk_data_file.writelines(data)
            chunk_data_file.close()

    def handle_input(self):
        # time.dt is the difference between a second and the frequency of the game being run so that the game speed
        # is the same regardless of different FPS values
        if held_keys['left shift']:
            self.player.y -= 3 * time.dt
        elif held_keys['space']:
            self.player.y += 3 * time.dt
        elif held_keys['escape']:
            self.save()
            quit()
        elif held_keys['g']:
            self.player.gravity = not self.player.gravity
        elif held_keys['l']:
            self.update_chunks()

    def break_block(self):
        direction = camera.forward
        origin = self.player.world_position + Vec3(0, 2, 0)
        hit_info = raycast(origin, direction, ignore=[self.player], distance=inf, traverse_target=scene, debug=False)
        if hit_info.entities:
            block = hit_info.entities[0]
            block.disable()
            for chunkData in self.chunk_data_list:
                if chunkData.get_coords() == block.get_chunk_coords():
                    chunkData.remove_block(block)

    def place_block(self):
        direction = camera.forward
        origin = self.player.world_position + Vec3(0, 2, 0)
        hit_info = raycast(origin, direction, ignore=[self.player], distance=inf, traverse_target=scene, debug=False)
        if hit_info.entities:
            surface_block = hit_info.entities[0]
            for chunkData in self.chunk_data_list:
                if chunkData.get_coords() == surface_block.get_chunk_coords():
                    block = Block(chunkData.get_coords(),
                                  position=(surface_block.X, surface_block.Y + 1, surface_block.Z),
                                  block_type='cobble')
                    chunkData.add_block(block)

    def culling(self):
        # identifies all non-visible entities (raycasting?)
        # disables entities if they are not already disabled
        pass


app = Ursina()

seed = 420
noises = [PerlinNoise(12, seed), PerlinNoise(6, seed), PerlinNoise(24, seed), PerlinNoise(3, seed)]

game = Game(FirstPersonController(gravity=0), noises)
game.start()


# ursina functions can't make oop
def update():
    game.update()


def input(key):
    if key == 'left mouse down':
        game.break_block()
    elif key == 'right mouse down':
        game.place_block()


app.run()
