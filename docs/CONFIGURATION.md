# Configuration Guide

This guide explains all configuration options for WayfinDex in detail.

## Configuration File Structure

The `config.yaml` file uses a straightforward YAML structure to define environments and AI provider settings.

### Basic Structure

```yaml
environments:
  - name: production
    agents:
      - provider_modelname
      - provider_modelname

provider_api_key_env_var: ENV_VAR_NAME
provider_model_names:
  - model-name-1
  - model-name-2
```

## Environments

Environments let you create different agent configurations for different use cases.

### Defining Environments

```yaml
environments:
  - name: prod
    agents:
      - openai_gpt-4
      - gemini_gemini-pro

  - name: dev
    agents:
      - openai_gpt-3.5-turbo

  - name: testing
    agents:
      - anthropic_claude-3-opus-20240229
      - perplexity_pplx-7b-online
```

### Environment Properties

- **name**: Unique identifier for the agent group (used with `--agent-group` flag)
- **agents**: List of agents in format `provider_modelname`

### Agent Format

Agents are specified as `{provider}_{model_name}`:

- `openai_gpt-4` → OpenAI's GPT-4
- `gemini_gemini-pro` → Google's Gemini Pro
- `anthropic_claude-3-opus-20240229` → Anthropic's Claude 3 Opus

The provider prefix determines which API to use, while the model name must match one defined in that provider's model list.

## Supported Providers

### OpenAI

```yaml
openai_api_key_env_var: OPENAI_API_KEY
openai_model_names:
  - gpt-4
  - gpt-4-turbo-preview
  - gpt-3.5-turbo
```

**Available models**: Any OpenAI chat model
**API Key**: Get from [platform.openai.com](https://platform.openai.com)

### Google Gemini

```yaml
gemini_api_key_env_var: GEMINI_API_KEY
gemini_model_names:
  - gemini-pro
  - gemini-1.5-pro
```

**Available models**: Gemini Pro, Gemini 1.5 Pro
**API Key**: Get from [Google AI Studio](https://makersuite.google.com)

### Anthropic Claude

```yaml
anthropic_api_key_env_var: ANTHROPIC_API_KEY
anthropic_model_names:
  - claude-3-opus-20240229
  - claude-3-sonnet-20240229
  - claude-3-haiku-20240307
```

**Available models**: Claude 3 family (Opus, Sonnet, Haiku)
**API Key**: Get from [console.anthropic.com](https://console.anthropic.com)

### Perplexity

```yaml
perplexity_api_key_env_var: PERPLEXITY_API_KEY
perplexity_model_names:
  - pplx-7b-online
  - pplx-70b-online
```

**Available models**: Perplexity's online models
**API Key**: Get from [perplexity.ai](https://www.perplexity.ai)

### OpenRouter

```yaml
openrouter_api_key_env_var: OPENROUTER_API_KEY
openrouter_model_names:
  - anthropic/claude-2
  - openai/gpt-4
  - google/palm-2
```

**Available models**: Any model available on OpenRouter
**API Key**: Get from [openrouter.ai](https://openrouter.ai)

## Environment Variables

WayfinDex reads API keys from environment variables. The variable names are defined in your config file.

### Setting Environment Variables

**Option 1: Use .env file (recommended)**

Create a `.env` file in the repository root:

```bash
cp .env.example .env
```

Edit `.env` with your actual keys:

```bash
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
ANTHROPIC_API_KEY=sk-ant-...
```

The `.env` file is automatically loaded when you run WayfinDex and is ignored by git.

**Option 2: Export as shell variables**

**macOS/Linux:**

```bash
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AI..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Persistent Setup (add to `~/.zshrc` or `~/.bashrc`):**

```bash
# WayfinDex API Keys
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AI..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Custom Environment Variable Names

You can use any environment variable name:

```yaml
# Use your own naming convention
openai_api_key_env_var: MY_OPENAI_KEY
gemini_api_key_env_var: MY_GEMINI_KEY
```

Then set them accordingly:

```bash
export MY_OPENAI_KEY="sk-..."
export MY_GEMINI_KEY="AI..."
```

## Complete Example Configuration

```yaml
# WayfinDex Configuration

# Define environments for different use cases
environments:
  # Production: high-quality models for important research
  - name: prod
    agents:
      - openai_gpt-4
      - gemini_gemini-1.5-pro
      - anthropic_claude-3-opus-20240229

  # Development: faster, cheaper models for testing
  - name: dev
    agents:
      - openai_gpt-3.5-turbo
      - gemini_gemini-pro

  # Testing: single agent for quick checks
  - name: quick
    agents:
      - openai_gpt-3.5-turbo

  # Comparison: mix of providers to compare outputs
  - name: compare
    agents:
      - openai_gpt-4
      - anthropic_claude-3-sonnet-20240229
      - gemini_gemini-pro

# OpenAI Configuration
openai_api_key_env_var: OPENAI_API_KEY
openai_model_names:
  - gpt-4
  - gpt-4-turbo-preview
  - gpt-3.5-turbo

# Gemini Configuration
gemini_api_key_env_var: GEMINI_API_KEY
gemini_model_names:
  - gemini-pro
  - gemini-1.5-pro

# Anthropic Configuration
anthropic_api_key_env_var: ANTHROPIC_API_KEY
anthropic_model_names:
  - claude-3-opus-20240229
  - claude-3-sonnet-20240229
  - claude-3-haiku-20240307
# Optional: Perplexity Configuration
# perplexity_api_key_env_var: PERPLEXITY_API_KEY
# perplexity_model_names:
#   - pplx-7b-online
#   - pplx-70b-online

# Optional: OpenRouter Configuration
# openrouter_api_key_env_var: OPENROUTER_API_KEY
# openrouter_model_names:
#   - anthropic/claude-2
#   - openai/gpt-4
```

## Best Practices

### Environment Strategy

1. **prod**: Use your best models for real research
2. **dev**: Use cheaper models while developing features
3. **quick**: Single fast model for quick lookups
4. **compare**: Multiple providers to see different perspectives

### Cost Management

- Use GPT-3.5-turbo or Claude Haiku for high-volume testing
- Reserve GPT-4 and Claude Opus for production
- Mix models across providers to balance cost and quality

### Model Selection

- **OpenAI GPT-4**: Best general knowledge, great for popular places
- **Gemini Pro**: Good balance of speed and quality
- **Claude Opus**: Excellent at nuanced descriptions
- **Perplexity**: Real-time web search, current information

## Troubleshooting

### "Environment 'X' not found"

Check that the agent group name in your command matches an environment defined in `config.yaml`:

```bash
# List environments
grep -A 1 "name:" config.yaml
```

### "No agents were loaded"

1. Verify API keys are set as environment variables
2. Check that variable names in config.yaml match your exports
3. Ensure model names are spelled correctly
4. Confirm you have valid API keys

### Agent Not Querying

If a specific agent isn't working:

1. Test the API key directly
2. Verify the model name is correct for that provider
3. Check for typos in the agent format (`provider_modelname`)
4. Ensure the provider's configuration section is not commented out

## Advanced Configuration

### Multiple Model Versions

You can test multiple versions of the same model:

```yaml
openai_model_names:
  - gpt-4
  - gpt-4-turbo-preview
  - gpt-4-0125-preview

environments:
  - name: gpt4-comparison
    agents:
      - openai_gpt-4
      - openai_gpt-4-turbo-preview
      - openai_gpt-4-0125-preview
```

### Mixed Provider Environments

Create environments with agents from different providers:

```yaml
environments:
  - name: diverse
    agents:
      - openai_gpt-4
      - gemini_gemini-pro
      - anthropic_claude-3-sonnet-20240229
      - perplexity_pplx-70b-online
```

This gives you different perspectives from different AI systems.
