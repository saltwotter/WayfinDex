# Quick Start Guide

Get WayfinDex running in under 5 minutes.

## Installation

1. **Clone or navigate to the repository:**

   ```bash
   cd WayfinDex
   ```

2. **Install dependencies and the CLI tool:**

   ```bash
   uv sync
   uv pip install -e .
   ```

3. **Verify installation:**
   ```bash
   wayfindex --help
   ```

You should see the command options displayed.

## Configuration

1. **Create your config file:**

   ```bash
   cp config.yaml.example config.yaml
   ```

2. **Edit `config.yaml` to enable your preferred AI provider(s):**

   - Uncomment the sections for providers you want to use
   - Keep the ones you don't need commented out
   - Make sure model names are correct

3. **Set API keys as environment variables:**

   ```bash
   export OPENAI_API_KEY="sk-..."
   export GEMINI_API_KEY="AI..."
   # Add others as needed
   ```

   **Tip**: Add these to your `~/.zshrc` or `~/.bashrc` to make them permanent.

## First Run

Run your first place search:

```bash
wayfindex --agent-group prod --query "Pike Place Market" --verbose
```

The `--verbose` flag shows you what's happening step by step.

## Check Your Results

Look in the `output/` directory:

```bash
ls output/
```

You should see markdown files like:

```
openai-gpt-4_Pike_Place_Market_20251204_143022.md
```

Open them to see the generated place notes!

## Common Workflows

### Quick Search (Single Agent)

```bash
wayfindex --agent-group quick --query "Local Coffee Shop"
```

### Compare Multiple AI Models

```bash
wayfindex --agent-group compare --query "Space Needle"
```

This creates multiple notes from different AI providers for comparison.

### Custom Output Location

```bash
wayfindex --agent-group prod --output ~/Documents/places --query "Museum of Pop Culture"
```

### Different Template

```bash
wayfindex --agent-group prod --template custom_note.md --query "Some Place"
```

## Troubleshooting

### "Configuration file config.yaml not found"

**Solution**: Make sure you're running the command from the repository root directory, or use the `--config` flag:

```bash
wayfindex --config /path/to/config.yaml --agent-group prod --query "Place Name"
```

### "Environment 'X' not found"

**Solution**: Check what agent groups are defined in your `config.yaml`:

```bash
grep -A 2 "name:" config.yaml
```

Make sure you're using one of those names with the `--agent-group` flag.

### "No agents were loaded"

This usually means your API keys aren't set correctly.

**Check**:

1. Did you export your API keys?
   ```bash
   echo $OPENAI_API_KEY
   ```
2. Do the environment variable names in `config.yaml` match your exports?

   ```yaml
   openai_api_key_env_var: OPENAI_API_KEY # Must match your export
   ```

3. Are the model names spelled correctly in your config?

4. Did you uncomment the provider configuration sections you want to use?

### "Module not found" or import errors

**Solution**: Reinstall from the repository root:

```bash
uv pip install -e .
```

### No output files created

**Check**:

1. Did the command complete successfully?
2. Look for error messages in the output
3. Try with `--verbose` to see what's happening
4. Check that the output directory is writable

## Next Steps

- **Customize your agent groups**: Edit `config.yaml` to create custom agent combinations
- **Try different providers**: Experiment with different AI models to compare results
- **Create custom templates**: Edit templates in `src/templates/` to change output format
- **Read the docs**: Check [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) for advanced configuration options

## Getting Help

If you run into issues:

1. Check the error message carefully
2. Try running with `--verbose` for more details
3. Verify your API keys are valid
4. Make sure your config.yaml matches the expected format
5. Check that you have the required Python version (3.13+)

## Quick Reference

**Basic command structure:**

```bash
wayfindex --agent-group GROUP_NAME --query "PLACE NAME" [OPTIONS]
```

**Essential options:**

- `--agent-group` or `-ag`: Which agent group to use (required)
- `--query` or `-q`: What place to search for (required)
- `--output` or `-o`: Where to save notes
- `--verbose` or `-v`: Show detailed progress
- `--config` or `-c`: Use a different config file

**Example commands:**

```bash
# Simple search
wayfindex --agent-group prod -q "Coffee Shop"

# Verbose with custom output
wayfindex --agent-group dev -q "Museum" -o ~/notes -v

# Different config file
wayfindex -c custom.yaml -ag testing -q "Restaurant"
```
