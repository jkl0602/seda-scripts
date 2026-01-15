import unreal

# 설정: 적용할 머티리얼 인스턴스 경로
MATERIAL_PATH = '/Game/Developers/USER/MaterialTest/MITest/Instances/MI_Color_0000'  # 여기에 실제 경로를 입력하세요

# 머티리얼 로딩
material = unreal.load_asset(MATERIAL_PATH)
if not material:
    unreal.log_error(f"Material not found at path: {MATERIAL_PATH}")
    raise RuntimeError("Material instance not found")

# 현재 선택된 액터 가져오기
selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

# StaticMeshActor에 대해서만 처리
for actor in selected_actors:
    if not isinstance(actor, unreal.StaticMeshActor):
        continue

    static_mesh_component = actor.static_mesh_component
    static_mesh = static_mesh_component.static_mesh

    if not static_mesh:
        unreal.log_warning(f"{actor.get_name()} has no static mesh assigned.")
        continue

    slot_count = static_mesh_component.get_num_materials()

    # 모든 슬롯에 동일 머티리얼 세팅
    for index in range(slot_count):
        static_mesh_component.set_material(index, material)

    # 변경 사항 적용
    unreal.log(f"Updated materials on {actor.get_name()}")
