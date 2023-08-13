from settings import NPC_PATH


def create_npc(id, name):
    # Assuming you want to use the "down" sprite for the NPC
    sprite_path = NPC_PATH / name / "down" / "down_0.png"
    return {"id": id, "name": name, "sprite": sprite_path, "speech": [], "notice_radius": 50}


npcs = {
    400: create_npc(id=400, name="Koula"),
    401: create_npc(id=401, name="Tina"),
}
