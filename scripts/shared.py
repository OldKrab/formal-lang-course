import os
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
DOCS = ROOT / "docs"
TESTS = ROOT / "tests"
PROJECT = ROOT / "project"
LANGUAGE = PROJECT / "language"
LANGUAGE_GRAMMAR = LANGUAGE / "Language.g4"


def configure_python_path():
    python_path = os.getenv("PYTHONPATH")

    if python_path is None:
        os.environ["PYTHONPATH"] = str(ROOT)
    else:
        os.environ["PYTHONPATH"] += ";" + str(ROOT)
    print("Configure python path: ", os.getenv("PYTHONPATH"))
