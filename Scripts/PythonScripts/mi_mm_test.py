import unreal
import math
import colorsys

# ====== 사용자 설정 ======
NUM_INSTANCES = 10000  # 생성할 머티리얼 인스턴스 및 액터 수
TEMPLATE_MI_PATH = "/Game/Developers/USER/MaterialTest/MITest/MM_StaticMI_Inst"        # 복제 원본이 될 템플릿 MI 경로
STATIC_MESH_PATH = "/Game/Developers/USER/MaterialTest/MITest/Cliff_Single"             # 사용할 Static Mesh 경로
MI_SAVE_PATH = "/Game/Developers/USER/MaterialTest/MITest/Instances"              # MI 저장 위치
MATERIAL_PARAM_NAME = "BC"                              # 머티리얼 파라미터 이름
ACTOR_LABEL_PREFIX = "ColoredMesh_"
ACTOR_FOLDER = "GeneratedActors"
SPACING = 2000                                           # 액터 간 거리

# ====== 에디터 API 준비 ======
editor_asset_lib = unreal.EditorAssetLibrary()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

# 템플릿 및 메시 자산 로드
template_mi = editor_asset_lib.load_asset(TEMPLATE_MI_PATH)
static_mesh = editor_asset_lib.load_asset(STATIC_MESH_PATH)

if not template_mi:
    raise RuntimeError(f"❌ 템플릿 MI를 찾을 수 없습니다: {TEMPLATE_MI_PATH}")
if not static_mesh:
    raise RuntimeError(f"❌ 스태틱 메시를 찾을 수 없습니다: {STATIC_MESH_PATH}")

# 진행 상태 표시
#task = unreal.ScopedSlowTask(NUM_INSTANCES * 2, f"Generating {NUM_INSTANCES} Material Instances and Actors...")
#task.make_dialog(True)

mi_list = []
needs_save = []

# ====== MI 생성 ======
for i in range(NUM_INSTANCES):
    try:
        name = f"MI_Color_{i:04d}"
        package_path = MI_SAVE_PATH  # 경로: "/Game/Materials/Instances"

        # 복제 실행
        mi = asset_tools.duplicate_asset(
            asset_name=name,
            package_path=package_path,
            original_object=template_mi
        )

        if not mi:
            unreal.log_error(f"❌ 복제 실패: {package_path}/{name}")
            continue

        # 색상 설정 (HSV → RGB)
        hue = i / float(NUM_INSTANCES)
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = unreal.LinearColor(r, g, b, 1.0)
        unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, MATERIAL_PARAM_NAME, color)

        mi_list.append(mi)
        needs_save.append(mi.get_path_name())

    except Exception as e:
        unreal.log_error(f"[MI 복제 루프 예외] {e}")
        continue


# MI 저장
#unreal.EditorAssetLibrary.wait_for_asset_registry()
for path in needs_save:
    if editor_asset_lib.does_asset_exist(path):
        editor_asset_lib.save_asset(path)
    else:
        unreal.log_warning(f"⚠️ 저장 중 자산 누락: {path}")

#del task
# ====== 액터 배치 ======
num_per_side = math.ceil(math.sqrt(NUM_INSTANCES))
offset = (num_per_side - 1) * SPACING / 2.0

for i, mi in enumerate(mi_list):
    #task.enter_progress_frame(1, f"Placing Actor {i+1}/{NUM_INSTANCES}" if i % 10 == 0 else "")

    x = i % num_per_side
    y = i // num_per_side
    location = unreal.Vector((x * SPACING) - offset, (y * SPACING) - offset, 0)

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location)
    actor.set_actor_label(f"{ACTOR_LABEL_PREFIX}{i:04d}")
    actor.set_folder_path(ACTOR_FOLDER)

    comp = actor.static_mesh_component
    comp.set_static_mesh(static_mesh)

    mi = mi_list[i]
    for s in range(comp.get_num_materials()):
        comp.set_material(s, mi)
