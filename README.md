# Gen AI Assignment

Submission for the Generative AI Internship Assignment.  
Three tasks built using **Google Gemini API (gemini-2.5-flash)** and Python, each demonstrating a different real-world AI automation use case.

## Assignment Tasks

| Task       | Title                                         | Output                  |
| ---------- | --------------------------------------------- | ----------------------- |
| **Task 1** | AI-Based Automated News Video Generation      | `news_video{N}.mp4`     |
| **Task 2** | SEO Blog Post Creation Tool                   | `blog_post_{N}.md`      |
| **Task 3** | High-Level to Low-Level Architecture Pipeline | `technical_spec_{N}.md` |

---

## Task 1: AI-Based Automated News Video Generation

**Objective**: Automatically generate a news broadcast video from live news data using AI.

**How It Works**:

1. Fetches trending news from Google News RSS feed
2. Sends news to Gemini to generate a 6-scene broadcast script
3. Creates scene images with text overlay and anchor person using PIL
4. Compiles images into a silent MP4 video using moviepy

**Libraries Used**:

- `feedparser` — parse Google News RSS
- `beautifulsoup4` — clean HTML from feed summaries
- `google-genai` — Gemini script generation
- `Pillow` — generate and composite scene images
- `moviepy` — compile images into video

**Run**:

```bash
python "GEN_AI_Tasks/Task 1/code/main.py"
```

**Output**: `GEN_AI_Tasks/Task 1/outputs/news_video{N}.mp4`

---

## Task 2: SEO Blog Post Creation Tool

**Objective**: Automatically generate an SEO-optimized blog post for a trending product.

**How It Works**:

1. Fetches a random product from [FakeStore API](https://fakestoreapi.com/products)
2. Sends product name to Gemini to generate 4 SEO keywords
3. Sends product + keywords to Gemini to write a 150-200 word blog post
4. Saves the output as a formatted markdown file

**Libraries Used**:

- `requests` — HTTP calls to FakeStore API
- `google-genai` — keyword and blog generation via Gemini
- `beautifulsoup4` — HTML parsing utility

**Run**:

```bash
python "GEN_AI_Tasks/Task 2/code/main.py"
```

**Output**: `GEN_AI_Tasks/Task 2/outputs/blog_post_{N}.md`

---

## Task 3: High-Level to Low-Level Architecture Pipeline

**Objective**: Convert a plain-English business requirement into a complete low-level technical specification using AI.

**How It Works**:

1. Takes a business requirement (default: food delivery app)
2. Calls Gemini to generate system modules
3. Calls Gemini to design database schema based on modules
4. Calls Gemini to define REST API endpoints
5. Calls Gemini to write pseudocode for core workflows
6. Compiles everything into a structured markdown specification

**Libraries Used**:

- `google-genai` — all AI generation steps via Gemini

**Customize**:
Edit `BUSINESS_REQUIREMENT` in `GEN_AI_Tasks/Task 3/code/main.py` to generate a spec for any system.

**Run**:

```bash
python "GEN_AI_Tasks/Task 3/code/main.py"
```

**Output**: `GEN_AI_Tasks/Task 3/outputs/technical_spec_{N}.md`

---

## Setup

### Requirements

- Python 3.13+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey) — free, no billing required)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set API Key

```powershell
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key-here"
```

```bash
# macOS/Linux
export GEMINI_API_KEY="your-api-key-here"
```

### Run All Tasks

```bash
python "GEN_AI_Tasks/Task 1/code/main.py"
python "GEN_AI_Tasks/Task 2/code/main.py"
python "GEN_AI_Tasks/Task 3/code/main.py"
```

---

## Project Structure

```
Gen-AI-Assignment/
├── GEN_AI_Tasks/
│   ├── Task 1/
│   │   ├── code/main.py
│   │   ├── outputs/
│   │   │   ├── assets/anchor_image.png
│   │   │   └── news_video1.mp4
│   │   └── REPORT.md
│   ├── Task 2/
│   │   ├── code/
│   │   │   ├── main.py
│   │   │   ├── scraper.py
│   │   │   ├── seo_keywords.py
│   │   │   └── blog_generator.py
│   │   ├── outputs/blog_post_1.md
│   │   └── REPORT.md
│   └── Task 3/
│       ├── code/
│       │   ├── main.py
│       │   ├── analyzer.py
│       │   ├── module_generator.py
│       │   ├── schema_generator.py
│       │   ├── api_generator.py
│       │   └── pseudocode_gen.py
│       ├── outputs/technical_spec_1.md
│       └── REPORT.md
├── requirements.txt
├── COMPREHENSIVE_DOCUMENTATION.md
└── README.md
```

---

## Notes

- All outputs are auto-numbered (`_1`, `_2`, ...) so re-running never overwrites previous results.
- All tasks have fallback logic — if Gemini quota is exceeded (20 req/day free tier), the script completes using hardcoded templates.
- Each task has a `REPORT.md` with a detailed explanation of the code flow, functions, and design decisions.
- See `COMPREHENSIVE_DOCUMENTATION.md` for a full technical deep-dive across all three tasks.
