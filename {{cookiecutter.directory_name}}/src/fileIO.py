# -*- coding: utf-8 -*-
"""fileIO.py
file input/output functions
"""
import codecs
import csv
import os
import re
import stat
from collections import OrderedDict

import yaml
from bids.layout.writing import build_path


def create_dir(directory):
    """

    create a directory if it doesn't exist.

    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def parse_instructions(input_data):
    """
    parse instruction into pages
    page break is #
    """

    return re.findall(r"([^#]+)", input_data)


def load_instruction(PATH):
    """
    load and then parse instrucition
    return a list
    """

    with codecs.open(PATH, "r", encoding="utf8") as f:
        input_data = f.read()

    return parse_instructions(input_data)


def load_conditions_dict(condition_file):
    """
    load each row as a dictionary with the headers as the keys
    save the headers in its original order for data saving
    """

    with codecs.open(condition_file, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        trials = [row for row in reader]

        # save field names as a list in order
        fieldnames = reader.fieldnames

    return trials, fieldnames


def create_headers(list_headers):
    """
    create ordered headers for the output data csv file
    """

    headers = [(header, None) for header in list_headers]

    return OrderedDict(headers)


def write_csv(fileName, list_headers, thisTrial):
    """
    append the data of the current trial to the data file
    if the data file has not been created, this function will create one


    attributes

    fileName: str
        the file name generated when capturing participant info

    list_headers: list
        the headers in a list, will pass on to function create_headers

    thisTrial: dict
        a dictionary storing the current trial
    """

    full_path = os.path.abspath(fileName)
    directory = os.path.dirname(full_path)
    create_dir(directory)
    fieldnames = create_headers(list_headers)

    if not os.path.isfile(full_path):
        # headers and the first entry
        with codecs.open(full_path, "ab+", encoding="utf8") as f:
            dw = csv.DictWriter(f, fieldnames=fieldnames)
            dw.writeheader()
            dw.writerow(thisTrial)
    else:
        with codecs.open(full_path, "ab+", encoding="utf8") as f:
            dw = csv.DictWriter(f, fieldnames=fieldnames)
            dw.writerow(thisTrial)


def read_only(path):
    """
    change the mode to read only
    """
    os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def load_config():

    root = os.path.join(os.path.dirname(__file__), "..")
    config_file = os.path.join(root, "config", "config.yml")

    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        print(config)
        return config


def create_filename(config, extension=".tsv"):

    entities = {
        "suffix": "events",
        "extension": extension,
        "modality": config["info"]["modality"],
        "subject": config["info"]["subject"],
        "session": config["info"]["session"],
        "task": config["info"]["task_name"],
        "run": config["info"]["run"],
        "date": config["info"]["date"],
    }

    if entities["modality"] == "mri":
        entities["modality"] = "func"

    patterns = [
        "sub-{subject}[/ses-{session}][/{modality<func|beh|eeg|meg>}]/"
        "sub-{subject}[_ses-{session}]"
        "[_task-{task}][_run-{run}]"
        "[_date-{date}]"
        "_{suffix<events|beh>}"
        "{extension<.json|.tsv>}"
    ]

    return build_path(entities, patterns)
