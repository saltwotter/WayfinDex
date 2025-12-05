# WayfinDex Documentation

Welcome to the WayfinDex documentation. Here's where to find what you need.

## Documentation Overview

### For Users

- **[Main README](../README.md)** - Start here! Overview, quick start, and basic usage
- **[Quick Start Guide](../QUICKSTART.md)** - Step-by-step installation and first run
- **[Configuration Guide](CONFIGURATION.md)** - Detailed configuration options and examples

### For Developers

- **[Architecture](ARCHITECTURE.md)** - How WayfinDex works internally
- **Source Code Docstrings** - All Python modules have comprehensive inline documentation

## Quick Navigation

**I want to...**

- **Get started quickly** → [Quick Start Guide](../QUICKSTART.md)
- **Understand what WayfinDex does** → [Main README](../README.md)
- **Configure multiple AI providers** → [Configuration Guide](CONFIGURATION.md)
- **Understand the codebase** → [Architecture](ARCHITECTURE.md)
- **Fix an error** → Check troubleshooting in [Quick Start](../QUICKSTART.md) or [Configuration](CONFIGURATION.md)
- **Add a new AI provider** → See "Extension Points" in [Architecture](ARCHITECTURE.md)
- **Customize output templates** → See "What You Get" in [Main README](../README.md)
- **Understand the data flow** → [Architecture - Data Flow](ARCHITECTURE.md#data-flow)

## Documentation Principles

WayfinDex documentation follows these principles:

1. **README**: User-focused, concise, gets you running quickly
2. **QUICKSTART**: Hands-on guide with common workflows
3. **Configuration Guide**: Complete reference for all config options
4. **Architecture**: Technical deep-dive for developers and contributors

## Getting Help

1. **Start with the error message** - Most errors have clear explanations
2. **Check troubleshooting** - Both QUICKSTART and Configuration docs have troubleshooting sections
3. **Review your config** - Many issues come from configuration mismatches
4. **Enable verbose mode** - Use `--verbose` to see what's happening
5. **Check the architecture** - Understanding the flow helps debug issues

## Contributing to Documentation

When updating documentation:

- Keep the README user-focused and concise
- Put technical details in docs/CONFIGURATION.md or docs/ARCHITECTURE.md
- Update QUICKSTART.md when adding new workflows
- Add docstrings to all new functions and classes
- Update examples when changing behavior

## Project Files Quick Reference

```
WayfinDex/
├── README.md              ← Start here
├── QUICKSTART.md          ← Installation & first run
├── .env.example           ← Environment variables template
├── categories.json        ← Place categories (auto-created)
├── docs/
│   ├── README.md          ← This file
│   ├── CONFIGURATION.md   ← Complete config reference
│   └── ARCHITECTURE.md    ← Technical documentation
├── config.yaml.example    ← Configuration template
├── src/
│   ├── main.py           ← CLI entry point
│   ├── helpers/          ← Core modules (well-documented)
│   ├── prompts/          ← Agent system prompts
│   └── templates/        ← Output templates
└── output/               ← Generated notes (created on first run)
```
