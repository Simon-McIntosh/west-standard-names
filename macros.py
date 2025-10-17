"""
MkDocs macros for WEST Standard Names

This module provides macros to dynamically load and display YAML standard names
directly in MkDocs pages without requiring pre-generation.
"""

import os
import yaml
from pathlib import Path
from collections import defaultdict

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """
    
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
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if file.endswith('.yml') or file.endswith('.yaml'):
                        yaml_path = Path(root) / file
                        try:
                            with open(yaml_path, 'r', encoding='utf-8') as f:
                                data = yaml.safe_load(f)
                            
                            if data and isinstance(data, dict):
                                # Add metadata
                                data['_file_path'] = str(yaml_path.relative_to(project_root))
                                data['_category'] = yaml_path.parent.name
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
            category = item.get('_category', 'unknown')
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
            if 'tags' in item and item['tags']:
                primary_tag = item['tags'][0]
                tags_groups[primary_tag].append(item)
        
        return dict(tags_groups)
    
    @env.macro
    def standard_names_table(items, show_category=False):
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
        sorted_items = sorted(items, key=lambda x: x.get('name', ''))
        
        for item in sorted_items:
            name = item.get('name', 'Unknown')
            unit = item.get('unit', '-')
            description = item.get('description', 'No description')
            
            # Escape and truncate description
            description = description.replace('|', '\\|').replace('\n', ' ')
            if len(description) > 80:
                description = description[:77] + "..."
            
            # Create link to individual page
            name_link = f"[`{name}`](names/{name}.md)"
            
            row = [name_link, unit, description]
            
            if show_category:
                category = item.get('_category', 'Unknown')
                category_display = category.replace('-', ' ').title()
                primary_tag = item.get('tags', [''])[0] if item.get('tags') else category
                category_link = f"[{category_display}](tags/{primary_tag}.md)"
                row.append(category_link)
            
            table += "| " + " | ".join(row) + " |\n"
        
        return table
    
    @env.macro
    def standard_name_detail(name):
        """Get detailed information for a specific standard name"""
        standard_names = load_standard_names()
        
        for item in standard_names:
            if item.get('name') == name:
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
    def category_stats():
        """Get statistics about categories and standard names"""
        categories = get_categories()
        tags = get_tags()
        total_names = sum(len(items) for items in categories.values())
        
        return {
            'total_names': total_names,
            'total_categories': len(categories),
            'total_tags': len(tags),
            'categories': categories,
            'tags': tags
        }