from dataclasses import dataclass
from Options import (Choice, Range, NamedRange, Toggle, DefaultOnToggle, OptionSet, DeathLink, OptionGroup,
                     StartInventoryPool, PerGameCommonOptions, Visibility)

from .data import Data


class RequiredSecretDisks(Range):
    """Percentage of the seed's Secret Disks required to unlock the final stage.

    The Abandoned Research Laboratory opens once every other stage has been cleared and
    you are holding this share of the disks. Clearing that stage completes the game.
    A seed has 180 disks, unless the disk cut option is enabled.
    """
    display_name = "Required Secret Disks"
    range_start = 0
    range_end = 100
    default = 67

class ExSkillRank(Choice):
    """The rank a stage clear needs in order to send that stage's EX Skill check. In the vanilla game it would be an A.

    The rank is for the mission just finished, not your overall rank. F sends the check on any clear.
    """
    display_name = "EX Skill Rank"
    option_s = Data.RANK_S
    option_a = Data.RANK_A
    option_b = Data.RANK_B
    option_c = Data.RANK_C
    option_d = Data.RANK_D
    option_e = Data.RANK_E
    option_f = Data.RANK_F
    default = Data.RANK_A


class FinalStageRank(Choice):
    """The rank you need to get on each stage for the final stage to open, in addition to the required disks.

    F means that clearing each stage will automatically unlock the boss.
    None means no stage has to be cleared at all, and the final stage opens as soon as you hold the required secret disks.
    """
    display_name = "Final Stage Rank"
    option_s = Data.RANK_S
    option_a = Data.RANK_A
    option_b = Data.RANK_B
    option_c = Data.RANK_C
    option_d = Data.RANK_D
    option_e = Data.RANK_E
    option_f = Data.RANK_F
    option_none = Data.AP_FINAL_RANK_NONE
    default = Data.RANK_F


class StartingWeapons(OptionSet):
    """Which weapons Zero starts with.
    The weapon will still start at its first tier, and progressive unlocks (charge attacks and saber combos) will need to be unlocked.
    If this is left empty, one random weapon is granted instead.
    
    Valid Keys: {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}"""
    display_name = "Starting Weapons"
    valid_keys = {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}
    default = frozenset({"Buster", "Z-Saber"})

class Itemsanity(Toggle):
    """Makes every static energy and E-Crystal pickup a location check (82 in total)."""
    display_name = "Itemsanity"


class ExtraLifeSanity(DefaultOnToggle):
    """Makes every 1-UP pickup a location check (10 in total)."""
    display_name = "Extra Life Sanity"


class SelectButton(Choice):
    """Select buttons functionality.

    Cycle Sub Weapon (Default)
    Cycle Main Weapon
    Cycle Head Chip
    Cycle Body Chip
    Cycle Foot Chip
    Use Subtank (Uses fullest Subtank)
    """
    display_name = "Select Button"
    option_cycle_sub_weapon = Data.AP_SELECT_CYCLE_SUB_WEAPON
    option_cycle_main_weapon = Data.AP_SELECT_CYCLE_MAIN_WEAPON
    option_cycle_head_chip = Data.AP_SELECT_CYCLE_HEAD_CHIP
    option_cycle_body_chip = Data.AP_SELECT_CYCLE_BODY_CHIP
    option_cycle_foot_chip = Data.AP_SELECT_CYCLE_FOOT_CHIP
    option_use_subtank = Data.AP_SELECT_USE_SUBTANK
    default = option_cycle_sub_weapon


class CyberElves(Choice):
    """Modifications to Cyber Elf usage. Satellite elves remain unmodified.

    Vanilla: Unmodified Vanilla. Upgrading elves cost eCrystals, fusion elves decrease rank.
    No Penalty: Fusing an elf does not affect rank.
    Auto: Every passive elf received via disk is automatically opened and applied. 
    Does not affect rank. Gives the game a nice sense of progression, but makes it a lot easier.
    """
    display_name = "Cyber-elves"
    option_vanilla = Data.AP_ELVES_VANILLA
    option_no_penalty = Data.AP_ELVES_NO_PENALTY
    option_auto = Data.AP_ELVES_AUTO
    default = option_vanilla


class WeaponDamageUpgrades(DefaultOnToggle):
    """Whether the last three steps of each progressive weapon raise its damage.

    A few players disliked this feature since it departed the gameplay from vanilla.

    WIP: Disabling this still keeps the extra three progressive weapon items in the pool, 
    they just don't provide any bonuses.
    """
    display_name = "Weapon Damage Upgrades"


class RandomizedPalettes(Toggle):
    """Every stage is drawn in a randomly chosen color scheme."""
    display_name = "Randomized Palettes"


class RandomizeEnemies(Toggle):
    """
    Randomize each enemy spawn location.
    WARNING: VERY EARLY WORK IN PROGRESS. DO NOT TAKE INTO BIG MULTIWORLDS!
    This mode is very buggy, see the readme section to know what to expect.
    Recommended to enable enemy disk markers!
    """
    display_name = "Randomize Enemies (WIP)"


class EnemyDifficulty(Choice):
    """
    Only applies if `randomize_enemies` is enabled. Higher difficulties put more enemies in the spot for one, based off of the health of the spot being replaced.
    Minimal: Tries to match enemy placements by health. If a less health enemy replaces one with more health, place multiple copies at that location.
    Chaos: Places multiple enemies around every spawnpoint regardless of HP or enemy type. Leads to many more enemies per stage. Developer's choice!
    Insanity: Places as many enemies as possible. Tries to prioritize enemies with higher HP. Expect many shield enemies in tight quarters. Good luck!
    """
    display_name = "Randomized Enemy Difficulty (WIP)"
    option_minimal = 0
    option_chaos = 1
    option_insanity = 2
    default = 0


class DiskNamePopup(DefaultOnToggle):
    """
    When a Secret Disk arrives from Archipelago, a message box prints its contents.

    The visual is slightly screen obscuring, so it is kept optional.
    """
    display_name = "Disk Name Popup"


class EnemyDiskMarkers(DefaultOnToggle):
    """
    Show a small Archipelago logo above enemies that can drop disks.
    Recommended with enemy randomizer!
    """
    display_name = "Enemy Disk Markers"


class LegacyStages(Choice):
    """
    Adds stages from the other Mega Man Zero series games to this seed.
    Just Zero 2 is added so far.
    Enemy Randomizer, Stage Palette Randomizer, Itemsanity, and Lifesanity are not current supported for these stages.

    You will need to add your Zero 2 ROM to zero2_rom_file under MMZero3_settings in host.yaml,
    located in your root Archipelago directory.

    Shuffle: keeps a total of 16 stages, with Zero 2 stages taking place of some of Zero 3's stages (see Legacy Shuffle Count).
    The final stage is always Zero 3's Abandoned Research Factory. 
    
    All: adds every Zero 2 stage beside Zero 3's, for a total of 32 stages.
    """
    display_name = "Legacy Stages"
    option_off = 0
    option_shuffle = 1
    option_all = 2
    default = 0


class CutSecretDisks(Toggle):
    """
    WARNING: This option will leave Secret Disks out of your seed during generation.

    Zero 2 stages have far fewer locations than the Zero 3 stages they replace, so a Legacy Stages shuffle with
    many zero 2 levels, combined with a small shop, and no itemsanity/lifesanity can have more items than locations. 
    This will cause generation to fail. This setting attempts to fix this problem by cutting down on the number of 
    secret disks in the Zero 3 game. This will only remove enemy and lore disks first, removing cosmetic related disks next.

    Off, a seed that cannot generate will refuses to generate. This lets you add more checks through the shop or other means.

    On, certain Secret Disks are left out until the game can succeed in generation. 
    """
    display_name = "Cut Secret Disks"


class LegacyShuffleCount(NamedRange):
    """How many of Zero 3's 15 stages Zero 2 stages replace, with Legacy Stages on shuffle."""
    display_name = "Legacy Shuffle Count"
    range_start = 0
    range_end = 15
    default = 0
    special_range_names = {"coin_flip": 0}


class InfiniteLives(Toggle):
    """Get infinite lives."""
    display_name = "Infinite Lives"


class AttackModeB(Toggle):
    """
    Start a new game with the attack mode set to Type B instead of Type A.
    You can still change it in game after the fact. This is just to save you several seconds every time you start a new game.
    """
    display_name = "Attack Mode B"


class DoubleTapDash(DefaultOnToggle):
    """Tapping left or right twice dashes, as how it works in the vanilla game. Disable to dash only with the dash button."""
    display_name = "Double-Tap Dash"


class ShopSlots(Range):
    """How many slots Cerveau's shop stocks."""
    display_name = "Shop Slots"
    range_start = 0
    range_end = 48
    default = 16


class ShopPriceScale(Range):
    """How expensive Cerveau's shop is, as a percentage.

    Items range from 70 to 700 eCrystals, with most being in the 100 to 300 range.
    """
    display_name = "Shop Price Scale"
    range_start = 25
    range_end = 400
    default = 100

class TrapPercentage(Range):
    """The percentage of filler items that are replaced with traps."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class EnabledTraps(OptionSet):
    """
    Which traps may be placed. Right now, all are currently visual only.
    Valid Keys: {"Earthquake", "Pixelate", "Slippery Floor"}
    """
    display_name = "Enabled Traps"
    valid_keys = {"Earthquake", "Pixelate", "Slippery Floor"}
    default = frozenset(valid_keys)


mmzero3_option_groups = [
    OptionGroup("Goal Options", [
        RequiredSecretDisks,
        FinalStageRank,
    ]),
    OptionGroup("Sanity Options", [
        ExtraLifeSanity,
        Itemsanity,
        ShopSlots,
        ShopPriceScale,
        LegacyStages,
        LegacyShuffleCount,
        CutSecretDisks,
    ]),
    OptionGroup("Optional Randomization", [
        RandomizeEnemies,
        EnemyDifficulty,
    ]),
    OptionGroup("Gameplay", [
        StartingWeapons,
        WeaponDamageUpgrades,
        SelectButton,
        CyberElves,
        ExSkillRank,
        InfiniteLives,
        AttackModeB,
        DoubleTapDash,
        DeathLink,
    ]),
    OptionGroup("Traps", [
        TrapPercentage,
        EnabledTraps,
    ]),
    OptionGroup("Aesthetics", [
        RandomizedPalettes,
        DiskNamePopup,
        EnemyDiskMarkers,
    ]),
]


@dataclass
class MMZero3Options(PerGameCommonOptions):
    required_secret_disks: RequiredSecretDisks
    ex_skill_rank: ExSkillRank
    final_stage_rank: FinalStageRank
    starting_weapons: StartingWeapons
    itemsanity: Itemsanity
    extra_life_sanity: ExtraLifeSanity
    randomized_palettes: RandomizedPalettes
    select_button: SelectButton
    weapon_damage_upgrades: WeaponDamageUpgrades
    cyber_elves: CyberElves
    disk_name_popup: DiskNamePopup
    enemy_disk_markers: EnemyDiskMarkers
    infinite_lives: InfiniteLives
    attack_mode_b: AttackModeB
    double_tap_dash: DoubleTapDash
    randomize_enemies: RandomizeEnemies
    enemy_difficulty: EnemyDifficulty
    start_inventory_from_pool: StartInventoryPool
    shop_slots: ShopSlots
    shop_price_scale: ShopPriceScale
    legacy_stages: LegacyStages
    legacy_shuffle_count: LegacyShuffleCount
    cut_secret_disks: CutSecretDisks
    trap_percentage: TrapPercentage
    enabled_traps: EnabledTraps
    death_link: DeathLink
