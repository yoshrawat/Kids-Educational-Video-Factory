import json
import uuid
import time
import requests
from pathlib import Path


class ComfyUIClient:
    """
    Local ComfyUI client for DreamShaper workflow execution.
    """

    def __init__(self, url: str = "http://127.0.0.1:8188"):
        self.url = url.rstrip("/")

        # ⭐ Resolve workflow path safely (worker-safe)
        # Try multiple possible paths to handle different execution contexts
        possible_paths = [
            Path("workflows/dreamshaper_api.json"),  # From project root
            Path(__file__).resolve().parents[2] / "workflows" / "dreamshaper_api.json",  # From file location
            Path.cwd() / "workflows" / "dreamshaper_api.json",  # Current working directory
        ]

        workflow_path = None
        for path in possible_paths:
            if path.exists():
                workflow_path = path
                break

        if workflow_path is None:
            raise RuntimeError(
                f"DreamShaper workflow missing. Tried:\n"
                + "\n".join(str(p) for p in possible_paths)
                + "\nCreate workflows/dreamshaper_api.json"
            )

        self.workflow_template = json.loads(workflow_path.read_text())

    # -------------------------------------------------------------

    def _deep_copy(self, data: dict) -> dict:
        """Safe deep copy."""
        return json.loads(json.dumps(data))

    # -------------------------------------------------------------

    def _inject_prompt(self, workflow: dict, prompt: str) -> dict:
        """
        Inject dynamic prompt into CLIPTextEncode nodes.
        """
        wf = self._deep_copy(workflow)

        for node in wf.values():
            if node.get("class_type") == "CLIPTextEncode":
                if "text" in node.get("inputs", {}):
                    node["inputs"]["text"] = prompt

        return wf

    # -------------------------------------------------------------

    def _submit_workflow(self, workflow: dict) -> str:
        payload = {
            "prompt": workflow,
            "client_id": str(uuid.uuid4())
        }

        response = requests.post(f"{self.url}/prompt", json=payload)
        response.raise_for_status()

        return response.json()["prompt_id"]

    # -------------------------------------------------------------

    def _wait_for_completion(self, prompt_id: str, timeout: int = 60) -> dict:
        """
        Poll ComfyUI history until image is ready.
        """
        start = time.time()

        while time.time() - start < timeout:
            history = requests.get(f"{self.url}/history/{prompt_id}").json()

            if prompt_id in history:
                return history[prompt_id]

            time.sleep(1)

        raise TimeoutError("ComfyUI generation timed out")

    # -------------------------------------------------------------

    def _extract_image(self, history: dict) -> str:
        """
        Extract generated image path from history.
        """
        for node in history.get("outputs", {}).values():
            if "images" in node:
                image = node["images"][0]
                # Try multiple possible paths for the output directory
                possible_paths = [
                    Path("ComfyUI") / "output" / image["filename"],
                    Path.cwd() / "ComfyUI" / "output" / image["filename"],
                    Path(__file__).resolve().parents[2] / "ComfyUI" / "output" / image["filename"],
                ]
                
                for path in possible_paths:
                    if path.exists():
                        return str(path.resolve())
                
                # If no path exists, return the first one and hope it appears soon
                return str(possible_paths[0].resolve())

        raise RuntimeError("No image found in ComfyUI output")

    # -------------------------------------------------------------

    def generate_image(self, prompt: str) -> str:
        """
        Public API: generate image from prompt.
        """

        workflow = self._inject_prompt(self.workflow_template, prompt)

        prompt_id = self._submit_workflow(workflow)

        history = self._wait_for_completion(prompt_id)

        return self._extract_image(history)