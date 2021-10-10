import codecs
import csv
import os
import sys
from collections import OrderedDict

import pytest
from src.fileIO import create_filename
from src.fileIO import load_conditions_dict
from src.fileIO import load_config
from src.fileIO import write_csv

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)


def test_write_csv():

    root = os.path.dirname(__file__)

    # given
    filename = os.path.join(root, "test_output.csv")
    list_headers = ["onset", "duration", "trial_type", "stimulus"]
    thisTrial = {
        "onset": 1,
        "duration": 1,
        "trial_type": "sound",
        "stimulus": "right_left.wav",
    }

    if os.path.isfile(filename):
        os.remove(filename)

    # when
    write_csv(filename, list_headers, thisTrial)

    # then

    with codecs.open(filename, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        trials = [row for row in reader]

        # save field names as a list in order
        fieldnames = reader.fieldnames

    assert fieldnames == ["onset", "duration", "trial_type", "stimulus"]
    assert trials == [
        OrderedDict(
            [
                ("onset", "1"),
                ("duration", "1"),
                ("trial_type", "sound"),
                ("stimulus", "right_left.wav"),
            ]
        )
    ]

    os.remove(filename)


def test_load_config():

    config = load_config()

    assert config["settings"] == {
        "debug": False,
        "logging_level": "INFO",
        "mouse_visible": False,
        "window_size": "full_screen",
        "font_size": 12,
    }
    assert config["fmri_setting"] == {
        "dummy_vol": 3,
        "slice_per_vol": 60,
        "tr": 3,
        "trigger": "t",
    }
    assert config["instructions"] == {
        "end_txt": "./instructions/end_instr.txt",
        "exp_txt": "./instructions/instruction.txt",
    }
    assert config["trials_file"] == "./stimuli/trials.csv"


@pytest.mark.parametrize(
    "modality, session, task, run, filename",
    [
        (
            "beh",
            "",
            "test",
            "",
            "sub-001/beh/sub-001_task-test_date-DATE_events.tsv",
        ),
        (
            "beh",
            "1",
            "test",
            "",
            "sub-001/ses-1/beh/sub-001_ses-1_task-test_date-DATE_events.tsv",
        ),
        (
            "beh",
            "1",
            "test",
            "1",
            "sub-001/ses-1/beh/sub-001_ses-1_task-test_run-1_date-DATE_events.tsv",
        ),
        (
            "mri",
            "",
            "test",
            "",
            "sub-001/func/sub-001_task-test_date-DATE_events.tsv",
        ),
        (
            "eeg",
            "",
            "test",
            "",
            "sub-001/eeg/sub-001_task-test_date-DATE_events.tsv",
        ),
    ],
)
def test_create_filename(modality, session, task, run, filename):

    config = {
        "info": {
            "subject": "001",
            "session": session,
            "run": run,
            "date": "DATE",
            "task_name": task,
            "modality": modality,
        },
    }

    assert create_filename(config) == filename


@pytest.mark.parametrize(
    "extension, filename",
    [
        (".json", "sub-001/beh/sub-001_task-test_date-DATE_events.json"),
    ],
)
def test_create_filename_extension(extension, filename):

    config = {
        "info": {
            "subject": "001",
            "session": "",
            "run": "",
            "modality": "beh",
            "date": "DATE",
            "task_name": "test",
        },
    }

    assert create_filename(config, extension) == filename


def test_load_conditions_dict():

    root = os.path.dirname(__file__)

    condition_file = os.path.join(root, "stimuli", "trials.csv")

    trials, fieldnames = load_conditions_dict(condition_file)

    assert fieldnames == ["block", "trial", "condition", "duration", "ISI"]
