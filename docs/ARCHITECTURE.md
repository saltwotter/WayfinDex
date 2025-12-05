# Architecture Documentation

This document explains how WayfinDex works internally and how the components interact.

## Overview

WayfinDex is a Python CLI application that orchestrates multiple AI agents to research places and generate structured markdown notes. It's built with:

- **Pydantic AI**: For AI agent orchestration and structured outputs
- **Jinja2**: For template rendering
- **Pydantic**: For data validation and models
- **asyncio**: For concurrent agent queries

## System Architecture

```
┌─────────────┐
│   CLI       │ wayfindex --agent-group prod --query "Place"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  main.py                                    │
│  • Parse arguments                          │
│  • Load configuration                       │
│  • Initialize agents                        │
│  • Run queries concurrently                 │
│  • Render templates                         │
└──────────────┬──────────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌───────────┐    ┌──────────────┐
│  Config   │    │  Agents      │
│  Loader   │    │  Factory     │
└─────┬─────┘    └──────┬───────┘
      │                 │
      │                 ▼
      │          ┌─────────────────────┐
      │          │  AI Provider APIs   │
      │          │  • OpenAI           │
      │          │  • Gemini           │
      │          │  • Anthropic        │
      │          │  • Perplexity       │
      │          │  • OpenRouter       │
      │          └──────────┬──────────┘
      │                     │
      │                     ▼
      │          ┌───────────────────────┐
      │          │  PlaceNote Models     │
      │          │  (Pydantic Validation)│
      │          └──────────┬────────────┘
      │                     │
      └─────────┬───────────┘
                ▼
        ┌──────────────┐
        │  Template    │
        │  Renderer    │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  Markdown    │
        │  Output      │
        └──────────────┘
```

## Core Components

### 1. CLI Entry Point (`main.py`)

**Purpose**: Orchestrates the entire workflow from user input to file output.

**Key Functions**:

- `parse_arguments()`: Handles command-line argument parsing
- `query_agent()`: Queries a single agent asynchronously
- `query_all_agents()`: Runs all agent queries concurrently
- `render_and_save_note()`: Renders template and saves markdown file
- `main()`: Coordinates the entire process

**Flow**:

1. Parse CLI arguments
2. Load configuration
3. Set environment (activates specific agents)
4. Initialize agent factory
5. Query all agents concurrently
6. Render and save results

### 2. Configuration Loader (`helpers/config.py`)

**Purpose**: Manages application configuration from YAML files.

**Class**: `WayfinDexConfigLoader`

**Key Methods**:

- `load_config()`: Reads and validates YAML configuration
- `set_environment(name)`: Activates a specific environment's agents
- `get_available_environments()`: Returns list of configured environments

**Validation**: Uses Pydantic's `WayfinDexConfig` model to ensure configuration validity.

### 3. Agent Factory (`helpers/agents.py`)

**Purpose**: Creates and manages AI agents based on configuration.

**Class**: `AgentFactory`

**Key Methods**:

- `load_agents()`: Loads all agents for active providers
- `create_openai_agents()`: Initializes OpenAI agents
- `create_gemini_agents()`: Initializes Gemini agents
- `create_anthropic_agents()`: Initializes Anthropic agents
- `create_openrouter_agents()`: Initializes OpenRouter agents
- `create_perplexity_agents()`: Initializes Perplexity agents

**Agent Creation Pattern**:

```python
# For each model in the config:
1. Get API key from environment variable
2. Create provider instance
3. Create model instance
4. Create Agent with:
   - Model
   - System prompt
   - Output type (PlaceNote model)
5. Wrap in PlaceSearchAgent for tracking
```

### 4. Type Models (`helpers/type_models.py`)

**Purpose**: Defines data structures and validation rules.

**Key Models**:

- `WayfinDexConfig`: Configuration structure validation
- `AgentEnvironment`: Environment definition
- `PlaceSearchAgent`: Agent wrapper with name and agent instance
- `PlaceResult`: Contains agent response and metadata
- `PlaceNote`: Dynamically created based on available categories

**Dynamic Model Creation**:

```python
create_place_note_model(categories: list[str])
```

Creates a Pydantic model with category validation based on loaded categories.

### 5. Template Renderer (`helpers/templating.py`)

**Purpose**: Handles Jinja2 template rendering with validation.

**Class**: `TemplateRenderer`

**Key Methods**:

- `extract_template_variables()`: Finds all variables in a template
- `validate_data()`: Ensures data matches template requirements
- `render()`: Renders template with data (with validation)
- `render_string()`: Renders template from string

**Validation Features**:

- Detects missing required variables
- Warns about unused data keys
- Prevents template errors before rendering

### 6. Data Utilities (`helpers/data.py`)

**Purpose**: Manages JSON data loading and saving.

**Key Functions**:

- `load_categories()`: Loads place categories from JSON
- `save_categories()`: Saves categories to JSON
- `load_json()`: Generic JSON file loader
- `save_json()`: Generic JSON file saver

## Data Flow

### Query Execution Flow

```
User Input
    │
    ▼
┌──────────────────────────┐
│ Parse CLI Arguments      │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Load Config & Set Env    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Initialize Agent Factory │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Load Active Agents       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Query All Agents (Concurrent)    │
│  ┌────────────┐  ┌────────────┐  │
│  │ Agent 1    │  │ Agent 2    │  │
│  │ (GPT-4)    │  │ (Gemini)   │  │
│  └─────┬──────┘  └─────┬──────┘  │
│        │               │         │
│        ▼               ▼         │
│  ┌────────────┐  ┌────────────┐  │
│  │ PlaceResult│  │ PlaceResult│  │
│  └────────────┘  └────────────┘  │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────┐
│ For Each Result:         │
│  • Prepare template data │
│  • Render template       │
│  • Generate filename     │
│  • Save to disk          │
└──────────┬───────────────┘
           │
           ▼
      Markdown Files
```

### Template Rendering Flow

```
PlaceResult
    │
    ▼
┌─────────────────────────┐
│ Extract Relevant Data   │
│  • name                 │
│  • address              │
│  • category             │
│  • description          │
│  • open_hours           │
│  • website              │
│  • tips                 │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Validate Against        │
│ Template Variables      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Render Jinja2 Template  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Generate Filename       │
│ {agent}_{place}_{time}  │
└──────────┬──────────────┘
           │
           ▼
      Markdown File
```

## Concurrency Model

WayfinDex uses `asyncio` to query multiple agents simultaneously:

```python
# Create tasks for all agents
tasks = [query_agent(agent, query, verbose) for agent in agents]

# Run all queries concurrently
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**Benefits**:

- Faster overall execution (queries run in parallel)
- Better resource utilization
- Graceful error handling (one agent failure doesn't stop others)

## Error Handling

### Configuration Errors

- Missing config file → Clear error message with instructions
- Invalid environment → List available environments
- Missing API keys → Specific error about which key is missing

### Runtime Errors

- Agent query failure → Continue with other agents, log error
- Template rendering failure → Skip that result, continue with others
- File save errors → Report but continue

### User Interruption

- Ctrl+C handling → Clean exit with status message

## Extension Points

### Adding New AI Providers

1. Add provider configuration to `type_models.py`:

```python
newprovider_api_key_env_var: str | None
newprovider_model_names: list[str] | None
```

2. Create agent factory method in `agents.py`:

```python
def create_newprovider_agents(self) -> list[PlaceSearchAgent]:
    # Implementation
```

3. Update `load_agents()` to include new provider

### Custom Templates

1. Create new template in `src/templates/`
2. Use with `--template` flag:

```bash
wayfindex --agent-group prod --query "Place" --template my_template.md
```

### Custom Agent Prompts

1. Edit existing prompt in `src/prompts/place_search.txt`
2. Or create new prompt file for specialized use cases
3. Update `agents.py` to load the new prompt in relevant agent creation methods

### Custom Categories

Categories are automatically created with defaults if `src/categories.json` doesn't exist. To customize:

```json
{
  "categories": ["restaurant", "cafe", "your-new-category"]
}
```

The system will auto-generate this file on first run if it's missing.

## Performance Considerations

### Agent Query Time

- Varies by provider and model
- GPT-4: ~5-15 seconds
- GPT-3.5: ~2-5 seconds
- Gemini: ~3-8 seconds

### Concurrent Execution

- 3 agents @ 10s each → ~10s total (not 30s)
- Network bandwidth: minimal impact
- API rate limits: check provider documentation

### File I/O

- Template loading: cached by Jinja2
- Config loading: once at startup
- Output writes: negligible time

## Security Considerations

### API Keys

- Stored only in environment variables
- Never committed to config files
- Never logged or printed

### User Input

- Query strings passed directly to AI models
- No SQL injection risk (no database)
- No command injection (no shell execution)

### File Output

- Sanitized filenames (removes special characters)
- Creates files with predictable names
- No arbitrary file system access

## Dependencies

### Core Dependencies

- `pydantic`: Data validation and settings
- `pydantic-ai`: AI agent framework
- `jinja2`: Template engine
- `pyyaml`: Configuration parsing

### Provider SDKs (via pydantic-ai)

- OpenAI
- Google (Gemini)
- Anthropic
- OpenRouter
- Perplexity (via OpenAI-compatible API)

## Future Architecture Considerations

### Potential Improvements

1. **Caching Layer**: Cache API responses to avoid redundant queries
2. **Database Storage**: Store results in SQLite for search/analysis
3. **Streaming Output**: Stream results as they arrive instead of batch
4. **Plugin System**: Modular provider system for easier extensions
5. **Web Interface**: Optional web UI for non-CLI users
6. **Result Aggregation**: Combine multiple agent responses into single notes

### Scalability

Current architecture handles:

- Any number of configured environments
- Any number of agents per environment
- Any number of providers
- Concurrent queries limited only by system resources

For production use at scale:

- Add rate limiting
- Implement retry logic
- Add request queuing
- Consider distributed execution
