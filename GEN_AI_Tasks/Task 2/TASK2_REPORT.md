# Task 2: AI Blog Post Generator - Detailed Report

## Overview

Task 2 generates SEO-optimized blog posts by fetching trending e-commerce products, extracting relevant information, generating SEO keywords, creating blog content via AI, and compiling everything into a professional markdown file.

## Workflow Steps

### Step 1: Fetch Trending Product

**File**: `code/scraper.py` → `fetch_trending_product()`

- **Source**: FakeStore API (`https://fakestoreapi.com/products`)
- **Tool**: `requests` library for HTTP calls

- **Process**:
  1. Make GET request to FakeStore API `/products` endpoint
  2. Fetch JSON response containing all available products
  3. Sort products by highest price (premium products more likely to have engagement)
  4. Select first product from sorted list
  5. Extract product details:
     - Product ID
     - Title
     - Price
     - Category
     - Description
     - Rating
     - Review count

**Output**: Dictionary with complete product information

**Error Handling**:

- If API call fails: Return hardcoded sample product (electronics item)
- Ensures workflow continues even if API is unavailable

---

### Step 2: Generate SEO Keywords

**File**: `code/seo_keywords.py` → `generate_seo_keywords(product_name)`

- **Model**: Google Gemini 2.5-flash
- **Prompt**: Instructs model to generate 4 high-ranking SEO keywords for the product:
  - Keywords must include product name variants
  - Keywords should be search engine optimized
  - Keywords must be relevant to product category
  - Format: comma-separated list

- **Process**:
  1. Extract product name from fetched product
  2. Send prompt to Gemini API with product name
  3. Parse response to extract 4 keywords
  4. Clean and format keywords

**Output**: List of 4 SEO-optimized keywords

- **Fallback**: If API fails, generates 4 keyword variants from product name:
  - "best [product]"
  - "buy [product]"
  - "top [product]"
  - "[product] review"

**Example Keywords** (for "WD 4TB Gaming Drive"):

- `best wd 4tb gaming`
- `buy wd 4tb gaming`
- `top wd 4tb gaming`
- `wd 4tb gaming review`

---

### Step 3: Generate Blog Content

**File**: `code/blog_generator.py` → `generate_blog(product, keywords)`

- **Model**: Google Gemini 2.5-flash
- **Prompt**: Instructs model to write professional blog post with:
  - 150-200 word content
  - Product features highlighted
  - SEO keywords naturally integrated
  - Engaging call-to-action
  - Professional business tone

- **Process**:
  1. Compile product details into structured prompt
  2. Include extracted SEO keywords in prompt
  3. Send to Gemini API with generation parameters
  4. Receive structured blog content
  5. Return blog text

**Output**: 150-200 word blog post article

- **Fallback**: If API fails, generates templated blog using:
  - Product title as heading
  - Product description as content
  - Keywords formatted at bottom
  - Ensures valid output structure

---

### Step 4: Compile Blog Markdown

**File**: `code/main.py` → `save_blog_md(title, content, keywords)`

- **Format**: Markdown (.md)
- **Structure**:

  ```markdown
  # Product Title

  [150-word blog content]

  ---

  SEO Keywords: keyword1, keyword2, keyword3, keyword4
  ```

- **Process**:
  1. Create output directory if not exists
  2. Determine next available filename: `blog_post_1.md`, `blog_post_2.md`, etc.
  3. Write markdown file with:
     - Product title as H1 heading
     - Blog content in body
     - Separator line (---)
     - SEO keywords in footer
  4. Return full path to generated file

**Output**: `blog_post_{N}.md` (N = auto-incrementing number)

---

### Step 5: Output Management

**Directory Structure**:

```
Task 2/
├── code/
│   ├── main.py (entry point)
│   ├── scraper.py (product fetching)
│   ├── seo_keywords.py (keyword generation)
│   ├── blog_generator.py (blog content)
│   └── requirements.txt
└── outputs/
    ├── blog_post_1.md
    ├── blog_post_2.md
    └── ...
```

**Numbering System**:

- Each run checks for existing files: `blog_post_1.md`, `blog_post_2.md`, etc.
- Automatically picks the next available number
- Prevents overwriting previous outputs

**Path Resolution**:

- Uses absolute path computed from script location: `os.path.abspath(__file__)`
- Works correctly regardless of current working directory
- Output always goes to `Task 2/outputs/` folder

---

## Key Technologies

| Component       | Technology              | Purpose                              |
| --------------- | ----------------------- | ------------------------------------ |
| Product API     | FakeStore API           | Fetch trending products              |
| HTTP Requests   | requests library        | Query API endpoints                  |
| SEO Keywords    | Google Gemini 2.5-flash | Generate search-optimized keywords   |
| Blog Content    | Google Gemini 2.5-flash | Create AI-written blog posts         |
| File Format     | Markdown (.md)          | Professional blog output             |
| File Management | Python `os` module      | Organize outputs with absolute paths |

---

## Configuration

- **Python Version**: 3.13
- **API Key**: Set via `$env:GEMINI_API_KEY` environment variable
- **API Endpoints**:
  - FakeStore: `https://fakestoreapi.com/products`
  - Gemini: via `google-genai` SDK
- **Output Path**: Computed from script location using `os.path.abspath(__file__)`

---

## Error Handling & Fallbacks

1. **Product Fetch Failure**:
   - Returns hardcoded sample product (WD 4TB Gaming Drive)
   - Allows blog generation to continue

2. **SEO Keyword Generation Failure**:
   - Falls back to 4 templated keywords from product name
   - Keywords still valid for SEO purposes

3. **Blog Content Generation Failure**:
   - Uses templated blog structure with product description
   - Integrates keywords into template
   - Produces valid output despite API failure

4. **File Write Failure**:
   - Automatically creates output directory if missing
   - Uses try-except wrapped around file operations

---

## API Quota Handling

- **Gemini Free Tier**: 20 requests per day limit
- **Fallback Strategy**: All Gemini calls wrapped in try-except
- **Behavior**: If quota exceeded, fallback functions generate valid content
- **Result**: Task still completes successfully even when API quota is hit

---

## Performance Notes

- **Total Execution Time**: ~5-15 seconds
- **Internet Required**: Yes (FakeStore API + Gemini API)
- **Disk Space**: ~2-5 KB per markdown file
- **Memory Usage**: ~50 MB (minimal)

---

## Data Flow Diagram

```
FakeStore API
      ↓
[fetch_trending_product]
      ↓
Product Dictionary
      ↙        ↘
[seo_keywords]  [blog_generator]
      ↓              ↓
Keywords ←→ Blog Content
      ↘        ↙
[save_blog_md]
      ↓
blog_post_{N}.md
```

---

## Example Run Output

```
Fetching trending product from FakeStore API...
✅ Product fetched: WD 4TB Gaming Drive | Price: $150-300
  Category: electronics
  Rating: 4.5/5 stars

Generating SEO keywords...
⚠️ Gemini failed: 429 quota exceeded
✅ Using fallback keywords:
  - best wd 4tb gaming
  - buy wd 4tb gaming
  - top wd 4tb gaming
  - wd 4tb gaming review

Generating blog content...
⚠️ Gemini failed: 429 quota exceeded
✅ Using fallback blog template

Saving blog post...
✅ Blog generated: C:\...\GEN_AI_Tasks\Task 2\outputs\blog_post_1.md
```

---

## Blog Post Example

```markdown
# WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive

The WD 4TB Gaming Drive is engineered specifically for gaming consoles,
offering lightning-fast performance and massive storage capacity. With
read/write speeds up to 150MB/s and 4TB of space, it's ideal for storing
large game libraries. The sleek black design matches most console setups,
and the USB 3.0 connection ensures minimal load times. Gamers love the
reliable performance and competitive pricing. Whether you're playing PS4,
Xbox One, or PC, this drive delivers the speed and capacity serious gamers
need for an uninterrupted experience.

---

SEO Keywords: best wd 4tb gaming, buy wd 4tb gaming, top wd 4tb gaming, wd 4tb gaming review
```
