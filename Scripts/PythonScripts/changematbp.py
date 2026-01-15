import unreal

def reset_actor_materials_to_mesh_defaults(actor: unreal.Actor):
    smcs = actor.get_components_by_class(unreal.StaticMeshComponent)

    if not smcs:
        unreal.log_warning(f"{actor.get_name()}에는 StaticMeshComponent가 없습니다.")
        return

    for smc in smcs:
        mesh = smc.static_mesh
        if not mesh:
            unreal.log_warning(f"{actor.get_name()}의 {smc.get_name()}에 스태틱 메시가 없습니다.")
            continue

        # StaticMeshComponent가 가진 머티리얼 슬롯 수 기준으로 루프
        num_slots = smc.get_num_materials()

        for i in range(num_slots):
            try:
                default_mat = mesh.get_material(i)
                if default_mat:
                    smc.set_material(i, default_mat)
                    unreal.log(f"{actor.get_name()} - {smc.get_name()} 슬롯 {i} → 메시 기본 머티리얼로 리셋 완료")
            except Exception as e:
                unreal.log_warning(f"{actor.get_name()} - {smc.get_name()} 슬롯 {i} 머티리얼 접근 실패: {e}")

# ✅ EditorActorSubsystem을 통한 액터 선택
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
selected_actors = editor_actor_subsystem.get_selected_level_actors()

for actor in selected_actors:
    reset_actor_materials_to_mesh_defaults(actor)
