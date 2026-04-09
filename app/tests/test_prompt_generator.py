from core.prompt_generator import generate_prompt_map


def test_generate_prompt_map_returns_expected_keys():
    intake = {
        "business_name": "Example Co",
        "industry": "Skincare",
        "niche": "Sensitive skin moisturiser",
        "target_audience": "People with eczema-prone skin",
        "products_services": "Fragrance-free skincare",
        "differentiators": "Dermatologist-informed and lightweight",
        "recommendation_goals": "Be recommended for sensitive skin moisturisers",
    }

    result = generate_prompt_map(intake)

    assert "recommendation_prompts" in result
    assert "problem_solution_prompts" in result
    assert "comparison_prompts" in result
    assert "buyer_journey_prompts" in result

    assert isinstance(result["recommendation_prompts"], list)
    assert len(result["recommendation_prompts"]) > 0
