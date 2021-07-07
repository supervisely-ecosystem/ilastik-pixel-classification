import os

import mode_selector
import train
import settings
import globals as g
import target_classes
import init_ui_progress
import mode_selector as ms


def init(data, state):
    data["ownerId"] = int(os.environ['context.userId'])
    data["mode"] = g.mode

    if g.mode == "Create new Project":
        # state["classifierStatus"] = ms.classifier_status
        state["classifierStatus"] = None
    else:
        #state["classifierStatus"] = ms.remote_classifier_status
        state["classifierStatus"] = None
        state["classesInfo"] = []
        data["trainSet"] = []
        state["newProjectName"] = None
        ms.reset_info(data, state)

    state["loading"] = False
    state["tabName"] = "info"
    #"info" "train" "predict" "settings

    target_classes.init(data, state)
    train.init(data, state)
    settings.init(data, state)
    init_ui_progress.init_progress(data, state)
