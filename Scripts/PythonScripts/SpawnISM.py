import unreal
import math

# 설정
BP_CLASS_PATH = "/Game/Developers/USER/Test2/BP_ISM"  # InstancedStaticMeshComponent 포함 BP
STATIC_MESH_PATH = "/Game/Developers/USER/Cliff_Multi"
INSTANCE_COUNT = 1000
SPACING = 2000.0

# 자산 로드
bp_class = unreal.EditorAssetLibrary.load_blueprint_class(BP_CLASS_PATH)
static_mesh = unreal.EditorAssetLibrary.load_asset(STATIC_MESH_PATH)

if not bp_class or not static_mesh:
    unreal.log_error("블루프린트 클래스 또는 메시 자산 로드 실패")
    raise RuntimeError("경로 확인 필요")

# 액터 생성
editor_level_lib = unreal.EditorLevelLibrary
actor = editor_level_lib.spawn_actor_from_class(bp_class, unreal.Vector(0, 0, 0))
actor.set_actor_label("NaniteISMCActor")

# ISMC 컴포넌트 가져오기
components = actor.get_components_by_class(unreal.InstancedStaticMeshComponent)
if not components:
    unreal.log_error("BP에 InstancedStaticMeshComponent가 존재하지 않습니다.")
    raise RuntimeError("BP 구성 확인 필요")

ismc = components[0]
ismc.set_static_mesh(static_mesh)

# 배치: 정사각형 형태로 XY 방향 배치, 원점 중심 정렬
grid_size = math.ceil(math.sqrt(INSTANCE_COUNT))  # 한 변의 인스턴스 수
half_extent = (grid_size - 1) * SPACING * 0.5      # 중심 보정

placed = 0
for y in range(grid_size):
    for x in range(grid_size):
        if placed >= INSTANCE_COUNT:
            break

        loc_x = x * SPACING - half_extent
        loc_y = y * SPACING - half_extent
        transform = unreal.Transform(location=unreal.Vector(loc_x, loc_y, 0))
        ismc.add_instance(transform)
        placed += 1

unreal.log(f"✅ InstancedStaticMeshComponent에 Nanite 메시 인스턴스 {placed}개 배치 완료 (정사각형, 중심 정렬)")
