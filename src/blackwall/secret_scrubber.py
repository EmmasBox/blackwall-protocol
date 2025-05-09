
secrets = [
    "pass(",
    "password(",
    "phrase(",
    "passphrase(",
]

def remove_secret(string_input: str) -> str:
    string_input = string_input
    for secret in secrets:
        secret_start = string_input.find(secret)
        if secret_start is not -1:
            secret_end = string_input.find(")")
            return string_input[:secret_start] + string_input[secret_end:]
    return string_input