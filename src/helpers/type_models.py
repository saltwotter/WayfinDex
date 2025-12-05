"""
Type models and data structures for WayfinDex.

This module defines Pydantic models for configuration, agents, and place data.
It includes a factory function for dynamically creating PlaceNote models with
category validation based on available categories.
"""

from typing import Any, Literal

from pydantic import BaseModel, Field, create_model


### Technical Models ###


class AgentEnvironment(BaseModel):
    """Represents a named environment with a list of configured agents."""

    name: str
    agents: list[str]


class WayfinDexConfig(BaseModel):
    """
    Main configuration model for WayfinDex.

    Defines environments, active agents, and provider-specific settings
    including API key environment variable names and available model names.
    """

    environments: list[AgentEnvironment] = Field(
        ...,
        description="A list of environments, each containing a name and list of agents (format: provider_modelname).",
    )
    active_agents: list[str] = Field(
        default_factory=list,
        description="The list of active agents to be used (populated from environment selection).",
    )
    gemini_api_key_env_var: str | None = Field(
        None,
        description="The environment variable name that holds the Google API key.",
    )
    gemini_model_names: list[str] | None = Field(
        None,
        description="A list of Gemini model names to be used.",
    )
    openai_api_key_env_var: str | None = Field(
        None,
        description="The environment variable name that holds the OpenAI API key.",
    )
    openai_model_names: list[str] | None = Field(
        None,
        description="A list of OpenAI model names to be used.",
    )
    perplexity_api_key_env_var: str | None = Field(
        None,
        description="The environment variable name that holds the Perplexity API key.",
    )
    perplexity_model_names: list[str] | None = Field(
        None,
        description="A list of Perplexity model names to be used.",
    )
    openrouter_api_key_env_var: str | None = Field(
        None,
        description="The environment variable name that holds the OpenRouter API key.",
    )
    openrouter_model_names: list[str] | None = Field(
        None,
        description="A list of OpenRouter model names to be used.",
    )
    anthropic_api_key_env_var: str | None = Field(
        None,
        description="The environment variable name that holds the Anthropic API key.",
    )
    anthropic_model_names: list[str] | None = Field(
        None,
        description="A list of Anthropic model names to be used.",
    )


class PlaceSearchAgent(BaseModel):
    """Wrapper for a Pydantic AI agent with a name identifier."""

    name: str
    agent: Any


class PlaceResult(BaseModel):
    """
    Result from an AI agent's place search query.

    Attributes:
        agent_name: Name of the agent that produced this result
        query: The original search query
        output: PlaceNote data returned by the agent
        usage: Optional API usage statistics
    """

    agent_name: str
    query: str
    output: Any
    usage: Any = None


### Place Note Models ###


def create_place_note_model(categories: list[str]):
    """
    Dynamically create a PlaceNote Pydantic model with category validation.

    Creates a model with category field that accepts either:
    - A string matching one of the provided categories (as a Literal type)
    - A CategorySuggestion object with a new category and fallback

    This allows AI agents to either categorize using existing categories
    or suggest new ones when the predefined list doesn't fit.

    Args:
        categories: List of valid category strings (e.g., ['restaurant', 'cafe', 'museum'])

    Returns:
        Dynamically created PlaceNote Pydantic model class

    Example:
        >>> categories = ['restaurant', 'cafe', 'museum']
        >>> PlaceNote = create_place_note_model(categories)
        >>> note = PlaceNote(
        ...     name="Pike Place Market",
        ...     address="85 Pike St, Seattle, WA",
        ...     category="museum",  # or CategorySuggestion object
        ...     description="Historic market...",
        ...     open_hours="9 AM - 6 PM",
        ...     website="https://...",
        ...     tips=["Arrive early", "Try the donuts"]
        ... )
    """
    CategoryLiteral = (
        Literal[tuple(categories)] if len(categories) > 1 else Literal[categories[0]]
    )

    CategorySuggestion = create_model(
        "CategorySuggestion",
        suggested_new_category=(
            str,
            Field(..., description="A suggested new category for the place."),
        ),
        fallback_existing_category=(
            CategoryLiteral,
            Field(
                ...,
                description="An existing category that is the closest match for the place.",
            ),
        ),
    )

    return create_model(
        "PlaceNote",
        name=(str, Field(..., description="The name of the place.")),
        slug=(
            str,
            Field(
                ...,
                description="A URL-safe slug for the place name (lowercase, alphanumeric and hyphens only, e.g., 'pike-place-market'). Must be suitable for use in filenames.",
            ),
        ),
        address=(str, Field(..., description="The address of the place.")),
        category=(
            CategoryLiteral | CategorySuggestion,
            Field(..., description="The category of the place."),
        ),
        description=(str, Field(..., description="A brief description of the place.")),
        open_hours=(str, Field(..., description="The opening hours of the place.")),
        website=(str | None, Field(None, description="The website URL of the place.")),
        tips=(
            list[str],
            Field(
                ...,
                description="A list of 1-3 tips for visiting the place, each no more than 15 words.",
            ),
        ),
    )
