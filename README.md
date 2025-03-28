#### Stability notice
This software is still in pre-alpha and under active development, do not use it on production systems. Features might not work yet and there are numerous bugs in the ones that do work to some extent.

![pypi/v/blackwall](https://badgen.net/pypi/v/blackwall) ![pypi/dm/blackwall](https://badgen.net/pypi/dm/blackwall) 

![Blackwall Logo](blackwall_banner.svg)
# Blackwall Protocol
Blackwall Protocol is a terminal based administration panel for RACF. Blackwall is meant to be easier to install and use than many previous attempts at creating mainframe security administration software. Previous attempts from major companies to make software like this are very clunky to use because they're built around 3270 protocols, which are quite limited compared to a modern SSH session connecting to a Unix environment. Blackwall incorporates dynamic and true color, tool tips, dynamic UI, dynamically re-sizable windows, and tabs to give a better user experience. The tab driven design of Blackwall allows security administrators and engineers to have a lot of stuff open at once, this is a major advantage over other programs in this space. Blackwall however is not just a fancy text based user interface for people new to the mainframe, it also allows you to submit TSO and RACF commands from an always visible command line, input can then be viewed either through a tab or a separate screen. This command line is very handy if the action you want to perform is very simple, pulling up a new tab for that can be very overkill. The Blackwall command line also comes with rudimentary command autocompletion, to further speed up power users. Blackwall is designed to be used for everyone, both power users and seasoned security specialists.

Blackwall does not support ACF2 or Top Secret and never will, people are more than welcome to fork it and create their own versions however.

## Features
- Execute TSO commands
- Create and modify users
- Create and modify dataset profiles

## Dependencies
### Required dependencies:
#### System dependencies
- z/OS 2.4 or later
- OpenSSH installed and configured on z/OS (for connecting to z/OS Unix, OMVS in ISPF won't work)
- Python 3.11 or later
#### Python packages
- Textual 3.0.0 or later (For UI)
- [RACFU](https://github.com/ambitus/racfu) (To communicate with RACF)
  - RACFU being a dependency also indirectly also means you need the IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space configured

### Optional dependencies:
#### Python packages
- [ZOAU 1.3.4.x or later](https://www.ibm.com/docs/en/zoau/1.3.x) (For gathering system information like LPAR name, not required but highly recommended)

## Installation
As mentioned in the dependencies section, before you install you will have to install Python and ZOAU yourself before installing Blackwall. You also need to make sure IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space are configured correctly. 

If you your environment is not airgapped pip will install Blackwall and it's dependencies automatically, by running the command below:
```
pip install blackwall
```
If your environment is airgapped you will also have to download and install [Textual](https://pypi.org/project/textual/) and [RACFU](https://pypi.org/project/racfu/) manually by downloading the wheel/whl files and uploading them to the mainframe, make sure you get the correct minimum versions.
After you've [downloaded Blackwall](https://pypi.org/project/blackwall/) upload the .whl package to the machine through Zowe Explorer or SSH and run the pip command in the folder with the .whl file like so:
```
pip install blackwall-<REPLACE WITH VERSION>-py3-none-any.whl 
```

## Required permissions
Make sure each user that is supposed to use this software has access to the following RACF profiles:

| Class    | Profile             | Access | Reason |
|----------|---------------------|--------|--------|
| FACILITY |IRR.RADMIN.LISTUSER | Read   |Needed to extract user information       |
| FACILITY |IRR.RADMIN.LISTGRP  | Read   |Needed to extract group information       |
| FACILITY |IRR.RADMIN.RLIST    | Read   |Needed to extract general resource profile information       |
| FACILITY |IRR.RADMIN.LISTDSD   | Read   |Needed to extract dataset profile information     |
| FACILITY |IRR.RADMIN.SETROPTS.LIST | Read   |Needed to extract RACF system settings     |
| XFACILIT |IRR.IRRSMO00.PRECHECK    | Update   |Needed to create new profiles in RACF and modify things     |

It's probably best to create a group with each of the required resources, this group can be named after the program.

## Supported terminals
Not all terminals are capable of displaying advanced TUI applications. Below is a list of terminals that have been tested on whether they work or not. Terminals not in list might work.
| Terminal         | Supported | Notes |
|------------------|-----------|-------|
| VS Code          | Yes*          |You must set minimum contrast ratio to 1, otherwise certain UI elements will not be displayed correctly causing a degraded user experience       |
| Windows Terminal | Yes          |       |
| Blackbox         | Yes          |       |
| TSO OMVS in z/OS | No          |       |
| Default terminal on Raspbian | No          |       |
| Kitty | Yes          |       |
| Alacritty | Yes          |       |

## Running Blackwall Protocol
Once you have installed Blackwall and have the required permissions you can start Blackwall simply by typing the blackwall command in an SSH session, through a supported terminal:
```
>blackwall
```