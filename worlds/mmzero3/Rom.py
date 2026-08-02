from dataclasses import dataclass
import os
import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import TYPE_CHECKING, Optional
from settings import get_settings
import settings
import json

if TYPE_CHECKING:
    from . import MMZero3World


class MMZero3ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        file_name = get_settings().MMZero3_settings["rom_file"]
        if not os.path.exists(file_name):
          file_name = Utils.user_path(file_name)
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

def write_tokens(world: "MMZero3World", patch: MMZero3ProcedurePatch) -> None:
    """Seed data that will be eventually written into the ROM.

    (goal, required disks, starting weapons) as gApSeedConfig read from ap_symbols.json.
    """
    patch.write_file("token_data.bin", patch.get_token_binary())


class MMZero3Settings(settings.Group):
    class MMZero3RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) """
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]


    rom_file: MMZero3RomFile = MMZero3RomFile(MMZero3RomFile.copy_to)