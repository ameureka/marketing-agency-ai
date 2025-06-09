# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""logo_create_agent: for creating logos"""

import os

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import ToolContext, load_artifacts
from google.genai import Client, types

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06" 
MODEL_IMAGE = "imagen-3.0-generate-002"

load_dotenv()

# Only Vertex AI supports image generation for now.
client = Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)


def generate_image(img_prompt: str, tool_context: "ToolContext"):
    """Generates an image based on the prompt."""
    try:
        print(f"[DEBUG] Starting image generation with prompt: {img_prompt[:100]}...")
        
        # 生成图像
        response = client.models.generate_images(
            model=MODEL_IMAGE,
            prompt=img_prompt,
            config={"number_of_images": 1},
        )
        
        if not response.generated_images:
            print("[ERROR] No images generated from the API response")
            return {"status": "failed", "error": "No images generated"}
        
        print(f"[DEBUG] Successfully generated {len(response.generated_images)} image(s)")
        
        # 获取图像字节数据
        image_bytes = response.generated_images[0].image.image_bytes
        print(f"[DEBUG] Image bytes length: {len(image_bytes)}")
        
        # 创建Part对象
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
        print(f"[DEBUG] Created Part object with mime_type: {image_part.inline_data.mime_type}")
        
        # 保存到artifacts
        print("[DEBUG] Attempting to save artifact...")
        tool_context.save_artifact("image.png", image_part)
        print("[DEBUG] Artifact saved successfully")
        
        # 验证保存是否成功
        try:
            saved_artifacts = tool_context.load_artifacts()
            print(f"[DEBUG] Available artifacts after save: {list(saved_artifacts.keys()) if saved_artifacts else 'None'}")
        except Exception as e:
            print(f"[WARNING] Could not verify saved artifacts: {e}")
        
        return {
            "status": "success",
            "detail": "Image generated successfully and stored in artifacts.",
            "filename": "image.png",
            "image_size_bytes": len(image_bytes)
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in generate_image: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "failed", 
            "error": f"{type(e).__name__}: {str(e)}"
        }


logo_create_agent = Agent(
    model=MODEL,
    name="logo_create_agent",
    description=(
        "An agent that generates images and answers "
        "questions about the images."
    ),
    instruction=prompt.LOGO_CREATE_PROMPT,
    output_key="logo_create_output",
    tools=[generate_image, load_artifacts],
)
