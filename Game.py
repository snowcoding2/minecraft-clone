from ursina import *
import ChunkLocator
import ChunkGenerator
import ChunkChecker
import ChunkSaver
import ChunkCoords
import Block
import MovementHandler
import UserCoords


class Game:

    def __init__(self, player, noises):
        self.player = player
        self.noises = noises
        self.locator = ChunkLocator.ChunkLocator(player, "ChunkData.txt")
        self.movementHandler = MovementHandler.MovementHandler(ChunkLocator.ChunkLocator(player, "ChunkData.txt"))
        self.generator = ChunkGenerator.ChunkGenerator(ChunkChecker.ChunkChecker("ChunkData.txt"), noises,
                                                       ChunkSaver.ChunkSaver("ChunkData.txt", self.locator),
                                                       self.locator)
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
        new_chunks = [ChunkCoords.ChunkCoords(x - 1, y + 1),
                      ChunkCoords.ChunkCoords(x, y + 1),
                      ChunkCoords.ChunkCoords(x + 1, y + 1),
                      ChunkCoords.ChunkCoords(x - 1, y),
                      ChunkCoords.ChunkCoords(x + 1, y),
                      ChunkCoords.ChunkCoords(x - 1, y - 1),
                      ChunkCoords.ChunkCoords(x, y - 1),
                      ChunkCoords.ChunkCoords(x + 1, y - 1)]

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
        self.movementHandler.change_coords(UserCoords.UserCoords(self.player.x, self.player.z))
        self.movementHandler.change_chunk_coords(
            self.locator.locate(UserCoords.UserCoords(self.player.x, self.player.z)))

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
        # has been removed temporarily
        if held_keys['left shift']:
            self.player.y -= 3
        elif held_keys['space']:
            self.player.y += 3
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
                    block = Block.Block(chunkData.get_coords(),
                                        position=(surface_block.X, surface_block.Y + 1, surface_block.Z),
                                        block_type='cobble')
                    chunkData.add_block(block)

    def culling(self):
        # identifies all non-visible entities (raycasting?)
        # disables entities if they are not already disabled
        pass
