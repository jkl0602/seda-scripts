import unreal
import math

# === 사용자 입력 값 ===
sm_path = "/Game/Developers/oyj/01.01"  # 스폰할 액터의 BP 클래스 경로
total_count = 10000   # 생성할 총 개수
spacing = 3000       # 액터 간 간격 (cm)

# === 에디터 월드 컨텍스트 가져오기 ===
editor_level_lib = unreal.EditorLevelLibrary
spawn_location = unreal.Vector(-10, -30, 750)
rotation = unreal.Rotator(0, 0, 180)

# === 블루프린트 클래스 로딩 ===
staticmesh = unreal.EditorAssetLibrary.load_asset(sm_path)
if not staticmesh:
    unreal.log_error(f"Staticmesh 를 찾을 수 없습니다: {sm_path}")
    raise RuntimeError("invalid sm_path")

# === 배치 계산 ===
# 정사각형 그리드로 배치할 행/열 수 계산
side_count = math.ceil(math.sqrt(total_count))

# 전체 그리드의 크기 계산
grid_width = (side_count - 1) * spacing
half_grid = grid_width / 2

# 액터 스폰
for i in range(total_count):
    row = i // side_count
    col = i % side_count

    x = (col * spacing) - half_grid
    y = (row * spacing) - half_grid
    location = unreal.Vector(x, y, 0) + spawn_location

    actor = editor_level_lib.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
    if not actor:
        unreal.log_warning(f"{i}번째 액터 스폰 실패")

    static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if not static_mesh_component:
        unreal.log_error(f"Static Mesh Component를 찾을 수 없습니다: 액터 인덱스 {i}")
        continue
    static_mesh_component.set_static_mesh(staticmesh)
