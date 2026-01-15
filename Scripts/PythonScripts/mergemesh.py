import unreal
from collections import defaultdict

def group_actors_by_mesh_and_material(actors):
    groups = defaultdict(list)

    for actor in actors:
        smcs = actor.get_components_by_class(unreal.StaticMeshComponent)
        if not smcs:
            continue

        smc = smcs[0]
        mesh = smc.static_mesh
        mat = smc.get_material(0)

        if not mesh or not mat:
            continue

        key = (mesh.get_path_name(), mat.get_path_name())
        groups[key].append(actor)

    return groups

def merge_actor_group(actor_list, group_name_suffix):
    if len(actor_list) < 2:
        unreal.log(f"스킵: {group_name_suffix} 그룹은 병합할 액터가 2개 미만입니다.")
        return

    static_mesh_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

    # 병합 옵션 구성
    merge_options = unreal.MergeStaticMeshActorsOptions()
    merge_options.base_package_name = f"/Game/Merged/Merged_{group_name_suffix}"
    merge_options.mesh_merging_settings = unreal.MeshMergingSettings()
    merge_options.mesh_merging_settings.merge_materials = False
    merge_options.mesh_merging_settings.lod_selection_type = unreal.MeshLODSelectionType.ALL_LODS
    merge_options.mesh_merging_settings.generate_light_map_uv = True
    merge_options.mesh_merging_settings.pivot_point_at_zero = True

    result = static_mesh_subsystem.merge_static_mesh_actors(
        actors_to_merge=actor_list,
        merge_options=merge_options
    )

    if result:
        unreal.log(f"[성공] 병합 완료: {result.get_name()}")
    else:
        unreal.log_error(f"[실패] 병합 실패: {group_name_suffix}")


# 선택된 액터로 그룹화 및 병합 실행
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
selected_actors = editor_actor_subsystem.get_selected_level_actors()

groups = group_actors_by_mesh_and_material(selected_actors)

for idx, ((mesh_path, mat_path), actors) in enumerate(groups.items()):
    group_name = f"{idx}"
    merge_actor_group(actors, group_name)
