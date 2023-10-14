from settings import paths

NPC_NAMES = {
    400: "giannis",
    401: "tina",
}

NPC_SPEECHES = {
    400: ["Quick! We need to save my godfather!"],
    401: ["What happened? You look pale! Here, drink this homemade potion!"],
}


def create_npc(id):
    name = NPC_NAMES[id]
    sprite_path = paths.NPC_DIR / name / "down" / "down_0.png"
    speech = NPC_SPEECHES.get(id, ["Hello, Archivist!"])  # default speech if none found
    return {"id": id, "name": name, "sprite": sprite_path, "speech": speech, "notice_radius": 80}


npcs = {id: create_npc(id) for id in NPC_NAMES.keys()}
