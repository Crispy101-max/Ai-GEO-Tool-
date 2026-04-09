from typing import Dict


def build_summary_markdown(intake: Dict, prompt_map: Dict, audit_result: Dict, entity_output: Dict, schema_output: Dict) -> str:
    recommendation_prompts = prompt_map.get("recommendation_prompts", [])
    problem_solution_prompts = prompt_map.get("problem_solution_prompts", [])
    comparison_prompts = prompt_map.get("comparison_prompts", [])
    buyer_journey_prompts = prompt_map.get("buyer_journey_prompts", [])

    md = f"""
# GEO Summary Report

## Business
- **Business name:** {intake.get('business_name', '')}
- **Website:** {intake.get('website_url', '')}
- **Industry:** {intake.get('industry', '')}
- **Niche:** {intake.get('niche', '')}
- **Target audience:** {intake.get('target_audience', '')}
- **Products / services:** {intake.get('products_services', '')}

## Prompt Targeting
### Recommendation prompts
{chr(10).join(f"- {p}" for p in recommendation_prompts)}

### Problem-solution prompts
{chr(10).join(f"- {p}" for p in problem_solution_prompts)}

### Comparison prompts
{chr(10).join(f"- {p}" for p in comparison_prompts)}

### Buyer-journey prompts
{chr(10).join(f"- {p}" for p in buyer_journey_prompts)}

## GEO Audit
- **Page title:** {audit_result.get('page_title', '')}
- **Overall score:** {audit_result.get('overall_score', 0)}

### Top issues
{chr(10).join(f"- {issue}" for issue in audit_result.get('top_issues', []))}

## Entities
### Core entities
{chr(10).join(f"- {e}" for e in entity_output.get('core_entities', []))}

### Missing entities
{chr(10).join(f"- {e}" for e in entity_output.get('missing_entities', []))}

## Implementation priorities
1. Improve answer-first copy in weak sections.
2. Align headings and copy with target prompts.
3. Add missing semantic entities where relevant.
4. Publish JSON-LD schema markup.
5. Re-test the page after implementation.

## Schema
```json
{schema_output.get('json', '')}
