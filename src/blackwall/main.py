#Project by Emma Skovgaard

#Enables true colors to be active by default
from os import environ
if "TEXTUAL_COLOR_SYSTEM" not in environ:
    environ["TEXTUAL_COLOR_SYSTEM"] = "truecolor"

from .app import Blackwall

def main():
    Blackwall().run()

if __name__ == "__main__":
    main()
