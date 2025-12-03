from typing import Any, Literal

from pydantic import BaseModel, Field, create_model


### Technical Models ###


class WayfinDexConfig(BaseModel):
    active_agents: list[
        Literal["gemini", "openai", "perplexity", "openrouter", "anthropic"]
    ] = Field(
        ...,
        description="A list of active agent names to be used by the application.",
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
    name: str
    agent: Any


class PlaceResult(BaseModel):
    agent_name: str
    query: str
    output: Any
    usage: Any = None


### Place Note Models ###


def create_place_note_model(categories: list[str]):
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
