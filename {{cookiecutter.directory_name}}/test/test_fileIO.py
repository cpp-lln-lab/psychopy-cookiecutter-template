import os
import pytest
import sys

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)

from src.fileIO import *

# @pytest.mark.parametrize(
#     "this_schema, dir, basename", [("neurovault", "neurovault", "neurovault")]
# )
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
