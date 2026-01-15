# UE Editor Python
import unreal

# 바꾸고 싶은 목표 LOD 인덱스(-1=자동, 0=LOD0, 1=LOD1, ...)
NEW_FORCED_LOD = 0

def set_lodsync_forced_lod(value: int) -> int:
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not actors:
        unreal.log_warning("[LODSync] 선택된 액터가 없습니다.")
        return 0

    changed = 0
    with unreal.ScopedEditorTransaction("Set LODSync Forced LOD"):
        for actor in actors:
            comps = actor.get_components_by_class(unreal.LODSyncComponent)
            if not comps:
                unreal.log(f"[LODSync] {actor.get_name()}: LODSyncComponent 없음")
                continue

            for comp in comps:
                comp.modify()

                prev = comp.get_editor_property("forced_lod")
                num_lods = comp.get_editor_property("num_lo_ds")  # -1이면 자동 계산(개수 모드)

                # 필요 시 안전하게 클램프 (개수가 설정된 경우에만)
                new_value = int(value)
                if new_value >= 0 and isinstance(num_lods, int) and num_lods > 0:
                    max_idx = num_lods - 1
                    if new_value > max_idx:
                        unreal.log_warning(
                            f"[LODSync] {actor.get_name()}:{comp.get_name()}  "
                            f"요청 LOD={new_value}가 최대 {max_idx}를 넘어 클램프합니다."
                        )
                        new_value = max_idx

                comp.set_editor_property("forced_lod", new_value)

                # 디버그 문자열(현재 매핑/상태) 출력
                try:
                    dbg = comp.get_lod_sync_debug_text()
                except Exception:
                    dbg = ""
                unreal.log(f"[LODSync] {actor.get_name()}:{comp.get_name()}  ForcedLOD {prev} -> {new_value}  {dbg}")

                changed += 1

    # 뷰포트 갱신은 보통 자동으로 되지만, 필요하면 아래 한 줄을 주석 해제하세요.
    # unreal.EditorLevelLibrary.redraw_all_viewports()  # 엔진 버전에 따라 없을 수 있음

    unreal.log(f"[LODSync] 완료: {changed}개 컴포넌트 수정")
    return changed

# 실행
set_lodsync_forced_lod(NEW_FORCED_LOD)
