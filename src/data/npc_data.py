from src.settings import paths

NPC_NAMES = {
    400: "giannis",
    401: "tina",
    402: "ioanna"
}

NPC_SPEECHES = {
    400: ["Quick! We need to save my godfather!"],
    401: ["What happened? You look pale! Here, drink this homemade potion!"],
    402: ["They did what? They took my brother? NOBODY MESSES WITH MY BROTHER.. AAAAARGHHHH"],
}

NPC_WEAPON_GRANT = {400: "sword"}

NPC_MAGIC_GRANT = {402: "flame", 401: "heal"}


def create_npc(id):
    name = NPC_NAMES[id]
    sprite_path = paths.NPC_DIR / name / "down" / "down_0.png"
    speech = NPC_SPEECHES.get(id, ["Hello, Archivist!"])  # default speech if none found
    weapon = NPC_WEAPON_GRANT.get(id, None)
    magic = NPC_MAGIC_GRANT.get(id, None)
    npc = {
        "id": id,
        "name": name,
        "sprite": sprite_path,
        "speech": speech,
        "notice_radius": 80,
        "weapon": weapon,
        "magic": magic,
    }
    return npc


npcs = {id: create_npc(id) for id in NPC_NAMES.keys()}
