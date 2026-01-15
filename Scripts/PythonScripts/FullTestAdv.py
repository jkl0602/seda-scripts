import unreal
from itertools import product

# 설정
#BASE_MATERIAL_PATH = "/Game/Developers/USER/Test2/MM_TB"
BASE_MATERIAL_PATH = "/Game/Developers/USER/Test2/MM_TB_S"
STATIC_MESH_PATH = "/Game/Developers/USER/Cliff_Multi"
OUTPUT_FOLDER = "/Game/Developers/USER/Test2/Instances"
INSTANCE_NAME_FORMAT = "MI_StaticTest_{:03d}"
ACTOR_LABEL_FORMAT = "StaticTestActor_{:03d}"
SPACING = 2000.0
ACTOR_COUNT = 1000
#STATIC_SWITCH_PARAMS = ["UseNoise", "UseWPO", "UseSine", "UseTex"]
STATIC_SWITCH_PARAMS = []

# 에디터 API
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_level_lib = unreal.EditorLevelLibrary
asset_lib = unreal.EditorAssetLibrary
material_editing_lib = unreal.MaterialEditingLibrary

# 베이스 자산 로드
base_material = asset_lib.load_asset(BASE_MATERIAL_PATH)
static_mesh = asset_lib.load_asset(STATIC_MESH_PATH)

if not base_material or not static_mesh:
    raise RuntimeError("필수 자산 로드 실패")

# 메시의 머티리얼 슬롯 수 확인
num_material_slots = static_mesh.get_num_sections(0)  # LOD 0 기준
if num_material_slots == 0:
    num_material_slots = 1

# 모든 Static Switch 조합 생성 (2^4 = 16개)
def generate_static_switch_permutations(param_names):
    return [dict(zip(param_names, vals)) for vals in product([True, False], repeat=len(param_names))]

switch_combinations = generate_static_switch_permutations(STATIC_SWITCH_PARAMS)
material_instances = []

# 전체 작업량 계산 (인스턴스 생성 + 액터 배치)
TOTAL_STEPS = len(switch_combinations) + ACTOR_COUNT

with unreal.ScopedSlowTask(TOTAL_STEPS, "머티리얼 생성 및 액터 배치 중...") as slow_task:
    slow_task.make_dialog(True)

    # 머티리얼 인스턴스 생성 (16개)
    for i, switch_set in enumerate(switch_combinations):
        if slow_task.should_cancel():
            break

        mi_name = INSTANCE_NAME_FORMAT.format(i)
        mi_path = f"{OUTPUT_FOLDER}/{mi_name}"

        material_instance = asset_tools.create_asset(
            asset_name=mi_name,
            package_path=OUTPUT_FOLDER,
            asset_class=unreal.MaterialInstanceConstant,
            factory=unreal.MaterialInstanceConstantFactoryNew()
        )

        material_instance.set_editor_property("parent", base_material)

        for param, value in switch_set.items():
            material_editing_lib.set_material_instance_static_switch_parameter_value(material_instance, param, value)

        asset_lib.save_asset(mi_path)
        material_instances.append(material_instance)

        slow_task.enter_progress_frame(1, f"{i+1}/{len(switch_combinations)} 머티리얼 생성 중...")

    # 액터 배치: 정사각형 그리드 + 원점 기준 중앙 정렬
    grid_size = int(ACTOR_COUNT ** 0.5)
    if grid_size * grid_size < ACTOR_COUNT:
        grid_size += 1

    half_extent = (grid_size - 1) * SPACING * 0.5

    actor_index = 0
    for y in range(grid_size):
        for x in range(grid_size):
            if actor_index >= ACTOR_COUNT or slow_task.should_cancel():
                break

            loc_x = x * SPACING - half_extent
            loc_y = y * SPACING - half_extent
            location = unreal.Vector(loc_x, loc_y, 0)

            actor = editor_level_lib.spawn_actor_from_class(unreal.StaticMeshActor, location)
            actor.set_actor_label(ACTOR_LABEL_FORMAT.format(actor_index))

            smc = actor.static_mesh_component
            smc.set_static_mesh(static_mesh)
            smc.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

            for slot in range(num_material_slots):
                mi = material_instances[(actor_index * num_material_slots + slot) % len(material_instances)]
                #mi = material_instances[slot]
                smc.set_material(slot, mi)

            slow_task.enter_progress_frame(1, f"{actor_index+1}/{ACTOR_COUNT} 액터 배치 중...")
            actor_index += 1

unreal.log("✅ 작업 완료: 머티리얼 인스턴스 생성 및 액터 배치")
