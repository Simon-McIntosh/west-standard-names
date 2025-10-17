# WEST Standard Names Documentation

Welcome to the WEST tokamak standard names documentation using DD version 3.42.2.

## Overview

This documentation provides a comprehensive reference for standard names used in the WEST tokamak experiment. Standard names are organized by functional categories and include detailed descriptions, units, and mathematical formulations.

{% set stats = category_stats() %}

## Categories

The standard names are organized into the following categories:

{% for tag, items in stats.tags.items() %}
- **[{{ tag.replace('-', ' ').title() }}](tags/{{ tag }}.md)** - {{ items|length }} standard names
{% endfor %}

## Statistics

- **Total Standard Names**: {{ stats.total_names }}
- **Categories**: {{ stats.total_categories }}
- **Tags**: {{ stats.total_tags }}
- **DD Version**: 3.42.2

## Usage

Navigate through the categories using the navigation menu or use the search functionality to find specific standard names. Each standard name includes:

- **Standard Name**: The unique identifier
- **Description**: Brief description of the quantity
- **Unit**: Physical units (where applicable)
- **Documentation**: Detailed explanation with mathematical formulations
- **Tags**: Categorization tags
- **Status**: Development status

Mathematical equations are rendered using MathJax and follow standard LaTeX syntax.