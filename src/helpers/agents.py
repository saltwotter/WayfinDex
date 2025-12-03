import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from config import WayfinDexConfigLoader
from models import PlaceSearchAgent, create_place_note_model
from data import load_categories


class AgentFactory:
    """Factory to create AI agents based on configuration."""

    def __init__(self, config_loader: WayfinDexConfigLoader):
        self.config = config_loader.config
        self.agents: list[PlaceSearchAgent] = list()
        self.categories = load_categories()

    def load_agents(self) -> list[PlaceSearchAgent]:
        """Load agents based on the configuration."""
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
        """Create Gemini agents."""
        if not self.config.gemini_api_key_env_var or not self.config.gemini_model_names:
            return []
        api_key = os.getenv(self.config.gemini_api_key_env_var)
        if not api_key:
            return []
        provider = GoogleProvider(api_key=api_key)
        agents = []
        for model_name in self.config.gemini_model_names:
            model = GoogleModel(model_name, provider=provider)
            agent_name = f"gemini-{model_name}"
            agent = Agent(
                model=model,
                system_prompt="""
                You are an agent that searches the web for information about a place based on
                a user query. Your task is to find the most relevant information about the
                place and provide it in a concise manner. Return as many results as you deem 
                appropriate for the place, but return at least one result, and no duplicates.""",
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_openai_agents(self) -> list[PlaceSearchAgent]:
        """Create OpenAI agents."""
        if not self.config.openai_api_key_env_var or not self.config.openai_model_names:
            return []
        api_key = os.getenv(self.config.openai_api_key_env_var)
        if not api_key:
            return []
        provider = OpenAIProvider(api_key=api_key)
        agents = []
        for model_name in self.config.openai_model_names:
            model = OpenAIChatModel(model_name, provider=provider)
            agent_name = f"openai-{model_name}"
            agent = Agent(
                model=model,
                system_prompt="""
                You are an agent that searches the web for information about a place based on
                a user query. Your task is to find the most relevant information about the
                place and provide it in a concise manner. Return as many results as you deem 
                appropriate for the place, but return at least one result, and no duplicates.""",
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_anthropic_agents(self) -> list[PlaceSearchAgent]:
        """Create Anthropic agents."""
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
        for model_name in self.config.anthropic_model_names:
            model = AnthropicModel(model_name, provider=provider)
            agent_name = f"anthropic-{model_name}"
            agent = Agent(
                model=model,
                system_prompt="""
                You are an agent that searches the web for information about a place based on
                a user query. Your task is to find the most relevant information about the
                place and provide it in a concise manner. Return as many results as you deem 
                appropriate for the place, but return at least one result, and no duplicates.""",
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_openrouter_agents(self) -> list[PlaceSearchAgent]:
        """Create OpenRouter agents."""
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
        for model_name in self.config.openrouter_model_names:
            model = OpenRouterModel(model_name, provider=provider)
            agent_name = f"openrouter-{model_name}"
            agent = Agent(
                model=model,
                system_prompt="""
                You are an agent that searches the web for information about a place based on
                a user query. Your task is to find the most relevant information about the
                place and provide it in a concise manner. Return as many results as you deem 
                appropriate for the place, but return at least one result, and no duplicates.""",
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents

    def create_perplexity_agents(self) -> list[PlaceSearchAgent]:
        """Create Perplexity agents."""
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
        for model_name in self.config.perplexity_model_names:
            model = OpenAIChatModel(model_name, provider=provider)
            agent_name = f"perplexity-{model_name}"
            agent = Agent(
                model=model,
                system_prompt="""
                You are an agent that searches the web for information about a place based on
                a user query. Your task is to find the most relevant information about the
                place and provide it in a concise manner. Return as many results as you deem 
                appropriate for the place, but return at least one result, and no duplicates.""",
                name=agent_name,
                output_type=create_place_note_model(categories=self.categories),
            )
            agents.append(PlaceSearchAgent(name=agent_name, agent=agent))
        return agents
