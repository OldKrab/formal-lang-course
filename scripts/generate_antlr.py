import os
import shared
import subprocess


if __name__ == "__main__":
    os.chdir(shared.LANGUAGE)
    subprocess.check_call(
        [
            "antlr4",
            "-Dlanguage=Python3",
            "-o",
            "antlr_generated",
            "-visitor",
            shared.LANGUAGE_GRAMMAR,
        ]
    )
