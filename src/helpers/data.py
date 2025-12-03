import json


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def save_json(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def load_categories(file_path="categories.json"):
    """Load categories from a JSON file."""
    data = load_json(file_path)
    return data.get("categories", [])


def save_categories(categories: list[str], file_path="categories.json"):
    """Save categories to a JSON file."""
    data = {"categories": categories}
    save_json(file_path, data)
