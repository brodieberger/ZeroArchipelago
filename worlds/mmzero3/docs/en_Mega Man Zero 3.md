# Mega Man Zero 3 Archipelago

Welcome to my project. Things are still under heavy development, but here you will find my development of a custom Archipelago World for Mega Man Zero 3 on the GBA. You should probably read everything here so you know what to expect before playing!

## General Information
- As of right now, the randomized items include: All secret disks, armor chips, EX Skills, subtanks, the four weapons, and E-Crystals as filler.

- To beat the game, the player must defeat the final boss while collecting a configurable number of secret disks (default: 80). You can set this number using the required_secret_disks option in your YAML file.

- EX Skills are awarded based on your score on the level you just completed, rather than on your average score going into that level. (Yes, that's how they worked in the vanilla game).

- You can leave every level at will, except the opening level, the Missile Factory, and Weil's Lab (These levels are tied to in game events). In the vanilla game, you would only escape levels that you have beaten previously. This change will be much more important later once the routing changes are implemented.

- Talking to the operator in the command room and choosing to transfer to a level you have already beaten now asks you how you want to run it. EXPLORE is the vanilla revisit for picking up disks you missed. RETRY MISSION plays the level as a real mission again, so the boss is back and you get another shot at the A+ rank check.

- Pressing SELECT during gameplay swaps your sub weapon to the next one you own. This will be turned into a proper weapon wheel later.

- When Archipelago gives you an item, a small icon pops up over Zero's head with a sound. This is still an early WIP, so most items just show up as the AP logo.

- Collecting certain lore related secret disks will simultaneously unlock a random e-Reader graphical change. A full list can be seen [here](https://tcrf.net/Mega_Man_Zero_3/e-Reader_Functions). 

- All skippable cutscenes are skippable by default.

## Options

- `required_secret_disks`:  
  Set the number of disks needed for completion. Default is 80, max is 180.

- `randomize_weapons`:  
  Puts the Buster, Z-Saber, Recoil Rod and Shield Boomerang into the item pool. With this off you get all four from the start and starting_weapons does nothing.

- `starting_weapons`:  
  Which of the four you begin with when randomize_weapons is on. Those ones stay out of the pool. Zero can't hurt anything bare handed, so if you leave this empty you get one weapon anyway.

- `easy_ex_skill`:  
  Always sends the EX Skill location check at the end of a level, whatever your rank was.

- `death_link`:  
  Standard DeathLink. Dying sends, and receiving kills you.

## Known Bugs

- There's a chance that I may have missed out on a few dialogue related rewards. If there are any issues, please ping me in the discord!

- Retrying a level several times will mess up your overall rank, with the HUD desyncing with what it actually is in game. It looks like the game averages every clear you have ever done. The bosses use that rank to decide whether to use new attacks. Later I will be replacing how that number is worked out when the level select screen goes in, so I've left it alone for now.

- There's probably some more bugs especially with world generation; I haven't done too much testing, so provide any feedback if something goes wrong!

## Planned Features
- Routing changes. 
  - Like how Mega Man 2 limits the available robot masters you could fight until you have the proper AP item, this world should likely do the same. 
  - Either limit stages based off of an entry item (like MM2) or by total collected disk count (like SM64).
- An improved level select screen. 
  - All levels viewable from the start by tabbing from menu to menu.
  - Boss portraits greyed out until you unlock them.
  - Once you have beaten a level it tells you how many disks you have left to find, and your best rank.
- A weapon wheel on SELECT for swapping chips and weapons without opening the menu.
- Progressive weapon upgrades. 
  - The first one gives you the weapon
  - Each one after unlocks an upgrade (similar to Zero 1 and 2).
  - Lastly you get attack power boosts, which are ripped from the E-Reader cards.
  - This will hopefully fix an issue where weapons can be hard to find in the current game.
- Other collectables as location checks. Like static health pickups, extra lives, etc.
- Level, enemy, or entrance randomization.

---
If you have any questions, feel free to contact me on Discord: Stingrays110, though I'd prefer if you kept it to the Zero channel on the Archipelago Discord
