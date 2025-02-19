# Blackwall Protocol
Blackwall Protocol is a terminal based administration panel for RACF. The goal of Blackwall is to create a more modern and open source alternative to zSecure. Blackwall does not support ACF2 or Top Secret and never will, people are more than welcome to fork it and create their own versions however.

## Dependencies
Required dependencies:
- z/OS 2.4 or later
- Python 3.13 or later
- Textual (For UI)
- [RACFU](https://github.com/ambitus/racfu) (To communicate with RACF)

Optional dependencies:
- [ZOAU 1.3.4.x or later](https://www.ibm.com/docs/en/zoau/1.3.x) (For gathering system information like LPAR name, not required but highly recommended)
