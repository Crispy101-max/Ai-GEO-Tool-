from typing import Dict, List
from core.llm import llm_text


def build_rewrite_prompt(section: Dict, intake: Dict, prompt_map: Dict[str, List[str]]) -> str:
    all_prompts = []
    for values in prompt_map.values():
        all_prompts.extend(values)

    target_prompts = section.get("supported_prompts") or all_prompts[:5]

    return f"""
Business: {intake.get('business_name', '')}
Industry: {intake.get('industry', '')}
Niche: {intake.get('niche', '')}
Audience: {intake.get('target_audience', '')}
Products/Services: {intake.get('products_services', '')}
Differentiators: {intake.get('differentiators', '')}

Current section title:
{section.get('title', '')}

Current section content:
{section.get('content', '')}

Known issues:
{section.get('issues', [])}

Target prompts:
{target_prompts}

Rewrite this section to:
- be answer-first
- improve prompt alignment
- improve clarity and structure
- sound human and commercial, not robotic
- include a strong heading
- use short paragraphs and bullet points where useful

Return only the rewritten section in markdown.
"""


def heuristic_rewrite(section: Dict, intake: Dict) -> str:
    title = section.get("title", "Improved Section")
    content = section.get("content", "")
    service = intake.get("products_services", "") or intake.get("niche", "") or intake.get("industry", "service")
    audience = intake.get("target_audience", "the right audience")
    differentiators = intake.get("differentiators", "")

    first_sentence = f"{service} should clearly explain who it is for, what problem it solves, and why it is different."

    bullets = [
        f"Who it is for: {audience}",
        f"What it helps with: clearer understanding of the offer and outcomes",
        f"Why choose this option: {differentiators or 'clear positioning, useful guidance, and stronger trust signals'}",
    ]

    rewritten = f"""## {title}

{first_sentence}

This section should quickly help visitors understand the value of the offer and whether it fits their needs. It should also make it easier for AI systems to identify the purpose of the page and match it to recommendation-style prompts.

### Key points
- {bullets[0]}
- {bullets[1]}
- {bullets[2]}

### Improved explanatory copy
{content[:350].strip()}{"..." if len(content) > 350 else ""}
"""

    return rewritten.strip()


def optimise_content(audit_result: Dict, intake: Dict, prompt_map: Dict[str, List[str]]) -> Dict:
    optimised_sections = []

    for section in audit_result.get("sections", []):
        system_prompt = (
            "You are a GEO content optimiser. Rewrite sections for AI recommendation visibility, "
            "clear UX, semantic clarity, and answer-first structure."
        )
        user_prompt = build_rewrite_prompt(section, intake, prompt_map)
        rewritten = llm_text(system_prompt, user_prompt)

        if not rewritten:
            rewritten = heuristic_rewrite(section, intake)

        optimised_sections.append({
            "title": section["title"],
            "original": section["content"],
            "rewritten": rewritten,
            "issues": section.get("issues", []),
            "supported_prompts": section.get("supported_prompts", []),
            "score_before": section.get("score", 0),
        })

    return {
        "page_title": audit_result.get("page_title", "Untitled"),
        "overall_score_before": audit_result.get("overall_score", 0),
        "sections": optimised_sections,
    }
