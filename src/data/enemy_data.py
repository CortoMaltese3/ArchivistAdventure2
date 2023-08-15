from settings import AUDIO_PATH

# enemy
monster_data = {
    "scarab": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "slash",
        "attack_sound": AUDIO_PATH / "attack" / "slash.wav",
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
        "attack_sound": AUDIO_PATH / "attack" / "fireball.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
