import ChunkCoords
import UserCoords


class MovementHandler:

    def __init__(self, locator):
        self.__locator = locator
        self.currentChunk = ChunkCoords.ChunkCoords(0, 0)
        self.previousChunkCoords = ChunkCoords.ChunkCoords(0, 0)
        self.userCoords = UserCoords.UserCoords(0, 0)
        self.previousUserCoords = UserCoords.UserCoords(0, 0)

    def chunk_changed(self):
        return True if self.currentChunk != self.previousChunkCoords else False

    def change_coords(self, new_coords):
        self.previousUserCoords = self.userCoords
        self.userCoords = new_coords

    def change_chunk_coords(self, new_coords):
        self.previousChunkCoords = self.currentChunk
        self.currentChunk = new_coords
