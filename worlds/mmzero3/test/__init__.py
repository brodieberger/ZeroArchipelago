from test.bases import WorldTestBase

from ..Options import StartingWeapons

ALL_WEAPONS = frozenset(StartingWeapons.valid_keys)


class MMZero3TestBase(WorldTestBase):
    game = "Mega Man Zero 3"

    def assert_weapon_invariants(self) -> None:
        """Zero always owns a weapon, and every weapon is either owned or placed, never both."""
        starting = self.world.starting_weapons
        pool = [item.name for item in self.multiworld.itempool]

        self.assertTrue(starting, "Zero must start with at least one weapon")
        self.assertTrue(
            starting <= ALL_WEAPONS,
            f"starting_weapons contains unknown weapons: {starting - ALL_WEAPONS}",
        )

        for weapon in ALL_WEAPONS:
            if weapon in starting:
                self.assertNotIn(weapon, pool, f"{weapon} is owned at start but was also placed")
            else:
                self.assertIn(weapon, pool, f"{weapon} is neither owned at start nor placed")

        self.assertEqual(sorted(starting), self.world.fill_slot_data()["starting_weapons"])
