from settings import NPC_PATH


def create_npc(num, name):
    return {"name": name, "sprite": NPC_PATH / f"{num}" / "idle.png", "speech": []}


npcs = {
    0: create_npc(0, "Koula"),
    1: create_npc(1, "Tina"),
}
