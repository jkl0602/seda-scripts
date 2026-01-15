import unreal
from itertools import product

# 기본 설정
BASE_MATERIAL_PATH = "/Game/Developers/USER/Test2/MM_TB"
STATIC_MESH_PATH = "/Game/Developers/USER/Cliff_Multi"
OUTPUT_FOLDER = "/Game/Developers/USER/Test2/Instances"
INSTANCE_NAME_FORMAT = "MI_StaticTest_{:03d}"
ACTOR_LABEL_FORMAT = "StaticTestActor_{:03d}"
SPAWN_LOCATION_BASE = unreal.Vector(0, 0, 0)
SPACING = 2000.0
ACTOR_COUNT = 1000

# Static Switch Parameter 목록
SWITCH_PARAMS = ["UseNoise", "UseWPO", "UseSine", "UseTex"]

# 에디터 API 접근
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_level_lib = unreal.EditorLevelLibrary
asset_lib = unreal.EditorAssetLibrary
material_editing_lib = unreal.MaterialEditingLibrary

# 베이스 머티리얼 및 메시 로드
base_material = asset_lib.load_asset(BASE_MATERIAL_PATH)
if not base_material:
    unreal.log_error(f"Base material not found: {BASE_MATERIAL_PATH}")
    raise RuntimeError("Missing base material")

static_mesh = asset_lib.load_asset(STATIC_MESH_PATH)
if not static_mesh:
    unreal.log_error(f"Static mesh not found: {STATIC_MESH_PATH}")
    raise RuntimeError("Missing static mesh")

# 스태틱 스위치 조합 생성
def generate_permutations(param_names, count):
    combos = list(product([True, False], repeat=len(param_names)))
    result = []
    i = 0
    while len(result) < count:
        combo = combos[i % len(combos)]
        result.append(dict(zip(param_names, combo)))
        i += 1
    return result

switch_combinations = generate_permutations(SWITCH_PARAMS, ACTOR_COUNT)
material_instances = []

# 머티리얼 인스턴스 생성
for i, switch_set in enumerate(switch_combinations):
    instance_name = INSTANCE_NAME_FORMAT.format(i)
    instance_path = f"{OUTPUT_FOLDER}/{instance_name}"

    material_instance = asset_tools.create_asset(
        asset_name=instance_name,
        package_path=OUTPUT_FOLDER,
        asset_class=unreal.MaterialInstanceConstant,
        factory=unreal.MaterialInstanceConstantFactoryNew()
    )

    material_instance.set_editor_property("parent", base_material)

    for param, value in switch_set.items():
        material_editing_lib.set_material_instance_static_switch_parameter_value(material_instance, param, value)

    asset_lib.save_asset(instance_path)
    material_instances.append(material_instance)

unreal.log("✅ Material instances created.")

# 액터 배치
for i in range(ACTOR_COUNT):
    spawn_loc = unreal.Vector(0, i * SPACING, 0)
    actor = editor_level_lib.spawn_actor_from_class(unreal.StaticMeshActor, spawn_loc)
    actor.set_actor_label(ACTOR_LABEL_FORMAT.format(i))

    smc = actor.static_mesh_component
    smc.set_static_mesh(static_mesh)
    smc.set_material(0, material_instances[i])
    smc.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

unreal.log("✅ All actors placed with material instances.")
