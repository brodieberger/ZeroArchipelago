import pkgutil
from typing import TYPE_CHECKING, List, Tuple
import io, os, bsdiff4

from worlds.Files import APDeltaPatch
from BaseClasses import MultiWorld, Region, Entrance, Location
from settings import get_settings

class MMZero3DeltaPatch(APDeltaPatch):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def get_base_rom_as_bytes() -> bytes:
    with open("Mega Man Zero 3 (USA).gba", "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes

class Rom:
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"

    def __init__(self, world: MultiWorld, player: int):
        with open("Mega Man Zero 3 (USA).gba", 'rb') as file:
            content = file.read()
        patched = self.apply_static_delta(content)
        self.random = world.per_slot_randoms[player]
        self.stream = io.BytesIO(patched)
        self.world = world
        self.player = player

    def apply_static_delta(self, b: bytes) -> bytes:
        """
        Gets the patched ROM data generated from applying the ap-patch diff file to the provided ROM.
        Which should contain all changed text banks and assembly code
        """
        import pkgutil
        patch_bytes = pkgutil.get_data(__name__, "data/basepatch.bsdiff")
        patched_rom = bsdiff4.patch(b, patch_bytes)
        return patched_rom

    def close(self, path):
        output_path = os.path.join(path, f"AP_{self.world.seed_name}_P{self.player}_{self.world.player_name[self.player]}.gba")
        with open(output_path, 'wb') as outfile:
            outfile.write(self.stream.getvalue())
        patch = MMZero3DeltaPatch(os.path.splitext(output_path)[0] + ".apmmzero3", player=self.player,
                                player_name=self.world.player_name[self.player], patched_path=output_path)
        patch.write()
        os.unlink(output_path)
        self.stream.close()