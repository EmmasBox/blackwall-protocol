# Blackwall Protocol
Blackwall Protocol is a terminal based administration panel for RACF. The goal of Blackwall is to create a more modern and open source alternative to zSecure. Blackwall does not support ACF2 or Top Secret and never will, people are more than welcome to fork it and create their own versions however.

## Dependencies
### Required dependencies:
- z/OS 2.4 or later
- Python 3.13 or later
- Textual (For UI, bundled with the program)
- [RACFU](https://github.com/ambitus/racfu) (To communicate with RACF, bundled with the program)
  - RACFU being a dependency also indirectly also means you need the IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space configured

### Optional dependencies:
- [ZOAU 1.3.4.x or later](https://www.ibm.com/docs/en/zoau/1.3.x) (For gathering system information like LPAR name, not required but highly recommended)

## Installation
As mentioned in dependencies before you install you will have to install Python and ZOAU yourself. You also manually need to make sure IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space are configured. Textual and RACFU are bundled with the program and thus do not need to be installed manually via pip.

## Features
