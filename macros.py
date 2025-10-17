"""
MkDocs macros for WEST Standard Names

This module provides macros to dynamically load and display YAML standard names
directly in MkDocs pages without requiring pre-generation.
"""

import os
import yaml
from pathlib import Path
from collections import defaultdict
from importlib.metadata import version, PackageNotFoundError


def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    # Add package version to environment variables
    try:
        env.variables["package_version"] = version("west-standard-names")
    except PackageNotFoundError:
        env.variables["package_version"] = "dev"

    @env.macro
    def load_standard_names():
        """Load all YAML standard names from the standard_names directory"""
        project_root = Path(env.project_dir)
        standard_names_dir = project_root / "standard_names"
        standard_names = []

        # Only look in the standard_names directory
        if standard_names_dir.exists():
            for root, dirs, files in os.walk(standard_names_dir):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]

                for file in files:
                    if file.endswith(".yml") or file.endswith(".yaml"):
                        yaml_path = Path(root) / file
                        try:
                            with open(yaml_path, "r", encoding="utf-8") as f:
                                data = yaml.safe_load(f)

                            if data and isinstance(data, dict):
                                # Add metadata
                                data["_file_path"] = str(
                                    yaml_path.relative_to(project_root)
                                )
                                data["_category"] = yaml_path.parent.name
                                standard_names.append(data)
                        except Exception as e:
                            print(f"Error loading {yaml_path}: {e}")

        return standard_names

    @env.macro
    def get_categories():
        """Get all unique categories (directories) containing standard names"""
        standard_names = load_standard_names()
        categories = {}

        for item in standard_names:
            category = item.get("_category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

        return categories

    @env.macro
    def get_tags():
        """Group standard names by their primary tags"""
        standard_names = load_standard_names()
        tags_groups = defaultdict(list)

        for item in standard_names:
            if "tags" in item and item["tags"]:
                primary_tag = item["tags"][0]
                tags_groups[primary_tag].append(item)

        return dict(tags_groups)

    @env.macro
    def standard_names_table(items, show_category=False, show_full_description=False):
        """Generate a markdown table for standard names"""
        if not items:
            return "No standard names found."

        # Table header
        headers = ["Standard Name", "Unit", "Description"]
        if show_category:
            headers.append("Category")

        table = "| " + " | ".join(headers) + " |\n"
        table += "|" + "|".join([" --- " for _ in headers]) + "|\n"

        # Sort by name
        sorted_items = sorted(items, key=lambda x: x.get("name", ""))

        for item in sorted_items:
            name = item.get("name", "Unknown")
            unit = item.get("unit", "-")
            description = item.get("description", "No description")

            # Escape special characters but don't truncate if showing full description
            description = description.replace("|", "\\|").replace("\n", " ")
            if not show_full_description and len(description) > 80:
                description = description[:77] + "..."

            # Just show the name as code, no link needed
            name_display = f"`{name}`"

            row = [name_display, unit, description]

            if show_category:
                category = item.get("_category", "Unknown")
                category_display = category.replace("-", " ").title()
                row.append(category_display)

            table += "| " + " | ".join(row) + " |\n"

        return table

    @env.macro
    def standard_name_detail(name):
        """Get detailed information for a specific standard name"""
        standard_names = load_standard_names()

        for item in standard_names:
            if item.get("name") == name:
                return item

        return None

    @env.macro
    def format_tags(tags):
        """Format tags as badges"""
        if not tags:
            return "None"

        formatted = []
        for tag in tags:
            formatted.append(f"`{tag}`")

        return ", ".join(formatted)

    @env.macro
    def standard_names_clean_list():
        """Generate a clean list with standard formatting"""
        result = ""
        categories = get_categories()

        for category, items in categories.items():
            category_name = category.replace("-", " ").title()
            result += f"## **{category_name}** {{#{category}}}\n\n"
            result += "---\n\n"

            sorted_items = sorted(items, key=lambda x: x.get("name", ""))

            for item in sorted_items:
                name = item.get("name", "Unknown")
                unit = item.get("unit", "")
                description = item.get("description", "")
                documentation = item.get("documentation", "")
                item_tags = item.get("tags", [])
                status = item.get("status", "")

                # Format tags as simple text
                tags_display = (
                    ", ".join(f"`{tag}`" for tag in item_tags) if item_tags else "None"
                )

                # Use h3 for standard names (will indent under h2 category in sidebar)
                result += f"### {name}\n\n"

                # Order: description, docs, unit, status, tags
                result += f"{description}\n\n"

                if documentation:
                    result += f"{_fix_markdown_formatting(documentation)}\n\n"

                if unit:
                    result += f"**Unit:** `{unit}`\n\n"

                if status:
                    result += f"**Status:** {status.title()}\n\n"

                if item_tags:
                    result += f"**Tags:** {tags_display}\n\n"

                result += "---\n\n"

        return result

    def _fix_markdown_formatting(text):
        """
        Fix markdown formatting and ensure proper indentation for admonitions
        """
        if not text:
            return ""

        import re

        # Clean up the text first
        text = text.strip()

        # Handle escaped newlines from YAML
        text = text.replace("\\n", "\n")

        # Split into paragraphs and process each one
        paragraphs = text.split("\n\n")
        processed_paragraphs = []

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Handle math equations - preserve them as-is but ensure proper spacing
            if "$$" in paragraph:
                # Block math equations
                processed_paragraphs.append(paragraph)
            elif paragraph.startswith("$$") and paragraph.endswith("$$"):
                # Already a block equation
                processed_paragraphs.append(paragraph)
            elif "$" in paragraph and paragraph.count("$") >= 2:
                # Contains inline math
                processed_paragraphs.append(paragraph)
            # Handle lists (lines starting with - or *)
            elif any(
                line.strip().startswith(("-", "*", "+"))
                for line in paragraph.split("\n")
            ):
                # This is a list, preserve newlines within it
                processed_paragraphs.append(paragraph)
            # Handle numbered lists
            elif any(
                re.match(r"^\d+\.", line.strip()) for line in paragraph.split("\n")
            ):
                # This is a numbered list, preserve newlines within it
                processed_paragraphs.append(paragraph)
            else:
                # Regular text paragraph
                processed_paragraphs.append(paragraph)

        # Join paragraphs back together with proper spacing
        result = "\n\n".join(processed_paragraphs)

        # Ensure math blocks have proper spacing
        result = re.sub(r"\n\s*\$\$", "\n\n$$", result)
        result = re.sub(r"\$\$\s*\n", "$$\n\n", result)

        return result

    @env.macro
    def category_stats():
        """Get statistics about categories and standard names"""
        categories = get_categories()
        tags = get_tags()
        total_names = sum(len(items) for items in categories.values())

        return {
            "total_names": total_names,
            "total_categories": len(categories),
            "total_tags": len(tags),
            "categories": categories,
            "tags": tags,
        }

    @env.macro
    def category_links():
        """Generate clickable category links for the home page"""
        tags = get_tags()
        result = ""

        for category, items in tags.items():
            category_name = category.replace("-", " ").title()
            # MkDocs generates anchors as lowercase with hyphens
            category_anchor = category_name.lower().replace(" ", "-")
            count = len(items)

            result += f"- **[{category_name}](standard-names.md#{category_anchor})** - {count} standard names\n"

        return result.strip()

    @env.macro
    def display_category(category_name):
        """Display all standard names for a specific category in detailed format"""
        result = ""
        tags = get_tags()

        if category_name not in tags:
            return f"Category '{category_name}' not found."

        items = tags[category_name]
        sorted_items = sorted(items, key=lambda x: x.get("name", ""))

        for item in sorted_items:
            name = item.get("name", "Unknown")
            unit = item.get("unit", "")
            description = item.get("description", "")
            documentation = item.get("documentation", "")
            item_tags = item.get("tags", [])
            status = item.get("status", "")

            # Format tags as simple text
            tags_display = (
                ", ".join(f"`{tag}`" for tag in item_tags) if item_tags else "None"
            )

            # Use h3 for standard names
            result += f"### {name}\n\n"

            # Order: description, docs, unit, status, tags
            result += f"{description}\n\n"

            if documentation:
                result += f"{_fix_markdown_formatting(documentation)}\n\n"

            if unit:
                result += f"**Unit:** `{unit}`\n\n"

            if status:
                result += f"**Status:** {status.title()}\n\n"

            if item_tags:
                result += f"**Tags:** {tags_display}\n\n"

            result += "---\n\n"

        return result
