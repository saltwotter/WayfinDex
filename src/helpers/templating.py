"""
Templating utilities for rendering markdown templates with Jinja2.
Provides validation functions to ensure template data completeness.
"""

import warnings
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template, meta


class TemplateRenderer:
    """
    A class to handle Jinja2 template rendering with validation.
    Manages the Jinja2 environment and provides methods for rendering templates.
    """

    def __init__(self, template_dir: str | Path):
        """
        Initialize the TemplateRenderer with a template directory.

        Args:
            template_dir: Path to the directory containing templates
        """
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def extract_template_variables(self, template_name: str) -> set[str]:
        """
        Extract all variable names used in a Jinja2 template file.

        Args:
            template_name: Name of the template file

        Returns:
            Set of variable names found in the template
        """
        loader = self.env.loader
        if loader is None:
            raise ValueError("Template loader is not configured")

        template_source = loader.get_source(self.env, template_name)[0]
        parsed_content = self.env.parse(template_source)

        return meta.find_undeclared_variables(parsed_content)

    def validate_data(
        self, data: dict[str, Any], template_name: str, strict: bool = True
    ) -> dict[str, list[str]]:
        """
        Validate that the provided data dictionary matches template requirements.

        Args:
            data: Dictionary with values to render in the template
            template_name: Name of the template file
            strict: If True, check for extra keys not used in template

        Returns:
            Dictionary with 'missing' and 'extra' keys containing lists of issues
        """
        template_vars = self.extract_template_variables(template_name)
        data_keys = set(data.keys())

        missing_vars = template_vars - data_keys
        extra_keys = data_keys - template_vars if strict else set()

        return {"missing": list(missing_vars), "extra": list(extra_keys)}

    def render(
        self,
        template_name: str,
        data: dict[str, Any],
        validate: bool = True,
        strict: bool = True,
    ) -> str:
        """
        Render a Jinja2 template with provided data.

        Args:
            template_name: Name of the template file
            data: Dictionary with values to render in the template
            validate: If True, validate data before rendering
            strict: If True, warn about extra keys not used in template

        Returns:
            Rendered template as a string

        Raises:
            ValueError: If required template variables are missing
            UserWarning: If extra keys are provided (when strict=True)
        """
        if validate:
            validation_result = self.validate_data(data, template_name, strict)

            if validation_result["missing"]:
                raise ValueError(
                    f"Missing required template variables: {', '.join(validation_result['missing'])}"
                )

            if strict and validation_result["extra"]:
                warnings.warn(
                    f"Extra keys provided that are not used in template: {', '.join(validation_result['extra'])}",
                    UserWarning,
                )

        template = self.env.get_template(template_name)
        return template.render(**data)

    def render_string(self, template_string: str, data: dict[str, Any]) -> str:
        """
        Render a Jinja2 template from a string with provided data.

        Args:
            template_string: Template content as a string
            data: Dictionary with values to render in the template

        Returns:
            Rendered template as a string
        """
        template = self.env.from_string(template_string)
        return template.render(**data)

    def get_template(self, template_name: str) -> Template:
        """
        Get a compiled Jinja2 template object.

        Args:
            template_name: Name of the template file

        Returns:
            Compiled Jinja2 Template object
        """
        return self.env.get_template(template_name)
