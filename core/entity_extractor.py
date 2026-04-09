import re
from typing import Dict, List


def keyword_terms(text: str) -> Listtokens = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text.lower())
    stop = {
        "the", "and", "for", "with", "that", "this", "your", "from", "have",
        "will", "into", "what", "best", "how", "when", "who", "why", "their",
        "about", "they", "them", "page", "section", "service", "services"
    }
    return [t for t in tokens if t not in stop]


def extract_entities(intake: Dict, prompt_map: Dict, audit_result: Dict) -> Dict:
    business_name = intake.get("business_name", "")
    industry = intake.get("industry", "")
    niche = intake.get("niche", "")
    audience = intake.get("target_audience", "")
    products = intake.get("products_services", "")
    differentiators = intake.get("differentiators", "")

    prompt_terms = []
    for values in prompt_map.values():
        for value in values:
            prompt_terms.extend(keyword_terms(value))

    content_terms = []
    for section in audit_result.get("sections", []):
        content_terms.extend(keyword_terms(section.get("content", "")))
        content_terms.extend(keyword_terms(section.get("title", "")))

    core_entities = [x for x in [business_name, industry, niche, audience, products] if x]
    supporting_entities = sorted(set(prompt_terms))[:20]

    missing_entities = []
    for term in sorted(set(prompt_terms)):
        if term not in content_terms:
            missing_entities.append(term)

    relationships = [
        {"source": business_name or "Business", "relationship": "operates_in", "target": industry or "industry"},
        {"source": business_name or "Business", "relationship": "serves", "target": audience or "target audience"},
        {"source": business_name or "Business", "relationship": "offers", "target": products or niche or "service"},
    ]

    if differentiators:
        relationships.append({
            "source": business_name or "Business",
            "relationship": "differentiated_by",
            "target": differentiators
        })

    return {
        "core_entities": core_entities,
        "supporting_entities": supporting_entities,
        "missing_entities": missing_entities[:20],
        "relationships": relationships,
    }
