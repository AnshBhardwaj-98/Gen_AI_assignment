# Task 1: News Video Generator - Detailed Report

## Overview

Task 1 generates an AI-powered news video by fetching trending news stories, generating a scripted narration, creating scene images with an anchor overlay, and compiling them into a silent MP4 video.

## Workflow Steps

### Step 1: Fetch Trending News

**File**: `code/main.py` → `fetch_trending_news()`

- **Source**: Google News RSS feed (`https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en`)
- **Tool**: `feedparser` library
- **Process**:
  1. Parse RSS feed to extract top news headlines
  2. Extract title and description from feed entries
  3. Collect 3-5 trending news stories
  4. Return list of news dictionaries with title and description

**Output**: List of current trending news stories

---

### Step 2: Generate AI Script

**File**: `code/main.py` → `generate_script(news_data)`

- **Model**: Google Gemini 2.5-flash (Generative AI)
- **Prompt**: Instructs the model to create a 6-scene news broadcast script with:
  - Scene descriptions for visual content
  - Anchor narration lines for each scene
  - News story integration
  - Professional broadcast tone

- **Process**:
  1. Build prompt from fetched news stories
  2. Call Gemini API with model `gemini-2.5-flash`
  3. Parse response into 6 scenes with scene descriptions and narration
  4. Extract script lines for video generation

**Output**: Array of 6 scene narratives with descriptions

- **Fallback**: If API fails, uses hardcoded 6-scene template news script

---

### Step 3: Generate Scene Images

**File**: `code/main.py` → `generate_images_hybrid(script_lines, image_dir)`

- **Tool**: Gemini API (image generation) + PIL (Pillow)

- **Process**:
  1. For each of 6 scenes:
     - Send scene description to Gemini API to generate AI image (768×432 px)
     - Download and save image to temporary directory
  2. Text overlay: Add scene narration text on top of each image using PIL
     - Font: Default system font
     - Text color: White
     - Position: Bottom 1/3 of image
  3. All images stored in passed-in temp directory

**Output**: 6 scene images with text overlay (PNG format)

- **Fallback**: If Gemini image API fails, generates synthetic placeholder images using PIL

---

### Step 4: Apply Anchor Image Overlay

**File**: `code/main.py` → `overlay_anchor_image(scene_image_path, anchor_path)`

- **Asset**: Anchor image (`Task 1/outputs/assets/anchor_image.png`)
  - Checks for `anchor_image.png` first, then `lady.png` as fallback
  - Anchor image is composited on second scene (scene with anchor introduction)

- **Process**:
  1. Load scene image (768×432 px)
  2. Load anchor image (RGBA format with transparency)
  3. Composite anchor image at top-left corner of scene
  4. Return combined image with anchor overlay

**Output**: Scene image with anchor person overlay

---

### Step 5: Compile Video

**File**: `code/main.py` → `generate_video(image_paths)`

- **Tool**: moviepy (v2.0+)
- **Settings**:
  - Codec: H.264 (`libx264`)
  - FPS: 24 frames per second
  - Resolution: 768×432 pixels
  - Audio: None (silent video)
  - Output format: MP4

- **Process**:
  1. Convert each image to video clip (2 seconds per image × 6 = 12 seconds total)
  2. Concatenate all video clips
  3. Write to MP4 file with specified codec and quality settings
  4. Use ffmpeg params for compatibility: `-pix_fmt yuv420p` (for broad playback) and `-movflags +faststart` (for web streaming)

**Output**: `news_video{N}.mp4` (N = auto-incrementing number)

---

### Step 6: Output Management

**Directory Structure**:

```
Task 1/
├── code/
│   ├── main.py (entry point)
│   └── requirements.txt
└── outputs/
    ├── assets/
    │   └── anchor_image.png (permanent anchor asset)
    ├── news_video1.mp4
    ├── news_video2.mp4
    └── ...
```

**Numbering System**:

- Each run checks for existing files: `news_video1.mp4`, `news_video2.mp4`, etc.
- Automatically picks the next available number
- Prevents overwriting previous outputs

---

## Key Technologies

| Component         | Technology              | Purpose                              |
| ----------------- | ----------------------- | ------------------------------------ |
| News Source       | Google News RSS Feed    | Fetch trending news                  |
| AI Script         | Google Gemini 2.5-flash | Generate 6-scene script              |
| Image Generation  | Gemini Image API        | Create scene visuals                 |
| Image Processing  | PIL/Pillow              | Text overlay & anchor compositing    |
| Video Compilation | moviepy                 | Combine images into MP4              |
| File Management   | Python `os` module      | Organize outputs with absolute paths |

---

## Configuration

- **Python Version**: 3.13
- **API Key**: Set via `$env:GEMINI_API_KEY` environment variable
- **Temporary Files**: Stored in system temp directory during processing
- **Output Path**: Computed from script location using `os.path.abspath(__file__)`

---

## Error Handling & Fallbacks

1. **News Fetch Failure**: Exits gracefully if RSS feed unavailable
2. **Gemini Script Generation Failure**: Uses hardcoded 6-scene news template
3. **Image Generation Failure**: Falls back to synthetic PIL-generated images
4. **Video Compilation Failure**: Raises exception (moviepy must work)
5. **Anchor Image Missing**: Checks `anchor_image.png` first, then `lady.png` as fallback

---

## Performance Notes

- **Total Execution Time**: ~2-5 minutes (depending on API response time)
- **Internet Required**: Yes (RSS feed + Gemini API)
- **Disk Space**: ~50-100 MB per video (MP4 at 768×432, 24 FPS, 12 seconds)
- **Memory Usage**: ~500 MB-1 GB (image processing + video compilation)

---

## Example Run Output

```
Fetching trending news...
✅ Found 5 news stories

Generating 6-scene script with Gemini...
✅ Script generated: 6 scenes

Generating scene images...
✅ Scene 1 image generated
✅ Scene 2 image generated
✅ Scene 3 image generated
✅ Scene 4 image generated
✅ Scene 5 image generated
✅ Scene 6 image generated

Processing images with anchor overlay...
✅ Anchor overlay applied

Compiling video...
✅ Video saved at: C:\...\GEN_AI_Tasks\Task 1\outputs\news_video1.mp4
```
