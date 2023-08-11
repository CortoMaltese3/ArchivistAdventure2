from settings import NPC_PATH


def create_npc(num, name):
    # Assuming you want to use the "down" sprite for the NPC
    sprite_path = NPC_PATH / str(num) / "down" / "down_0.png"
    return {"name": name, "sprite": sprite_path, "speech": []}


npcs = {
    400: create_npc(400, "Koula"),
    401: create_npc(401, "Tina"),
}
