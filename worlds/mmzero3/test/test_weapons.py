"""Weapon option matrix tests.

The general test suite only runs default options, where randomize_weapons is off and every
weapon rule is trivially satisfiable. Each class here re-runs the inherited reachability and
fill tests under a different combination.
"""

from . import ALL_WEAPONS, MMZero3TestBase

ROD_GATED_LOCATIONS = [
    "Aegis Volcano Base (4) 114: Push 1st Container",
    "Oceanic Highway Ruins (1) 005: 1st Pit Breakable",
    "Weapons Repair Factory (2) 115: Hit 3rd Hammer",
    "Old Residential (1) 039: 1st Door",
    "Old Residential (3) 112: Floor Breakables",
    "Forest of Anatre (8) 040: Breakables Below Boss Room",
    "Giant Elevator (2) 041: 1st Passage High Ledges",
    "Giant Elevator (6) 027: 1st Descent Bottom Left Breakable",
]


class TestWeaponsDefaultOptions(MMZero3TestBase):
    options = {}

    def test_weapon_invariants(self) -> None:
        self.assert_weapon_invariants()


class TestWeaponsNotRandomized(MMZero3TestBase):
    options = {"randomize_weapons": False}

    def test_weapon_invariants(self) -> None:
        self.assert_weapon_invariants()

    def test_all_weapons_owned(self) -> None:
        self.assertEqual(self.world.starting_weapons, set(ALL_WEAPONS))


class TestWeaponsRandomizedEmptyStart(MMZero3TestBase):
    options = {"randomize_weapons": True, "starting_weapons": set()}

    def test_weapon_invariants(self) -> None:
        self.assert_weapon_invariants()

    def test_a_weapon_is_granted(self) -> None:
        # An empty start would leave Zero unable to damage anything.
        self.assertEqual(len(self.world.starting_weapons), 1)


class TestWeaponsStartWithRecoilRod(MMZero3TestBase):
    options = {"randomize_weapons": True, "starting_weapons": {"Recoil Rod"}}

    def test_weapon_invariants(self) -> None:
        self.assert_weapon_invariants()

    def test_recoil_rod_not_in_pool(self) -> None:
        self.assertNotIn("Recoil Rod", [item.name for item in self.multiworld.itempool])

    def test_rod_gated_locations_reachable(self) -> None:
        # Starting with the rod must open these; they must not require finding a
        # Recoil Rod item that was never created.
        state = self.multiworld.get_all_state(False)
        for location in ROD_GATED_LOCATIONS:
            self.assertTrue(
                state.can_reach_location(location, self.player),
                f"{location} is unreachable despite starting with the Recoil Rod",
            )


class TestWeaponsStartWithAll(MMZero3TestBase):
    options = {"randomize_weapons": True, "starting_weapons": set(ALL_WEAPONS)}

    def test_weapon_invariants(self) -> None:
        self.assert_weapon_invariants()

    def test_no_weapons_in_pool(self) -> None:
        pool = [item.name for item in self.multiworld.itempool]
        for weapon in ALL_WEAPONS:
            self.assertNotIn(weapon, pool)


class TestWeaponsRandomizedPartialStart(MMZero3TestBase):
    options = {"randomize_weapons": True, "starting_weapons": {"Buster", "Z-Saber"}}

    def test_weapon_invariants(self) -> None:
        self.assert_weapon_invariants()

    def test_complement_is_in_pool(self) -> None:
        pool = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Buster", pool)
        self.assertNotIn("Z-Saber", pool)
        self.assertIn("Recoil Rod", pool)
        self.assertIn("Shield Boomerang", pool)
