import unreal

# 블루프린트 액터 경로 (필요에 따라 수정)
BLUEPRINT_PATH = "/Game/Developers/USER/BP_Single"  # 예: /Game/Blueprints/BP_MyActor

# 에디터 라이브러리 인스턴스
editor_asset_lib = unreal.EditorAssetLibrary
editor_level_lib = unreal.EditorLevelLibrary

# 블루프린트 클래스 로드
actor_class = editor_asset_lib.load_blueprint_class(BLUEPRINT_PATH)
if not actor_class:
    unreal.log_error(f"블루프린트 클래스를 찾을 수 없습니다: {BLUEPRINT_PATH}")
else:
    for i in range(33):
        # 위치 설정 (예: X축으로 1000씩 간격)
        location = unreal.Vector(i * 1000.0, 0.0, 0.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)

        # 액터 스폰
        actor = editor_level_lib.spawn_actor_from_class(actor_class, location, rotation)
        if actor:
            unreal.log(f"액터 스폰 완료: 인덱스 {i}")
        else:
            unreal.log_error(f"액터 스폰 실패: 인덱스 {i}")
