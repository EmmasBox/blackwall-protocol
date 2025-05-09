
secrets = [
    "PASS",
    "PASSWORD",
    "PHRASE",
    "PASSPHRASE",
    "BINDPW",
]

redact_message = ">REDACTED SECRET"

def remove_secret(string_input: str) -> str:
    """Scrubs passwords and passphrases from commands"""
    string_input = string_input.upper()
    for secret in secrets:
        secret_start = string_input.find(secret + "(")
        if secret_start != -1:
            secret_end = string_input.find(")")
            return string_input[:secret_start] + string_input[secret_end+1:] + redact_message
    return string_input