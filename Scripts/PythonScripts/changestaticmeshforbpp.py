import unreal

# 📁 설정: 대상 폴더 (콘텐츠 브라우저 상의 경로)
TARGET_FOLDER = "/Game/Developers/JK/Assets/BPPs"  # 여기에 대상 폴더 경로 입력
# 🎯 교체할 Static Mesh (콘텐츠 브라우저 경로)
NEW_MESH_PATH = "/Game/Developers/oyj/01.01"  # 교체할 메시 경로

new_mesh = unreal.load_asset(NEW_MESH_PATH)
if not isinstance(new_mesh, unreal.StaticMesh):
    raise RuntimeError(f"❌ 메시 로드 실패: {NEW_MESH_PATH}")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
filter = unreal.ARFilter(
    package_paths=[TARGET_FOLDER],
    class_names=["Blueprint"],
    recursive_paths=False
)
assets = registry.get_assets(filter)
print(f"🔍 총 {len(assets)}개의 블루프린트 검색됨")

for asset_data in assets:
    blueprint_path = asset_data.package_name
    blueprint_class = unreal.EditorAssetLibrary.load_blueprint_class(blueprint_path)
    if not blueprint_class:
        print(f"⚠️ 클래스 로드 실패: {blueprint_path}")
        continue

    # 클래스의 CDO에서 구성요소 접근
    cdo = unreal.get_default_object(blueprint_class)
    if not cdo:
        print(f"⚠️ CDO 없음: {blueprint_path}")
        continue

    components = cdo.get_components_by_class(unreal.InstancedStaticMeshComponent)
    modified = False
    for comp in components:
        current_mesh = comp.get_editor_property("static_mesh")
        if current_mesh != new_mesh:
            comp.set_editor_property("static_mesh", new_mesh)
            modified = True
            print(f"🔧 메시 교체: {asset_data.asset_name}")

    if modified:
        # 저장 (GeneratedClass 수정은 CDO를 기반으로 반영됨)
        unreal.EditorAssetLibrary.save_asset(blueprint_path, only_if_is_dirty=False)

print("✅ 메시 교체 완료")