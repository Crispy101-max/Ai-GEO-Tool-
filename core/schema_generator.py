from typing import Dict, List
import json


def build_faq_items(prompt_map: Dict[str, List[str]]) -> Listfaq_items = []
    all_prompts = []
    for vals in prompt_map.values():
        all_prompts.extend(vals)

    for prompt in all_prompts[:6]:
        faq_items.append({
            "@type": "Question",
            "name": prompt,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"This page should clearly answer the question: {prompt}."
            }
        })
    return faq_items


def generate_schema(intake: Dict, prompt_map: Dict, optimised_output: Dict) -> Dict:
    website_url = intake.get("website_url", "")
    business_name = intake.get("business_name", "")
    industry = intake.get("industry", "")
    products = intake.get("products_services", "")
    differentiators = intake.get("differentiators", "")
    page_title = optimised_output.get("page_title", business_name or "Web Page")

    graph = []

    graph.append({
        "@type": "Organization",
        "@id": f"{website_url.rstrip('/')}/#organization" if website_url else "#organization",
        "name": business_name,
        "url": website_url,
        "description": f"{business_name} operates in {industry}. {differentiators}".strip(),
    })

    graph.append({
        "@type": "WebPage",
        "@id": f"{website_url.rstrip('/')}/#webpage" if website_url else "#webpage",
        "url": website_url,
        "name": page_title,
        "about": products or intake.get("niche", ""),
        "isPartOf": {
            "@id": f"{website_url.rstrip('/')}/#website" if website_url else "#website"
        },
    })

    if products:
        graph.append({
            "@type": "Service",
            "name": products,
            "provider": {
                "@id": f"{website_url.rstrip('/')}/#organization" if website_url else "#organization"
            },
            "areaServed": "Online",
            "description": differentiators or f"{business_name} provides {products}.",
        })

    graph.append({
        "@type": "FAQPage",
        "mainEntity": build_faq_items(prompt_map)
    })

    schema = {
        "@context": "https://schema.org",
        "@graph": graph
    }

    return {
        "dict": schema,
        "json": json.dumps(schema, indent=2)
    }
