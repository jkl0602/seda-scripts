import unreal

asset_path = "/Game/Developers/USER/BP_Cliff_SingleSlot.BP_Cliff_SingleSlot"
bp_class = unreal.EditorAssetLibrary.load_blueprint_class(asset_path)

spawn_location_base = unreal.Vector(0.0, 0.0, 2000)
spacing = 3000.0
count = 1000

for i in range(count):
    location = spawn_location_base + unreal.Vector((i % 100) * spacing, (i // 100) * spacing, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(bp_class, location)
    actor.set_actor_label(f"BP_{i}")
