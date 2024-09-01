import pathlib
import tomllib

import requests

config_path = pathlib.Path("../config.toml")

if not config_path.exists():
    raise FileNotFoundError("config.toml not found")

with open(config_path, "rb") as f:
    config = tomllib.load(f)

XI_API_KEY = config["elevenlabs"]["api_key"]

headers = {
    "Accept": "application/json",
    "xi-api-key": XI_API_KEY,
    "Content-Type": "application/json",
}

response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)

for voice in response.json()["voices"]:
    print(f"{voice['name']}; {voice['voice_id']}")
