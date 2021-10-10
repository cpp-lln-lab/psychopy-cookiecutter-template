import os
import pytest
import sys

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)

from src.fileIO import *


def test_write_csv():

    root = os.path.dirname(__file__)

    # given
    filename = os.path.join(root, "test_output.csv")
    list_headers = ["onset", "duration", "trial_type"]
    thisTrial = {"onset": 1, "duration": 1, "trial_type": "sound"}

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

    assert fieldnames == ["onset", "duration", "trial_type"]
    assert trials == [
        OrderedDict([("onset", "1"), ("duration", "1"), ("trial_type", "sound")])
    ]

    os.remove(filename)


def test_load_config():

    config = load_config()

    assert config["settings"] == {
        "MRI": False,
        "logging_level": "",
        "mouse_visible": False,
        "window_size": "full_screen",
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


def test_create_filename():

    entities = {
        "extension": ".tsv",
        "modality": "beh",
        "subject": "001",
        "task": "test",
        "suffix": "events",
        "date": "20211011",
    }

    filename = create_filename(entities)

    assert filename == "sub-001/beh/sub-001_task-test_date-20211011_events.tsv"
