import unreal

# 🔧 셀 크기 설정: 프로젝트의 World Partition Grid Cell Size와 일치시켜 주세요
CELL_SIZE = 51200
WORLD = unreal.EditorLevelLibrary.get_editor_world()

# 1. ActorDesc 목록 수집
descs = unreal.WorldPartitionBlueprintLibrary.get_actor_descs()
if not descs:
    unreal.log_error("ActorDesc를 가져올 수 없습니다.")
    raise RuntimeError("get_actor_descs failed")

# 2. 셀 기준으로 StaticMeshActor 레이블 그룹화
cells = {}
for desc in descs:
    # 아웃라이너에 있는 실제 액터가 StaticMeshActor인지 나중에 확인합니다
    bounds = desc.bounds
    center = (bounds.min + bounds.max) * 0.5
    cx = int(center.x // CELL_SIZE)
    cy = int(center.y // CELL_SIZE)
    cells.setdefault((cx, cy), []).append(desc.label)

# 3. 에디터 액터 서브시스템으로 레벨 액터 받아오기
actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = actor_subsys.get_all_level_actors()  # :contentReference[oaicite:1]{index=1}

# 4. 셀 폴더로 정리
with unreal.ScopedEditorTransaction("Group StaticMeshActors by Cell Folder"):
    for (cx, cy), labels in cells.items():
        folder = f"Cell_{cx}_{cy}"
        for actor in all_actors:
            # StaticMeshActor인지 확인하고, 라벨이 그룹에 포함된 경우만 폴더 배정
            if isinstance(actor, unreal.StaticMeshActor) and actor.get_actor_label() in labels:
                actor.set_folder_path(folder)

unreal.log("✅ StaticMeshActor 클래스만 셀 폴더로 분류 완료")
