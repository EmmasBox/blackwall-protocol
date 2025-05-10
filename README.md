#### Stability notice 🚧

This software is still in a **pre-alpha state** and under active development. **Do not use it on production systems!**
Some features might not work yet, performance might be unsatisfactory, and there are numerous bugs in the features that are implemented.
The current version may not be indicative of the quality in future stable releases.

[![pypi/v/blackwall](https://badgen.net/pypi/v/blackwall)](https://pypi.org/project/blackwall/) [![pypi/python/blackwall](https://badgen.net/pypi/python/blackwall)](https://pypi.org/project/blackwall/) [![pypi/dm/blackwall](https://badgen.net/pypi/dm/blackwall)](https://pypi.org/project/blackwall/) [![security: bandit](https://img.shields.io/github/actions/workflow/status/EmmasBox/blackwall-protocol/.github%2Fworkflows%2Fbandit.yml?label=Bandit%20Security)](https://github.com/PyCQA/bandit) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

![Blackwall Banner](blackwall_banner.svg)

# Blackwall Protocol

Blackwall Protocol is a terminal-based administration panel for [RACF](https://www.ibm.com/products/resource-access-control-facility). As Blackwall is written in Python, it is simple to install via the pip package manager. It is designed to be used via an SSH connection to z/OS UNIX. Blackwall incorporates dynamic and true color, tool tips, dynamic UI, dynamically re-sizable windows, and tabs to give a better user experience. The tab-driven design allows security administrators and engineers to have multiple items open simultaneously. Blackwall also allows you to submit TSO and RACF commands from an always-visible command line. Input can then be viewed either through a tab or a separate screen. The Blackwall command line also comes with rudimentary command autocompletion, to further speed up power users. Blackwall is designed to be used by everyone, both power users and seasoned security specialists.

Blackwall does not support ACF2 or Top Secret. Users are welcome to fork the code and create their own versions.

## Features

- Execute TSO and RACF commands
- Create and modify users
- Create and modify groups
- Create and modify dataset profiles
- Create and modify general resource profiles
- Modify and list system options
- Revert changes done through Blackwall
- Settings customization through toml files

## Planned features

- Certificate management
- Advanced search

## Dependencies

### Required dependencies

#### System dependencies

- z/OS 2.5 or later.
- OpenSSH installed and configured on z/OS (for connecting to z/OS UNIX)
  - OMVS in ISPF does not work due to a lack of terminal features.
- Python 3.12 or later.

#### Python packages

- Textual 3.2.0 or later (for UI)
- [RACFU](https://github.com/ambitus/racfu) 1.0a2-dev2 (To communicate with RACF)
  - RACFU being a dependency means you need the IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space configured.

### Optional dependencies

#### Python packages

- [ZOAU 1.3.4.x or later](https://www.ibm.com/docs/en/zoau/1.3.x) (For gathering system information like LPAR name. Not required but highly recommended)
- [textual-image](https://github.com/lnqs/textual-image), [pillow](https://github.com/python-pillow/Pillow), and [zlib](https://github.com/zopencommunity/zlibport) (For image support)

## Installation

Prior to Blackwall installation, Python and ZOAU must be installed. Ensure the IRRSEQ00, IRRSMO00, and RACF Subsystem Address Space are configured correctly.

If your environment is not airgapped, you can automatically install Blackwall and its dependencies by running the following command:

```sh
pip install blackwall
```

If your environment is airgapped, you will have to download and install [Textual](https://pypi.org/project/textual/) and [RACFU](https://pypi.org/project/racfu/) manually by downloading the wheel/whl files and uploading them to the mainframe. Make sure you get the correct minimum package versions.
After you have [downloaded Blackwall](https://pypi.org/project/blackwall/), upload the .whl package to the machine through Zowe Explorer or SSH and run the pip command in the folder with the .whl file:

```sh
pip install blackwall-<REPLACE WITH VERSION>-py3-none-any.whl
```

### Optional: installing Blackwall with image support

Blackwall has built in support for the [Sixel](https://en.wikipedia.org/wiki/Sixel) format and can use them to display graphics in the terminal.  This could be used for a company logo or other things. This is vastly more complicated to install and does decrease performance, which is why it doesn't come with Blackwall by default. Make sure you have access to zlib on the system. This can be installed from [zopen community](https://zopen.community).

First install pillow with the following command:

```sh
python3 -m pip install --upgrade Pillow -C jpeg=disable
```

Then install textual-image

```sh
pip install textual-image
```

Then install Blackwall with the images dependencies enabled as seen below:

```sh
pip install blackwall[images]
```

## Required permissions

Make sure each user that is supposed to use this software has access to the following RACF profiles:

 Class    | Profile                  | Access | Reason
----------|--------------------------|--------|--------
 FACILITY | IRR.RADMIN.LISTUSER      | Read   | User information
 FACILITY | IRR.RADMIN.LISTGRP       | Read   | Group information
 FACILITY | IRR.RADMIN.RLIST         | Read   | General resource profile information
 FACILITY | IRR.RADMIN.LISTDSD       | Read   | Dataset profile information
 FACILITY | IRR.RADMIN.SETROPTS.LIST | Read   | RACF system settings
 XFACILIT | IRR.IRRSMO00.PRECHECK    | Read   | Create new profiles in RACF and modify things

It is suggested to create a group with each of the required resources. This group can be named "BLACKWAL" after the program.

## Supported terminals

Not all terminals are capable of displaying advanced TUI applications. Below is a list of terminals that have been tested on whether they work or not. Terminals not in the list might work. Asterisks indicate that additional customization might be necessary to get the terminal to work with Blackwall properly.

 Terminal         | Supported | Notes
------------------|-----------|-------
 Alacritty        | Yes*      | Alacritty is only supported if you don't utilize the image support.
 Blackbox         | Yes*      | You must manually enable "Sixel Support" to display images.
 Contour          | Yes       | -
 Kitty            | Yes       | May have issues with displaying multiple images at the same time.
 MacOS terminal   | No        | -
 Raspbian         | No        | -
 TSO OMVS in z/OS | No        | -
 VS Code          | Yes*      | Set `terminal.integrated.minimumContrastRatio` to 1 and enable `terminal.integrated.enableImages`. Otherwise some UI elements will display incorrectly.
 Windows Console  | No        | -
 Windows Terminal | Yes       | Included with Windows 11 and can be installed manually on Windows 10 through the MS app store.

## Running Blackwall Protocol

Once you have installed Blackwall and have the required permissions you can start it by typing the command in an SSH session:

```sh
blackwall
```
