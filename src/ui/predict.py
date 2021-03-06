import os
import cache
import subprocess
import numpy as np
import globals as g
import init_directories
import supervisely_lib as sly

import target_classes


@g.my_app.callback("rm_predictions")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def remove_predicted_labels(api: sly.Api, task_id, context, state, app_logger):
    try:
        image_id = context['imageId']
        ann_info = g.api.annotation.download(image_id).annotation

        if g.project_id != context["projectId"]:
            meta_json = g.api.project.get_meta(context["projectId"])
            meta = sly.ProjectMeta.from_json(meta_json)
            ann_json = g.api.annotation.download(image_id).annotation
            ann = sly.Annotation.from_json(ann_json, meta)
        else:
            ann = sly.Annotation.from_json(ann_info, g.project_meta)
        for label in ann.labels:
            if g.prediction_tag in label.tags:
                ann = ann.delete_label(label)
        g.api.annotation.upload_ann(image_id, ann)
        api.task.set_field(task_id, "state.loading", False)
    except Exception as e:
        api.task.set_field(task_id, "state.loading", False)
        raise e


@g.my_app.callback("predict")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def predict(api: sly.Api, task_id, context, state, app_logger):
    try:
        if g.project_id != context["projectId"]:
            target_classes.synchronise_meta(api, task_id, context, state, app_logger)

        image_id = context['imageId']
        ann, img_path = cache.download_test(image_id, context["projectId"])
        ilp_path = os.path.join(init_directories.proj_dir, f'{g.project.name}.ilp')
        if not os.path.exists(ilp_path):
            api.task.set_field(task_id, "state.loading", False)
            raise Exception("No trained classifier detected")

        test_cmd = f"/ilastik-build/ilastik-1.4.0b14-Linux/run_ilastik.sh " \
                   f"--headless " \
                   f"--project='{ilp_path}' " \
                   f"--export_source='Simple Segmentation' " \
                   f"--output_format='png' " \
                   f"'{img_path}' "

        sly.logger.info("Testing", extra={"command": test_cmd})
        bash_out = subprocess.Popen([test_cmd], shell=True, executable="/bin/bash", stdout=subprocess.PIPE).communicate()
        output_log = bash_out[0]
        error_log = bash_out[1]
        seg_img_name = sly.fs.get_file_name(img_path) + "_Simple Segmentation.png"
        seg_path = os.path.join(os.path.dirname(img_path), seg_img_name)
        #os.rename(img_path, seg_path)
        img = sly.image.read(seg_path)
        mask = img[:, :, 0]
        labels = []
        selected_classes = target_classes.get_classes()
        machine_map = target_classes.generate_machine_map(selected_classes)
        for class_name in selected_classes:
            color = machine_map[class_name][0]
            mask_bool = mask == color
            if not np.any(mask_bool):
                g.my_app.logger.info(f"Mask for class: {class_name} is empty")
                continue
            labels.append(sly.Label(sly.Bitmap(mask_bool), g.project_meta.get_obj_class(class_name), tags=sly.TagCollection([g.prediction_tag])))

        ann = ann.add_labels(labels)
        api.annotation.upload_ann(image_id, ann)
        sly.fs.clean_dir(init_directories.test_dir)
        api.task.set_field(task_id, "state.loading", False)
    except Exception as e:
        api.task.set_field(task_id, "state.loading", False)
        raise e
