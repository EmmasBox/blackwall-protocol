import tomllib
from pathlib import Path

default_user_config_name = ".config/blackwall/user_config.toml"
default_site_config_name = "/etc/blackwall/site_config.toml"

site_config_path = Path(default_site_config_name)

if site_config_path.exists():
    site_config = site_config_path.open().read()
    site_settings = tomllib.loads(site_config)
else:
    site_settings = None

user_config_path = Path.home()/default_user_config_name

if user_config_path.exists():
    user_config = user_config_path.open().read()
    user_settings = tomllib.loads(user_config)
else:
    user_settings = None

def extract_setting(conf_dict: dict | None,section: str, setting: str):
    if conf_dict is not None:
        section_dict = conf_dict.get(section)
        if section_dict is not None:
            return section_dict.get(setting)
    return None

def get_site_setting(section: str,setting: str):
    #load settings from site config
    return extract_setting(conf_dict=site_settings,section=section,setting=setting)

def get_user_setting(section: str,setting: str):
    #load settings from user config
    return extract_setting(conf_dict=user_settings,section=section,setting=setting)
