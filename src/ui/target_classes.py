import supervisely_lib as sly
import globals as g


def init(data, state):
    state["classesInfo"] = None
    state["selectedClasses"] = None


def refresh_classes():
    g.refresh_meta()

    classes_info = []
    selected_classes = {}
    for obj_class in g.project_meta.obj_classes:
        obj_class: sly.ObjClass
        if obj_class.geometry_type in [sly.Bitmap, sly.AnyGeometry]:
            classes_info.append(obj_class.to_json())
            selected_classes[obj_class.name] = True

    fields = [
        {"field": "state.classesInfo", "payload": classes_info},
        {"field": "state.selectedClasses", "payload": selected_classes},
    ]
    g.api.app.set_fields(g.task_id, fields)