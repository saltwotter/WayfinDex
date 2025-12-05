"""
Agent factory for creating and managing AI agents from multiple providers.

This module provides the AgentFactory class which creates AI agents based on
configuration settings, supporting OpenAI, Google Gemini, Anthropic, OpenRouter,
and Perplexity providers.
"""

import os
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from helpers.config import WayfinDexConfigLoader
from helpers.type_models import PlaceSearchAgent, create_place_note_model
from helpers.data import load_categories


def load_prompt(prompt_name: str) -> str:
    """
    Load a system prompt from the prompts directory.
    
    Args:
        prompt_name: Name of the prompt file (without .txt extension)
        
    Returns:
        Content of the prompt file as a string
    """
    prompt_path = Path(__file__).parent.parent / "prompts" / f"{prompt_name}.txt"
    with open(prompt_path, "r") as f:
        return f.read().strip()


class AgentFactory:
    """
    Factory for creating and managing AI agents from multiple providers.

    This factory initializes AI agents based on the active environment configuration,
    handling API key retrieval, provider setup, and agent creation for OpenAI, Gemini,
    Anthropic, OpenRouter, and Perplexity.

    Attributes:
        config: The active WayfinDex configuration
        agents: List of initialized PlaceSearchAgent instances
        categories: Available place categories for validation
    """

    def __init__(self, config_loader: WayfinDexConfigLoader):
        """
        Initialize the AgentFactory with configuration.

        Args:
            config_loader: Configured WayfinDexConfigLoader instance
        """
        self.config = config_loader.config
        self.agents: list[PlaceSearchAgent] = list()
        self.categories = load_categories()

    def load_agents(self) -> list[PlaceSearchAgent]:
        """
        Load and initialize all agents for active providers.

        Checks which providers are listed in the active_agents configuration
        and creates agent instances for each configured model.

        Returns:
            List of initialized PlaceSearchAgent instances
        """
        agents: list[PlaceSearchAgent] = []
        if "gemini" in self.config.active_agents:
            agents.extend(self.create_gemini_agents())
        if "openai" in self.config.active_agents:
            agents.extend(self.create_openai_agents())
        if "anthropic" in self.config.active_agents:
            agents.extend(self.create_anthropic_agents())
        if "openrouter" in self.config.active_agents:
            agents.extend(self.create_openrouter_agents())
        if "perplexity" in self.config.active_agents:
            agents.extend(self.create_perplexity_agents())
        self.agents = agents
        return agents

    def create_gemini_agents(self) -> list[PlaceSearchAgent]:
        """
        Create Google Gemini agents.

        Reads the Gemini API key from the configured environment variable
        and creates an agent for each model listed in gemini_model_names.

        Returns:
            List of Gemini PlaceSearchAgent instances (empty if not configured)
        """
        if not self.config.gemini_api_key_env_var or not self.config.gemini_model_names:
            return []
        api_key = os.getenv(self.config.gemini_api_key_env_var)
        if not api_key:
            return []
        provider = GoogleProvider(api_key=api_key)
        agents = []
        system_prompt = load_prompt("place_search")
        for model_name in self.config.gemini_model_names:
            model = GoogleModel(model_name, provider=provider)
            agent_name = f"gemini-{model_name}"
            agent = Agent(
                model=model,
                system_prompt=system_prompt,
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_openai_agents(self) -> list[PlaceSearchAgent]:
        """
        Create OpenAI agents.

        Reads the OpenAI API key from the configured environment variable
        and creates an agent for each model listed in openai_model_names.

        Returns:
            List of OpenAI PlaceSearchAgent instances (empty if not configured)
        """
        if not self.config.openai_api_key_env_var or not self.config.openai_model_names:
            return []
        api_key = os.getenv(self.config.openai_api_key_env_var)
        if not api_key:
            return []
        provider = OpenAIProvider(api_key=api_key)
        agents = []
        system_prompt = load_prompt("place_search")
        for model_name in self.config.openai_model_names:
            model = OpenAIChatModel(model_name, provider=provider)
            agent_name = f"openai-{model_name}"
            agent = Agent(
                model=model,
                system_prompt=system_prompt,
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_anthropic_agents(self) -> list[PlaceSearchAgent]:
        """
        Create Anthropic Claude agents.

        Reads the Anthropic API key from the configured environment variable
        and creates an agent for each model listed in anthropic_model_names.

        Returns:
            List of Anthropic PlaceSearchAgent instances (empty if not configured)
        """
        if (
            not self.config.anthropic_api_key_env_var
            or not self.config.anthropic_model_names
        ):
            return []
        api_key = os.getenv(self.config.anthropic_api_key_env_var)
        if not api_key:
            return []
        provider = AnthropicProvider(api_key=api_key)
        agents = []
        system_prompt = load_prompt("place_search")
        for model_name in self.config.anthropic_model_names:
            model = AnthropicModel(model_name, provider=provider)
            agent_name = f"anthropic-{model_name}"
            agent = Agent(
                model=model,
                system_prompt=system_prompt,
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_openrouter_agents(self) -> list[PlaceSearchAgent]:
        """
        Create OpenRouter agents.

        Reads the OpenRouter API key from the configured environment variable
        and creates an agent for each model listed in openrouter_model_names.
        OpenRouter provides access to multiple AI models through a single API.

        Returns:
            List of OpenRouter PlaceSearchAgent instances (empty if not configured)
        """
        if (
            not self.config.openrouter_api_key_env_var
            or not self.config.openrouter_model_names
        ):
            return []
        api_key = os.getenv(self.config.openrouter_api_key_env_var)
        if not api_key:
            return []
        provider = OpenRouterProvider(api_key=api_key)
        agents = []
        system_prompt = load_prompt("place_search")
        for model_name in self.config.openrouter_model_names:
            model = OpenRouterModel(model_name, provider=provider)
            agent_name = f"openrouter-{model_name}"
            agent = Agent(
                model=model,
                system_prompt=system_prompt,
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_perplexity_agents(self) -> list[PlaceSearchAgent]:
        """
        Create Perplexity agents.

        Reads the Perplexity API key from the configured environment variable
        and creates an agent for each model listed in perplexity_model_names.
        Perplexity uses an OpenAI-compatible API interface.

        Returns:
            List of Perplexity PlaceSearchAgent instances (empty if not configured)
        """
        if (
            not self.config.perplexity_api_key_env_var
            or not self.config.perplexity_model_names
        ):
            return []
        api_key = os.getenv(self.config.perplexity_api_key_env_var)
        if not api_key:
            return []
        provider = OpenAIProvider(base_url="https://api.perplexity.ai", api_key=api_key)
        agents = []
        system_prompt = load_prompt("place_search")
        for model_name in self.config.perplexity_model_names:
            model = OpenAIChatModel(model_name, provider=provider)
            agent_name = f"perplexity-{model_name}"
            agent = Agent(
                model=model,
                system_prompt=system_prompt,
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents
