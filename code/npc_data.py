from settings import NPC_PATH

NPC_NAMES = {
    400: "giannis",
    401: "tina",
}

NPC_SPEECHES = {
    400: ["Hello, I'm Giannis. Welcome to the town!"],
    401: ["Hi there, I'm Tina. Have a great day!"],
}

def create_npc(id):
    name = NPC_NAMES[id]
    sprite_path = NPC_PATH / name / "down" / "down_0.png"
    speech = NPC_SPEECHES.get(id, ["Hello, adventurer!"]) # default speech if none found
    return {"id": id, "name": name, "sprite": sprite_path, "speech": speech, "notice_radius": 150}

npcs = {id: create_npc(id) for id in NPC_NAMES.keys()}
