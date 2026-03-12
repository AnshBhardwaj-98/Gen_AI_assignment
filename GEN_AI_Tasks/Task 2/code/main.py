import os
from scraper import fetch_trending_product
from seo_keywords import generate_seo_keywords
from blog_generator import generate_blog


CODE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(CODE_DIR), "outputs")

def save_blog_md(title, content, keywords):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    n = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, f"blog_post_{n}.md")):
        n += 1
    output_path = os.path.join(OUTPUT_DIR, f"blog_post_{n}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)
        f.write("\n\n---\n")
        f.write("SEO Keywords:" + ", ".join(keywords))

    return output_path


if __name__ == "__main__":
    product = fetch_trending_product()
    keywords = generate_seo_keywords(product["name"])
    blog = generate_blog(product, keywords)

    output_path = save_blog_md(product["name"], blog, keywords)
    print(f"Blog generated: {output_path}")
