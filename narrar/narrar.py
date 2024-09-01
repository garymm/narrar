import base64
import pathlib
import sys
import tomllib

import cv2
from openai import OpenAI

config_path = pathlib.Path("config.toml")

if not config_path.exists():
    raise FileNotFoundError("config.toml not found")

with open(config_path, "rb") as f:
    config = tomllib.load(f)

openai_api_key = config["openai"]["api_key"]


# This part based on
# https://cookbook.openai.com/examples/gpt_with_vision_for_video_understanding
openai = OpenAI(api_key=openai_api_key)

source_path = pathlib.Path(sys.argv[1])

source_video = cv2.VideoCapture(source_path)

base_64_frames = []
while source_video.isOpened():
    success, frame = source_video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base_64_frames.append(base64.b64encode(buffer).decode("utf-8"))

source_video.release()
print(len(base_64_frames), "frames read.")

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            (
                "These are frames from a video. Create a short voiceover script in the "
                "style of David Attenborough narrating a BBC nature documentary. "
                "Only include the narration."
            ),
            *map(lambda x: {"image": x, "resize": 768}, base_64_frames[0::50]),
        ],
    },
]
openai_params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 1000,
}

result = openai.chat.completions.create(**openai_params)
best_narration = result.choices[0].message.content
print(result.choices[0].message.content)
