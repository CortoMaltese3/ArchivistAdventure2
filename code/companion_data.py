from settings import COMPANION_PATH

COMPANION_NAMES = {500: "laika"}

COMPANION_SPEECHES = {
    500: ["Arf arf!"],
}

def create_npc(id):
    name = COMPANION_NAMES[id]
    sprite_path = COMPANION_PATH / name / "down" / "down_0.png"
    speech = COMPANION_SPEECHES.get(id, ["..."]) # default speech if none found
    return {"id": id, "name": name, "sprite": sprite_path, "speech": speech}

npcs = {id: create_npc(id) for id in COMPANION_NAMES.keys()}
