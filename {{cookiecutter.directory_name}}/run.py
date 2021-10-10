#!/usr/bin/python
# -*- coding: utf-8 -*-
"""run.py
build and run the main program here
"""
import os
import sys
from random import shuffle

from psychopy import core
from psychopy import event
from psychopy import logging
from psychopy import visual
from src.experiment import event_logger
from src.experiment import instructions
from src.experiment import Paradigm
from src.experiment import subject_info
from src.experiment import Text
from src.fileIO import load_conditions_dict
from src.fileIO import load_config

config = load_config()
config["setting"]["logging_level"] = logging.INFO


def run_experiment(config, trials):

    # create experiment
    Experiment = Paradigm(
        escape_key="esc", color=0, window_size=config["settings"]["window_size"]
    )
    fixation = Text(
        window=Experiment.window,
        text="+",
        color="white",
        height=config["settings"]["font_size"],
    )
    trigger = visual.TextStim(
        Experiment.window,
        text="Waiting for scanner.",
        name="trigger",
        pos=[-50, 0],
        height=48,
        wrapWidth=1100,
        color="white",
    )

    startexp = instructions(
        window=Experiment.window,
        instruction_txt=config["instructions"]["exp_txt"],
        color="white",
    )
    endexp = instructions(
        window=Experiment.window,
        instruction_txt=config["instructions"]["end_txt"],
        color="white",
    )

    # hide mouse
    event.Mouse(visible=config["settings"]["mouse_visible"])

    # task instruction
    startexp.show(duration=None)

    if config["modality"] == "mri":

        # wait trigger
        trigger.draw()
        Experiment.window.flip()
        event.waitKeys(keyList=config["fmri_setting"]["trigger"])

        # dummy volumes
        timer = core.Clock()
        fixation.show(
            timer, config["fmri_setting"]["tr"] * config["fmri_setting"]["dummy_vol"]
        )

    # start the clock
    timer = core.Clock()

    # for trial in trials:
    # write your task here

    # quit
    endexp.show(config["fmri_setting"]["tr"])
    Experiment.window.close()
    core.quit()


# now run this thing
if __name__ == "__main__":

    # set working directory as the location of this file
    _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(
        sys.getfilesystemencoding()
    )
    os.chdir(_thisDir)

    # load your experiment trials
    trials = load_conditions_dict(config["trials_file"])
    shuffle(trials)

    # collect participant info
    config = subject_info(config)

    # set log file
    event_logger(config["settings"]["logging_level"], config["info"]["log_file"])

    # run
    run_experiment(config, trials)
