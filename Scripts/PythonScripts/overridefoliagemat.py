import unreal

def try_struct_override():
    editor_world = unreal.EditorLevelLibrary.get_editor_world()
    actors = unreal.GameplayStatics.get_all_actors_of_class(editor_world, unreal.InstancedFoliageActor)

    for actor in actors:
        components = actor.get_components_by_class(unreal.FoliageInstancedStaticMeshComponent)

        for comp in components:
            static_mesh = comp.static_mesh
            if not static_mesh:
                continue

            materials = static_mesh.get_editor_property("static_materials")
            for mat_elem in materials:
                material_interface = mat_elem.material_interface
                if not material_interface:
                    continue

                if isinstance(material_interface, unreal.MaterialInstanceConstant):
                    try:
                        # BasePropertyOverrides 구조체 가져오기
                        overrides = material_interface.get_editor_property("base_property_overrides")
                        # 구조체 안의 override flag 켜기
                        overrides.set_editor_property("override_blend_mode", True)
                        # 구조체 안의 blend_mode 설정
                        overrides.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)

                        # 변경 적용
                        material_interface.set_editor_property("base_property_overrides", overrides)
                        material_interface.mark_package_dirty()

                        unreal.log(f"Set blend_mode to Opaque for: {material_interface.get_name()}")
                    except Exception as e:
                        unreal.log_warning(f"Failed on: {material_interface.get_name()} — {e}")

# 실행
try_struct_override()
