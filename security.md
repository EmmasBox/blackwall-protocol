# Blackwall Security Policy

## Supported Versions

No current versions are supported, due to the fact that the program is in alpha.

## Reporting a Vulnerability

To report a security vulnerability start a new issue at <https://github.com/EmmasBox/blackwall-protocol/issues> and report it with the "Security issues" template.

## Security pratices for Blackwall

To ensure high security code scanning with Ruff and Bandit has been set up to highlight everything from use of deprecated python modules to serious security vulnerabilities.

Other things this project strives to follow:

- Password fields in the application must be marked as such, to prevent people from seeing passwords if they walk by.
- Passwords must be scrupped from output and command history as much as possible.
- Passwords, usernames, IP addresses, ports, system names, and other secrets must never appear in the code.
- Dependencies should be actively maintained and when possible the Python standard library must be favored over introducing new dependencies.
- APIs should be used over commands whenever possible
