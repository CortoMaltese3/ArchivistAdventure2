from src.settings import paths

# weapons
weapon_data = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": paths.WEAPONS_DIR / "sword" / "full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "graphic": paths.WEAPONS_DIR / "lance" / "full.png",
    },
    "shovel": {
        "cooldown": 200,
        "damage": 15,
        "graphic": paths.WEAPONS_DIR / "shovel" / "full.png",
    },
    "pickaxe": {
        "cooldown": 150,
        "damage": 20,
        "graphic": paths.WEAPONS_DIR / "pickaxe" / "full.png",
    },
}
