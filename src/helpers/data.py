"""
Data utilities for loading and saving JSON files.

This module provides helper functions for JSON file operations, particularly
for managing place categories used in agent validation.
"""

import json
from pathlib import Path


def load_json(file_path):
    """
    Load and parse JSON data from a file.

    Args:
        file_path: Path to the JSON file to load

    Returns:
        Parsed JSON data as a Python dictionary or list

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def save_json(file_path, data):
    """
    Save data to a JSON file with pretty formatting.

    Args:
        file_path: Path where the JSON file should be saved
        data: Python dictionary or list to serialize to JSON
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def load_categories(file_path=None):
    """
    Load place categories from a JSON file.

    Categories are used for validating and categorizing places in AI agent responses.
    If no file path is provided, uses the default categories.json in the src directory.
    If the file doesn't exist, creates it with default categories.

    Args:
        file_path: Optional path to categories JSON file

    Returns:
        List of category strings (e.g., ['restaurant', 'cafe', 'museum'])
    """
    if file_path is None:
        # Default to categories.json in the src directory
        file_path = Path(__file__).parent.parent / "categories.json"
    
    # If file doesn't exist, create it with default categories
    if not Path(file_path).exists():
        default_categories = [
            "restaurant",
            "cafe",
            "bar",
            "museum",
            "park",
            "shopping",
            "attraction",
            "entertainment",
            "hotel",
            "services"
        ]
        save_categories(default_categories, str(file_path))
        return default_categories
    
    data = load_json(file_path)
    return data.get("categories", [])


def save_categories(categories: list[str], file_path="categories.json"):
    """
    Save place categories to a JSON file.

    Wraps the category list in a JSON object with a 'categories' key.

    Args:
        categories: List of category strings to save
        file_path: Path where the categories JSON file should be saved
    """
    data = {"categories": categories}
    save_json(file_path, data)
