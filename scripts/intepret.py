import sys
import shared

sys.path.insert(1, str(shared.ROOT))
from project.language.interpreter import interpret_file


if __name__ == "__main__":
    try:
        print(interpret_file(sys.argv[1]))
    except Exception as e:
        print("\ERROR: " + str(e))
