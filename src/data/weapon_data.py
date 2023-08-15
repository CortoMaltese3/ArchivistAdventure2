from settings import WEAPONS_PATH

# weapons
weapon_data = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": WEAPONS_PATH / "sword" / "full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "graphic": WEAPONS_PATH / "lance" / "full.png",
    },
}
