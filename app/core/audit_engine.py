import re
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from core.prompt_generator import flatten_prompt_map


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GEOAuditBot/1.0)"
}


def fetch_page(url: str) -> Dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return {"ok": True, "html": response.text}
    except Exception as e:
        return {"ok": False, "error": str(e), "html": ""}


def parse_html(html: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else "Untitled Page"

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    body = soup.body if soup.body else soup
    headings = body.find_all(re.compile("^h[1-3]$"))
    paragraphs = body.find_all(["p", "li"])

    sections = []
    current_section = {"title": "Introduction", "content": []}

    def flush_section():
        if current_section["content"]:
            sections.append({
                "title": current_section["title"],
                "content": "\n".join(current_section["content"]).strip()
            })

    if headings:
        all_nodes = body.find_all(["h1", "h2", "h3", "p", "li"])
        current_section = {"title": "Introduction", "content": []}

        for node in all_nodes:
            if node.name in ["h1", "h2", "h3"]:
                flush_section()
                current_section = {
                    "title": node.get_text(" ", strip=True),
                    "content": []
                }
            elif node.name in ["p", "li"]:
                text = node.get_text(" ", strip=True)
                if text:
                    current_section["content"].append(text)

        flush_section()
    else:
        text_blocks = []
        for p in paragraphs[:20]:
            text = p.get_text(" ", strip=True)
            if text:
                text_blocks.append(text)
        sections = [{"title": "Page Content", "content": "\n".join(text_blocks)}]

    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_description = meta_tag["content"].strip()

    return {
        "title": title,
        "meta_description": meta_description,
        "sections": sections,
    }


def normalise_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def prompt_overlap_score(section_text: str, prompts: List[str]) -> float:
    text = normalise_text(section_text)
    total = 0
    hits = 0

    for prompt in prompts:
        prompt_terms = [t for t in normalise_text(prompt).split() if len(t) > 2]
        if not prompt_terms:
            continue
        total += len(prompt_terms)
        hits += sum(1 for term in prompt_terms if term in text)

    if total == 0:
        return 0.0
    return round((hits / total) * 100, 1)


def evaluate_section(section: Dict, all_prompts: List[str]) -> Dict:
    title = section["title"]
    content = section["content"]
    combined = f"{title}\n{content}".strip()

    issues = []
    support_prompts = []

    if len(content.split()) < 40:
        issues.append("Section is thin and may not provide enough answer depth.")

    lines = [ln.strip() for ln in content.split("\n") if ln.strip()]
    first_line = lines[0] if lines else ""
    if first_line and len(first_line.split()) > 28:
        issues.append("Opening sentence is not answer-first and may be too long.")

    if not re.search(r"\b(what|why|how|best|for|who|when)\b", combined.lower()):
        issues.append("Section lacks explicit question-answer phrasing.")

    overlap = prompt_overlap_score(combined, all_prompts)

    for prompt in all_prompts:
        terms = [t for t in normalise_text(prompt).split() if len(t) > 3]
        text = normalise_text(combined)
        if terms and sum(1 for term in terms if term in text) >= max(1, min(2, len(terms))):
            support_prompts.append(prompt)

    if overlap < 18:
        issues.append("Low alignment with target prompts.")
    if not title or title.lower() in ["introduction", "page content"]:
        issues.append("Section heading is weak or non-descriptive.")

    score = 100
    score -= min(len(issues) * 15, 60)
    score = max(score - int(max(0, 30 - overlap) * 0.7), 0)

    return {
        "title": title,
        "content": content,
        "score": score,
        "overlap_score": overlap,
        "supported_prompts": support_prompts[:6],
        "issues": issues,
    }


def run_geo_audit(url: str, prompt_map: Dict[str, List[str]]) -> Dict:
    fetched = fetch_page(url)
    if not fetched["ok"]:
        return {
            "ok": False,
            "error": fetched["error"]
        }

    parsed = parse_html(fetched["html"])
    all_prompts = flatten_prompt_map(prompt_map)

    evaluated_sections = []
    top_issues = []

    for section in parsed["sections"]:
        result = evaluate_section(section, all_prompts)
        evaluated_sections.append(result)
        top_issues.extend(result["issues"])

    overall_score = 0
    if evaluated_sections:
        overall_score = round(sum(s["score"] for s in evaluated_sections) / len(evaluated_sections), 1)

    unique_top_issues = []
    seen = set()
    for issue in top_issues:
        if issue not in seen:
            seen.add(issue)
            unique_top_issues.append(issue)

    return {
        "ok": True,
        "page_title": parsed["title"],
        "meta_description": parsed["meta_description"],
        "overall_score": overall_score,
        "sections": evaluated_sections,
        "top_issues": unique_top_issues[:8],
    }
