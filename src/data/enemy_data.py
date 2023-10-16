from src.settings import paths

# enemy
monster_data = {
    "scarab": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "slash",
        "attack_sound": paths.ENEMY_AUDIO_DIR / "slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
    "book": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "thunder",
        "attack_sound": paths.ENEMY_AUDIO_DIR / "fireball.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
