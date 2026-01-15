import unreal

# 복제할 원본 머티리얼 경로
SOURCE_MATERIAL_PATH = "/Game/Developers/USER/Materials/MM_Base"  # 예시 경로

# 복제할 개수
NUM_DUPLICATES = 100

# 에셋 툴 및 에디터 라이브러리 인스턴스
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_asset_lib = unreal.EditorAssetLibrary

# 원본 머티리얼 로드
source_material = editor_asset_lib.load_asset(SOURCE_MATERIAL_PATH)
if not source_material:
    unreal.log_error(f"원본 머티리얼을 찾을 수 없습니다: {SOURCE_MATERIAL_PATH}")
else:
    # 원본 머티리얼 이름과 폴더 경로 추출
    source_name = source_material.get_name()
    source_path = editor_asset_lib.get_path_name_for_loaded_asset(source_material)
    folder_path = "/".join(source_path.split("/")[:-1])

    for i in range(NUM_DUPLICATES):
        new_name = f"{source_name}_{i:02d}"
        new_asset_path = f"{folder_path}/{new_name}"

        # 동일한 이름의 에셋이 이미 존재하는지 확인
        if editor_asset_lib.does_asset_exist(new_asset_path):
            unreal.log_warning(f"에셋이 이미 존재합니다: {new_asset_path}")
            continue

        # 머티리얼 복제
        duplicated_material = asset_tools.duplicate_asset(new_name, folder_path, source_material)
        if duplicated_material:
            unreal.log(f"복제 완료: {new_asset_path}")
        else:
            unreal.log_error(f"복제 실패: {new_asset_path}")
