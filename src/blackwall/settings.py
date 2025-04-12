import tomllib
from pathlib import Path

default_user_config_name = "./blackwall_user_config.toml"
default_site_config_name = "/etc/blackwall_site_config.toml"

site_config_path = Path(default_site_config_name)

if site_config_path.exists():
    site_config = site_config_path.open().read()
    site_settings = tomllib.loads(site_config)

user_config_path = Path(default_user_config_name)

if user_config_path.exists():
    user_config = user_config_path.open().read()
    user_settings = tomllib.loads(user_config)

def get_site_setting(section: str,setting: str):
    #load settings from site config
    if site_config_path.exists():
        return site_settings[section][setting]
    else:
        return None

def get_user_setting(section: str,setting: str):
    #load settings from user config
    if user_config_path.exists():
        return user_settings[section][setting]
    else:
        return None
