from typing import Dict, List
from core.llm import llm_json


def clean_list(items: List[str]) -> Listseen = set()
    output = []
    for item in items:
        item = item.strip()
        if item and item.lower() not in seen:
            seen.add(item.lower())
            output.append(item)
    return output


def flatten_prompt_map(prompt_map: Dict[str, List[str]]) -> Listprompts = []
    for category, values in prompt_map.items():
        prompts.extend(values)
    return clean_list(prompts)


def generate_prompt_map(intake: Dict) -> Dict[str, List[str]]:
    system_prompt = (
        "You generate AI-search target prompts for GEO optimisation. "
        "Return valid JSON with keys: recommendation_prompts, problem_solution_prompts, "
        "comparison_prompts, buyer_journey_prompts."
    )

    user_prompt = f"""
Business name: {intake.get('business_name', '')}
Industry: {intake.get('industry', '')}
Niche: {intake.get('niche', '')}
Target audience: {intake.get('target_audience', '')}
Products/services: {intake.get('products_services', '')}
Differentiators: {intake.get('differentiators', '')}
Recommendation goals: {intake.get('recommendation_goals', '')}

Generate 5-8 prompts per category.
"""

    llm_result = llm_json(system_prompt, user_prompt)
    if llm_result:
        return {
            "recommendation_prompts": clean_list(llm_result.get("recommendation_prompts", [])),
            "problem_solution_prompts": clean_list(llm_result.get("problem_solution_prompts", [])),
            "comparison_prompts": clean_list(llm_result.get("comparison_prompts", [])),
            "buyer_journey_prompts": clean_list(llm_result.get("buyer_journey_prompts", [])),
        }

    niche = intake.get("niche", "").strip()
    audience = intake.get("target_audience", "").strip()
    services = intake.get("products_services", "").strip()
    differentiators = intake.get("differentiators", "").strip()

    base_topic = niche or services or intake.get("industry", "service")

    recommendation = clean_list([
        f"best {base_topic}",
        f"best {base_topic} for {audience}" if audience else f"top {base_topic} options",
        f"recommended {base_topic}",
        f"trusted {base_topic} provider",
        f"{base_topic} experts",
        f"{base_topic} with {differentiators}" if differentiators else "",
    ])

    problem_solution = clean_list([
        f"how to solve {base_topic} problems",
        f"what helps with {base_topic}",
        f"best solution for {base_topic}",
        f"how to choose the right {base_topic}",
        f"who should use {base_topic}",
    ])

    comparison = clean_list([
        f"{base_topic} vs alternatives",
        f"best alternative to standard {base_topic}",
        f"compare {base_topic} providers",
        f"is premium {base_topic} worth it",
        f"which {base_topic} is best for {audience}" if audience else "",
    ])

    buyer_journey = clean_list([
        f"what to look for in {base_topic}",
        f"how much does {base_topic} cost",
        f"beginner guide to {base_topic}",
        f"who is {base_topic} best for",
        f"questions to ask before buying {base_topic}",
    ])

    return {
        "recommendation_prompts": recommendation,
        "problem_solution_prompts": problem_solution,
        "comparison_prompts": comparison,
        "buyer_journey_prompts": buyer_journey,
    }

