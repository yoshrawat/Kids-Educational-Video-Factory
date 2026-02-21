# infrastructure/video/comfyui_client.py
import json
import uuid
import requests
import time
from pathlib import Path


class ComfyUIClient:

    def __init__(self, url="http://127.0.0.1:8188"):
        self.url = url
        self.workflow = json.loads(
            Path("workflows/dreamshaper_api.json").read_text()
        )

    def generate_image(self, prompt: str) -> str:
        wf = self.workflow.copy()

        # inject prompt dynamically
        for node in wf.values():
            if node.get("class_type") == "CLIPTextEncode":
                node["inputs"]["text"] = prompt

        payload = {"prompt": wf, "client_id": str(uuid.uuid4())}

        requests.post(f"{self.url}/prompt", json=payload)

        time.sleep(5)

        output = list(Path("ComfyUI/output").glob("*.png"))
        return str(output[-1])