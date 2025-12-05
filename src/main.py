#!/usr/bin/env python3
"""
WayfinDex - AI-powered place search and note generation CLI.

This application queries multiple AI agents about a place and generates
formatted markdown notes based on their responses.
"""

import argparse
import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path

from helpers.agents import AgentFactory
from helpers.config import WayfinDexConfigLoader
from helpers.templating import TemplateRenderer
from helpers.type_models import PlaceResult


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="wayfindex",
        description="Query AI agents about places and generate markdown notes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wayfindex --agent-group prod --query "Aquarium Zen in North Seattle"
  wayfindex --agent-group dev --output ./notes --query "Pike Place Market"
  wayfindex -ag prod --config /path/to/config.yaml --query "Space Needle"
        """,
    )

    parser.add_argument(
        "--agent-group",
        "-ag",
        dest="agent_group",
        required=True,
        help="Agent group name (e.g., prod, dev, testing) defined in config.yaml",
    )

    parser.add_argument(
        "--query",
        "-q",
        required=True,
        help="The place search query (e.g., 'Aquarium Zen in North Seattle')",
    )

    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help="Output directory for generated notes (default: ./output)",
    )

    parser.add_argument(
        "--config",
        "-c",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )

    parser.add_argument(
        "--template",
        "-t",
        default="place_note.md",
        help="Template file name (default: place_note.md)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    return parser.parse_args()


def sanitize_slug(slug: str) -> str:
    """
    Sanitize and validate a slug to ensure it's safe for filenames.

    Converts to lowercase, removes non-alphanumeric characters (except hyphens),
    and ensures the slug is not empty.

    Args:
        slug: The slug to sanitize

    Returns:
        A safe, validated slug suitable for filenames
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = slug.lower().strip()
    slug = re.sub(r"\s+", "-", slug)

    # Remove any character that isn't alphanumeric or hyphen
    slug = re.sub(r"[^a-z0-9-]", "", slug)

    # Remove multiple consecutive hyphens
    slug = re.sub(r"-+", "-", slug)

    # Remove leading/trailing hyphens
    slug = slug.strip("-")

    # If slug is empty after sanitization, use a fallback
    if not slug:
        slug = "unknown-place"

    return slug


async def query_agent(agent_wrapper, query: str, verbose: bool = False) -> PlaceResult:
    """
    Query a single agent and return the result.

    Args:
        agent_wrapper: PlaceSearchAgent wrapper containing the agent
        query: The search query
        verbose: Whether to print verbose output

    Returns:
        PlaceResult containing the agent's response
    """
    if verbose:
        print(f"  Querying {agent_wrapper.name}...")

    try:
        result = await agent_wrapper.agent.run(query)

        if verbose:
            print(f"  ✓ {agent_wrapper.name} completed")

        return PlaceResult(
            agent_name=agent_wrapper.name,
            query=query,
            output=result.data,
            usage=result.usage() if hasattr(result, "usage") else None,
        )
    except Exception as e:
        print(f"  ✗ Error querying {agent_wrapper.name}: {e}", file=sys.stderr)
        raise


async def query_all_agents(
    agents: list, query: str, verbose: bool = False
) -> list[PlaceResult]:
    """
    Query all agents concurrently.

    Args:
        agents: List of PlaceSearchAgent wrappers
        query: The search query
        verbose: Whether to print verbose output

    Returns:
        List of PlaceResult objects
    """
    if verbose:
        print(f"\nQuerying {len(agents)} agent(s)...")

    tasks = [query_agent(agent, query, verbose) for agent in agents]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and log them
    valid_results = []
    for result in results:
        if isinstance(result, Exception):
            print(f"Agent query failed: {result}", file=sys.stderr)
        else:
            valid_results.append(result)

    return valid_results


def render_and_save_note(
    result: PlaceResult,
    template_renderer: TemplateRenderer,
    template_name: str,
    output_dir: Path,
    verbose: bool = False,
) -> Path:
    """
    Render a template with agent result data and save to file.

    Args:
        result: PlaceResult containing agent response
        template_renderer: TemplateRenderer instance
        template_name: Name of the template file
        output_dir: Directory to save the output file
        verbose: Whether to print verbose output

    Returns:
        Path to the saved file
    """
    # Prepare template data
    template_data = {
        "name": result.output.name,
        "slug": result.output.slug,
        "address": result.output.address,
        "category": (
            result.output.category.suggested_new_category
            if hasattr(result.output.category, "suggested_new_category")
            else result.output.category
        ),
        "description": result.output.description,
        "open_hours": result.output.open_hours,
        "website": result.output.website,
        "tips": result.output.tips,
    }

    # Render the template
    rendered_content = template_renderer.render(template_name, template_data)

    # Create filename using agent name, slug, and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_slug = sanitize_slug(result.output.slug)

    filename = f"{result.agent_name}_{safe_slug}_{timestamp}.md"
    output_path = output_dir / filename

    # Save to file
    with open(output_path, "w") as f:
        f.write(rendered_content)

    if verbose:
        print(f"  Saved: {output_path}")

    return output_path


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()

    try:
        # Print header
        if args.verbose:
            print("=" * 70)
            print("WayfinDex - AI Place Search & Note Generator")
            print("=" * 70)

        # Load configuration
        if args.verbose:
            print(f"\nLoading configuration from: {args.config}")

        config_loader = WayfinDexConfigLoader(config_path=args.config)

        # Set environment
        if args.verbose:
            available_groups = config_loader.get_available_environments()
            print(f"Available agent groups: {', '.join(available_groups)}")
            print(f"Selected agent group: {args.agent_group}")

        try:
            config_loader.set_environment(args.agent_group)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        # Initialize agent factory and load agents
        if args.verbose:
            print(
                f"\nInitializing agents: {', '.join(config_loader.config.active_agents)}"
            )

        agent_factory = AgentFactory(config_loader)
        agents = agent_factory.load_agents()

        if not agents:
            print(
                "Error: No agents were loaded. Check your configuration and API keys.",
                file=sys.stderr,
            )
            sys.exit(1)

        if args.verbose:
            print(f"Loaded {len(agents)} agent(s)")

        # Query all agents
        print(f"\nSearching for: {args.query}")
        results = asyncio.run(query_all_agents(agents, args.query, args.verbose))

        if not results:
            print("Error: No results were returned from any agents.", file=sys.stderr)
            sys.exit(1)

        print(f"\nReceived {len(results)} result(s)")

        # Set up template renderer
        templates_dir = Path(__file__).parent / "templates"
        template_renderer = TemplateRenderer(templates_dir)

        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        if args.verbose:
            print(f"\nOutput directory: {output_dir.absolute()}")

        # Render and save notes
        print("\nGenerating notes...")
        saved_files = []
        for result in results:
            try:
                output_path = render_and_save_note(
                    result,
                    template_renderer,
                    args.template,
                    output_dir,
                    args.verbose,
                )
                saved_files.append(output_path)
            except Exception as e:
                print(
                    f"Error rendering note for {result.agent_name}: {e}",
                    file=sys.stderr,
                )

        # Print summary
        print(f"\n{'=' * 70}")
        print(f"Successfully generated {len(saved_files)} note(s)")
        if not args.verbose:
            print("\nGenerated files:")
            for file_path in saved_files:
                print(f"  - {file_path}")
        print(f"{'=' * 70}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
