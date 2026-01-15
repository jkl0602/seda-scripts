import unreal

# 블루프린트 액터 경로
BLUEPRINT_PATH = "/Game/Developers/USER/BP_Multi"  # 실제 경로로 수정하세요

# 머티리얼 인스턴스 경로 템플릿
MATERIAL_PATH_TEMPLATE = "/Game/Developers/USER/Materials/Instances/MM_Base_{:02d}_Inst"

# 에디터 라이브러리 인스턴스
editor_asset_lib = unreal.EditorAssetLibrary
editor_level_lib = unreal.EditorLevelLibrary

# 블루프린트 클래스 로드
actor_class = editor_asset_lib.load_blueprint_class(BLUEPRINT_PATH)
if not actor_class:
    unreal.log_error(f"블루프린트 클래스를 찾을 수 없습니다: {BLUEPRINT_PATH}")
else:
    # 머티리얼 인스턴스 로드
    material_instances = []
    for i in range(99):
        material_path = MATERIAL_PATH_TEMPLATE.format(i)
        material = editor_asset_lib.load_asset(material_path)
        if not material:
            unreal.log_error(f"머티리얼 인스턴스를 찾을 수 없습니다: {material_path}")
        material_instances.append(material)

    # 액터 배치
    for actor_index in range(33):
        # 위치 설정 (예: X축으로 200씩 간격)
        location = unreal.Vector(actor_index * 1000.0, 0.0, 0.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)

        # 액터 스폰
        actor = editor_level_lib.spawn_actor_from_class(actor_class, location, rotation)
        if not actor:
            unreal.log_error(f"액터 스폰 실패: 인덱스 {actor_index}")
            continue

        # Static Mesh Component 가져오기
        static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
        if not static_mesh_component:
            unreal.log_error(f"Static Mesh Component를 찾을 수 없습니다: 액터 인덱스 {actor_index}")
            continue

        # 머티리얼 할당
        for slot_index in range(3):
            material_index = actor_index * 3 + slot_index
            if material_index >= len(material_instances):
                break
            material = material_instances[material_index]
            if material:
                static_mesh_component.set_material(slot_index, material)
