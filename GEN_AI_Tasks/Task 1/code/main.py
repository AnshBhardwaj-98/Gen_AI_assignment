import feedparser
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
import base64
import io
from moviepy import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
import textwrap


CODE_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(CODE_DIR)
OUTPUT_DIR = os.path.join(TASK_DIR, "outputs")
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")


def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ")

def fetch_trending_news():
    print("Fetching trending news...")

    rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        raise Exception("No news articles found!")

    article = feed.entries[0]

    news_title = article.title
    raw_summary = article.summary if 'summary' in article else article.title
    news_summary = clean_html(raw_summary)

    print("News Title:", news_title)
    print("Clean Summary:", news_summary)

    return news_title, news_summary

# ================== CONFIG ==================
USE_LLM_FOR_SCRIPT = True  # set False to force rule-based
_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def generate_script_with_llm(title, summary):
    """
    Gemini-powered script generator.
    Returns a list of 6 scene sentences.
    """
    try:
        prompt = f"""
You are a professional news video script writer.

Write a 30–60 second news video script.
Rules:
- EXACTLY 6 scenes
- One sentence per scene
- Plain text only
- No numbering, no bullets

News Title:
{title}

News Summary:
{summary}
"""

        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            return None

        lines = [
            line.strip("-• ").strip()
            for line in response.text.split("\n")
            if line.strip()
        ]

        return lines[:6] if len(lines) >= 6 else None

    except Exception as e:
        print("⚠️ Gemini failed, switching to fallback.")
        print(e)
        return None


def generate_script_rule_based(title, summary):
    """
    Intelligent rule-based fallback script generator.
    """
    text = f"{title} {summary}".lower()
    script = []

    script.append(f"Breaking news update: {title}.")

    if any(k in text for k in ["attack", "shoot", "terror", "blast"]):
        script.append("The incident involved a violent attack causing panic in the area.")
    elif any(k in text for k in ["fire", "explosion", "accident"]):
        script.append("A serious accident triggered an immediate emergency response.")
    elif any(k in text for k in ["technology", "ai", "launch"]):
        script.append("This development marks a significant moment in the technology sector.")
    else:
        script.append("Authorities are assessing the situation as details continue to emerge.")

    if any(k in text for k in ["killed", "dead", "injured"]):
        script.append("Officials have confirmed casualties and multiple injuries.")
    else:
        script.append("The situation has had a notable impact on the local population.")

    if any(k in text for k in ["police", "probe", "investigation"]):
        script.append("Police and security agencies have launched an investigation.")
    else:
        script.append("Emergency teams were deployed to manage the situation.")

    if any(k in text for k in ["pm", "minister", "government"]):
        script.append("Leaders and officials have issued statements regarding the incident.")
    else:
        script.append("Officials are closely monitoring the ongoing developments.")

    script.append("More updates are expected as the situation continues to unfold.")

    return script


def generate_video_script(title, summary):
    """
    FINAL HYBRID SCRIPT PIPELINE
    """
    print("Generating video script (Hybrid: Gemini + Rule-based)...")

    script = None

    if USE_LLM_FOR_SCRIPT:
        script = generate_script_with_llm(title, summary)

    if not script:
        script = generate_script_rule_based(title, summary)

    for i, line in enumerate(script, 1):
        print(f"Scene {i}: {line}")

    return script


"""
Hybrid Image Generation Module

- Detects scene type from text
- Generates scene-aware image prompts
- Optionally fetches images from external AI APIs
- Falls back to local image generation for reliability
"""

# Toggle external image generation (Banana / Stable Diffusion / etc.)

def detect_scene_type(scene_text: str) -> str:
    """
    Classifies a scene into a semantic category using rule-based logic.
    """
    text = scene_text.lower()

    if any(word in text for word in ["shoot", "attack", "incident", "killed"]):
        return "breaking_news"
    if any(word in text for word in ["police", "investigation", "raid"]):
        return "police"
    if any(word in text for word in ["emergency", "ambulance", "hospital"]):
        return "emergency"
    if any(word in text for word in ["leader", "minister", "condemned"]):
        return "leaders"
    return "general"


def generate_image_prompt(scene_type: str, scene_text: str) -> str:
    """
    Generates a descriptive image prompt based on scene type and text.
    """
    base_prompts = {
        "breaking_news": "breaking news scene, urgent atmosphere, city background",
        "police": "police investigation scene, flashing blue lights, crime scene tape",
        "emergency": "emergency response scene, ambulance, rescue team",
        "leaders": "official press conference, government building",
        "general": "professional news report background"
    }

    return f"{base_prompts.get(scene_type)}. {scene_text}"

USE_EXTERNAL_IMAGES = False  # Gemini image generation is experimental; local PIL used for reliability
def fetch_external_image(prompt: str, idx: int, image_dir: str):
    """
    Generate scene image using Gemini image model.
    Returns image path if successful, else None.
    """
    try:
        image_prompt = f"""
Create a realistic news-style image.
Style: professional news broadcast.
Scene description: {prompt}
No text, no logos, no watermark.
High realism, studio lighting.
"""

        response = _get_client().models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=image_prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
        )

        if not response or not response.candidates:
            return None

        # Find image part
        image_bytes = None
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_bytes = base64.b64decode(part.inline_data.data)
                break

        if image_bytes is None:
            raise ValueError("No image data found in Gemini response")

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        path = os.path.join(image_dir, f"scene_{idx}_ai.png")
        img.save(path)

        print(f"✅ Gemini image generated: {path}")
        return path

    except Exception as e:
        print("⚠️ Gemini image generation failed, falling back to local image")
        print(e)
        return None



def generate_local_image(scene_text: str, idx: int, image_dir: str) -> str:
    width, height = 1280, 720
    bg_color = (20, 20, 20)
    text_color = (255, 255, 255)

    # Base image
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # -------- TEXT (LEFT SIDE) --------
    wrapped_text = textwrap.fill(scene_text, width=35)

    try:
        font = ImageFont.truetype("arial.ttf", 44)
    except:
        font = ImageFont.load_default()

    draw.multiline_text(
        (60, height // 3),
        wrapped_text,
        fill=text_color,
        font=font,
        align="left"
    )

    # -------- ANCHOR (RIGHT SIDE) --------
    anchor_candidates = [
        os.path.join(ASSETS_DIR, "anchor_image.png"),
        os.path.join(ASSETS_DIR, "lady.png"),
    ]
    anchor_path = next((path for path in anchor_candidates if os.path.exists(path)), None)

    if anchor_path:
        anchor = Image.open(anchor_path).convert("RGBA")

        # Resize anchor (keep proportions)
        anchor = anchor.resize((350, 500))

        anchor_x = width - 400
        anchor_y = height - 520

        img.paste(anchor, (anchor_x, anchor_y), anchor)
    else:
        print("⚠️ Anchor image not found, skipping anchor overlay")

    # Save image
    path = os.path.join(image_dir, f"scene_{idx}.png")
    img.save(path)

    return path



def generate_images_hybrid(script_lines, image_dir: str):
    """
    Main hybrid image generation pipeline.
    """
    print("Generating images (Hybrid: Local + Optional API)...")

    image_paths = []

    for idx, scene in enumerate(script_lines, 1):
        scene_type = detect_scene_type(scene)
        prompt = generate_image_prompt(scene_type, scene)

        print(f"[Scene {idx}] Type: {scene_type}")
        print(f"[Scene {idx}] Prompt: {prompt}")

        image_path = None

        if USE_EXTERNAL_IMAGES:
            image_path = fetch_external_image(prompt, idx, image_dir)

        if image_path is None:
            image_path = generate_local_image(scene, idx, image_dir)

        image_paths.append(image_path)

    return image_paths


def generate_video(image_paths):
    print("Generating video (final stable version)...")

    clips = []
    duration_per_scene = 6  # seconds

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for path in image_paths:
        if not os.path.exists(path):
            continue

        clip = ImageClip(path).with_duration(duration_per_scene)
        clips.append(clip)

    if not clips:
        raise Exception("No valid image clips to create video")

    final_video = concatenate_videoclips(clips, method="compose")

    n = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, f"news_video{n}.mp4")):
        n += 1
    output_path = os.path.join(OUTPUT_DIR, f"news_video{n}.mp4")
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
        audio=False
    )

    print(f"✅ Video saved at: {output_path}")




"""
MAIN EXECUTION FLOW:
1. Fetch trending news
2. Generate AI-based script (with fallback)
3. Generate scene-aware images
4. Compile final news video
"""
if __name__ == "__main__":
    title, summary = fetch_trending_news()
    script_lines = generate_video_script(title, summary)
    with tempfile.TemporaryDirectory(dir=TASK_DIR) as temp_dir:
        image_paths = generate_images_hybrid(script_lines, temp_dir)
        generate_video(image_paths)





