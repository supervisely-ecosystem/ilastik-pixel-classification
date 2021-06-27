import globals as g
import supervisely_lib as sly

import ui             # for instance
from ui import ui     # for debug

import train
import predict

# imports to register callbacks
# import model_io


#@TODO: remove utils.py
#@TODO: show modal window ValueError("Unknown level 'debug'. Supported levels: ['warning', 'info', 'error']")
#@TODO: create all features
#@TODO: try catch errors
#@TODO: hotkeys
#@TODO: buttons loading
#@TODO: add multiple images to train-headless

#@TODO: launch app from instance
#@TODO: get classes from modal
#@TODO: add message to train tab that model has been trained?
def main():
    sly.logger.info(
        "Script arguments",
        extra={
            "team_id": g.team_id,
            "workspace_id": g.workspace_id,
            "task_id": g.task_id
        }
    )

    data = {}
    state = {}
    ui.init(data, state)

    g.my_app.compile_template(g.root_source_dir)
    g.my_app.run(data=data, state=state)


if __name__ == "__main__":
    sly.main_wrapper("main", main)
