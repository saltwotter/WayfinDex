# WayfinDex

A Pydantic AI tool to research places and create markdown notes with categorized information.

## Overview

WayfinDex uses multiple AI agents to search for and compile information about places. It supports various AI providers including OpenAI, Gemini, Anthropic, Perplexity, and OpenRouter.

## Setup

1. **Install dependencies:**

   ```bash
   uv sync
   ```

2. **Configure the application:**

   ```bash
   cp config.yaml.example config.yaml
   ```

3. **Edit `config.yaml`** with your API keys and preferred models.

4. **Set up environment variables** for your API keys:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export GEMINI_API_KEY="your-key-here"
   # etc.
   ```

## Configuration

The `config.yaml` file allows you to:

- Choose which AI providers to use
- Specify model names for each provider
- Configure environment variable names for API keys

Supported providers: `gemini`, `openai`, `perplexity`, `openrouter`, `anthropic`

## Project Status

🚧 **Early Development** - This project is still in its infancy.
