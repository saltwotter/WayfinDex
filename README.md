# WayfinDex

**AI-powered place research that generates structured markdown notes**

WayfinDex queries multiple AI models simultaneously to gather comprehensive information about any place, then generates clean, organized markdown notes. Perfect for travel planning, location research, or building a personal knowledge base of places.

## Quick Start

1. **Install the tool:**

   ```bash
   uv sync
   uv pip install -e .
   ```

2. **Configure your setup:**

   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml with your preferred AI providers and models
   ```

3. **Set API keys:**

   **Option 1: Use .env file (recommended)**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

   **Option 2: Export as environment variables**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export GEMINI_API_KEY="your-key-here"
   ```

4. **Run your first search:**

   ```bash
   wayfindex --agent-group prod --query "Pike Place Market"
   ```

That's it! Check the `output/` directory for your generated markdown notes.

## Usage

### Basic Command

```bash
wayfindex --agent-group prod --query "Aquarium Zen in North Seattle"
```

### Common Options

```bash
# Custom output directory
wayfindex --agent-group dev --output ./notes --query "Space Needle"

# Verbose mode (see what's happening)
wayfindex --agent-group prod --verbose --query "Museum of Pop Culture"

# Different config file
wayfindex -ag testing --config custom-config.yaml --query "Local Coffee Shop"
```

### All Options

- `--agent-group` or `-ag` (required): Which agent group to use (defined in config.yaml)
- `--query` or `-q` (required): The place you want to research
- `--output` or `-o`: Where to save notes (default: `./output`)
- `--config` or `-c`: Config file path (default: `config.yaml`)
- `--template` or `-t`: Template file name (default: `place_note.md`)
- `--verbose` or `-v`: Show detailed progress

## How It Works

1. You specify a place and agent group (e.g., "prod" with GPT-4 and Gemini)
2. WayfinDex queries all configured AI agents concurrently
3. Each agent researches the place and returns structured data including a URL-safe slug
4. Results are rendered into markdown files using customizable templates
5. Files are saved with clean, readable names: `{agent}_{slug}_{timestamp}.md`

**Example filename:** `openai-gpt-4_pike-place-market_20251205_143022.md`

## What You Get

Each generated note includes:

- **Name and address** of the place
- **URL-safe slug** (for clean, readable filenames)
- **Category** (auto-categorized or suggested)
- **Description** of what makes it special
- **Hours of operation**
- **Website** (if available)
- **Tips** for visiting

You can customize the output by editing:

- **Templates** in `src/templates/` to change the note format
- **Agent prompts** in `src/prompts/` to change how agents search
- **Categories** in `src/categories.json` to add new place types

## Configuration

WayfinDex supports multiple AI providers:

- OpenAI (GPT-4, GPT-3.5, etc.)
- Google Gemini
- Anthropic Claude
- Perplexity
- OpenRouter

Create different environments for different use cases:

- **prod**: High-quality models for important research
- **dev**: Faster, cheaper models for testing
- **testing**: Mix of models to compare outputs

See [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) for detailed configuration options.

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Step-by-step setup and troubleshooting
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed config options and examples
- **[Architecture](docs/ARCHITECTURE.md)** - How WayfinDex works under the hood

## Requirements

- Python 3.13+
- API keys for at least one AI provider
- `uv` package manager (recommended) or `pip`

## Project Status

🚧 **Early Development** - WayfinDex is functional but actively evolving. Expect changes to the API and configuration format.

## License

See [LICENSE](LICENSE) file for details.
