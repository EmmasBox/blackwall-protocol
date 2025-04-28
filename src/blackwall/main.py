#Project by Emma Skovgaard

#Enables true colors to be active by default
from os import environ

if "TEXTUAL_COLOR_SYSTEM" not in environ:
    environ["TEXTUAL_COLOR_SYSTEM"] = "truecolor"

import importlib.util

from .app import Blackwall

spec = importlib.util.find_spec('textual_image')

if spec:
    import textual_image.renderable  # noqa: F401
else:
    print("##BLKWL_ERROR_3 Warning: could not find textual-image")    

def main():
    Blackwall().run()

if __name__ == "__main__":
    main()
