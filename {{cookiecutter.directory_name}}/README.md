# {{cookiecutter.experiment_name}}

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Author: {{cookiecutter.author}}

```
├── docs                    <- Testing related documents i.e. consent forms
├── instructions            <- Instructions in the experiment
│   ├── end_instr.txt       <- Ending message
│   └── instruction.txt     <- Starting message/instructions
├── references              <- References related to this experiment's design etc.
├── src                     <- Source code for use
│   ├── __init__.py         <- Make src a Python module
│   ├── experiment.py       <- Experiment related functions
│   ├── fileIO.py           <- File reading/writing related functions
│   └── trial_generator.py  <- Experiment trial generation functions (optional).
├── stimuli                 <- Experiment stimuli
│   ├── audio
│   │   └── README.md
│   ├── images
│   │   └── README.md
│   ├── trials.csv          <- Pre-generated trials (optional).
│   └── video
│       └── README.md
├── tests
│   ├── stimuli
│   │   └── trials.csv
│   ├── test_experiment.py
│   └── test_fileIO.py
├── README.md               <- The README for people developing/using this experiment
└── run.py                  <- The main experiment code. The task is constructed here.

```

## Installing

Install all the necessary packages in a conda environment.

```
conda env update -f ./environment.yml
conda activate {{cookiecutter.experiment_name}}
```

---

<p align="center">
    <a href="https://cookiecutter.readthedocs.io/en/1.7.2/" target="_blank" style="margin: 20px">
        <img    alt="Cookiecutter"
                src="https://raw.githubusercontent.com/cookiecutter/cookiecutter/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/cookiecutter_medium.png"
                height=50px>
    </a>
    <a href="https://www.psychopy.org/" target="_blank" style="margin: 20px">
        <img    alt="PsychoPy"
                src="https://www.psychopy.org/_static/psychopyLogoType3_h240.png"
                height=50px>
    </a>
</p>
