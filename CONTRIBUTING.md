# Code contribution guidelines

- All code contributions must adhere to [the PEP8 style guide](https://peps.python.org/pep-0008/).
- New dependencies should be avoided to keep the program easy to install and vet.
- Passwords, usernames, IP addresses, ports, and other sensitive system information should be kept out of the code.
- Please follow the established folder structure. For example, do not put API wrapper code outside of the `api` folder.
- Tooltips and code should call datasets "dataset" and not "data-set" when possible to keep the code consistent
- It's recommended to have Ruff installed in your editor to utitlize the Ruff linting rules set for the project

# Documentation guidelines

- Documentation should be devoid of jokes and not be written from the perspective of a person.
- Documentation should avoid making too many assumptions about users.
