#### Stability notice
This software is still in pre-alpha and under active development, do not use it on production systems. Features might not work yet and there are numerous bugs in the ones that do work to some extent.

![pypi/v/blackwall](https://badgen.net/pypi/v/blackwall) ![pypi/dm/blackwall](https://badgen.net/pypi/dm/blackwall) 

![Blackwall Logo](blackwall_banner.svg)
# Blackwall Protocol
Blackwall Protocol is a terminal based administration panel for RACF. The goal of Blackwall is to create a more modern and open source alternative to zSecure. Blackwall does not support ACF2 or Top Secret and never will, people are more than welcome to fork it and create their own versions however.

## Features
- Execute TSO commands
- Create and modify users

## Dependencies
### Required dependencies:
#### System dependencies
- z/OS 2.4 or later
- OpenSSH installed and configured on z/OS (for connecting to z/OS Unix, OMVS in ISPF won't work)
- Python 3.13 or later
#### Python packages
- Textual (For UI, bundled with the program)
- [RACFU](https://github.com/ambitus/racfu) (To communicate with RACF, bundled with the program)
  - RACFU being a dependency also indirectly also means you need the IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space configured

### Optional dependencies:
#### Python packages
- [ZOAU 1.3.4.x or later](https://www.ibm.com/docs/en/zoau/1.3.x) (For gathering system information like LPAR name, not required but highly recommended)

## Installation
As mentioned in dependencies before you install you will have to install Python and ZOAU yourself before installing Blackwall. You also manually need to make sure IRRSEQ00, IRRSMO00 and RACF Subsystem Address Space are configured. Textual and RACFU are bundled with the program and thus do not need to be installed manually via pip.

```
pip install blackwall
```
or if your environment is airgapped upload the .whl package to the machine through other means and run the pip command in the folder with the .whl file like so:
```
pip install blackwall-<REPLACE WITH VERSION>-py3-none-any.whl 
```

## Required permissions
Make sure each user that is supposed to use this software has access to the following RACF profiles:

| Profile             | Reason |
|---------------------|--------|
| IRR.RADMIN.LISTUSER | Needed to extract user information       |
| IRR.RADMIN.LISTGRP  | Needed to extract group information       |
| IRR.RADMIN.RLIST    | Needed to extract general resource profile information       |
| IRR.RADMIN.LISTDSD   | Needed to extract dataset profile information     |
| IRR.RADMIN.SETROPTS.LIST | Needed to extract RACF system settings     |
| IRR.IRRSMO00.PRECHECK    | Needed to create new profiles in RACF and modify things     |

## Supported terminals
Not all terminals are capable of displaying advanced TUI applications. Below is a list of terminals that have been tested and whether they work or not.
| Terminal         | Supported | Notes |
|------------------|-----------|-------|
| VS Code          | Yes*          |You must set minimum contrast ratio to 1, otherwise certain UI elements will not be displayed correctly causing a degraded user experience       |
| Windows Terminal | Yes          |       |
| Blackbox         | Yes          |       |
| TSO OMVS in z/OS | No          |       |
| Default terminal on Raspbian | No          |       |