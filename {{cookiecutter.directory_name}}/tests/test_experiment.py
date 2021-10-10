import os
import sys

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)

from psychopy import data
from src.experiment import subject_info


def test_subject_info():

    config = {
        "info": {
            "experiment": "test",
            "subject": "001",
            "session": "",
            "run": "",
            "task_name": "test",
            "modality": "beh",
        },
        "settings": {"debug": True},
    }

    config = subject_info(config)

    assert (
        config["info"]["data_file"]
        == "sub-001/beh/sub-001_task-test_date-"
        + data.getDateStr(format="%Y%b%d%H%M")
        + "_events.tsv"
    )


# def test_Paradigm():

#     config = {"settings": {"window_size": "full_screen"}}

#     Experiment = Paradigm(
#         esc_key="esc", color=0, window_size=config["settings"]["window_size"]
#     )
