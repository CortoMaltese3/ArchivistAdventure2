from settings import NPC_PATH

NPC_NAMES = {
    400: "giannis",
    401: "tina",
}


def create_npc(id):
    name = NPC_NAMES[id]
    sprite_path = NPC_PATH / name / "down" / "down_0.png"
    return {"id": id, "name": name, "sprite": sprite_path, "speech": [], "notice_radius": 50}


npcs = {id: create_npc(id) for id in NPC_NAMES.keys()}
