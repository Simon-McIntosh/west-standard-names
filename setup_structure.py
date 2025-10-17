#!/usr/bin/env python3
"""
Simple script to create the basic page templates for MkDocs
This only creates the directory structure and template files
"""

import os
import yaml
from pathlib import Path

def create_basic_structure():
    """Create the basic directory structure and template files"""
    
    # Create directories
    docs_dir = Path("docs")
    tags_dir = docs_dir / "tags" 
    
    tags_dir.mkdir(exist_ok=True)
    
    # Find all YAML files in the standard_names directory
    categories = set()
    all_names = []
    standard_names_dir = Path("standard_names")
    
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
                            name = data.get('name')
                            tags = data.get('tags', [])
                            if name and tags:
                                all_names.append(name)
                                categories.add(tags[0])  # Primary tag
                                
                    except Exception as e:
                        print(f"Error processing {yaml_path}: {e}")
    
    # Create tag category pages
    for category in sorted(categories):
        category_display = category.replace('-', ' ').title()
        content = f"""# {category_display}

This category contains standard names related to {category_display.lower()}.

{{% set tag_items = get_tags()['{category}'] %}}

{{{{ standard_names_table(tag_items) }}}}
"""
        
        with open(tags_dir / f"{category}.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Created {len(categories)} category pages")
    return categories, all_names

def update_navigation(categories):
    """Update mkdocs.yml with navigation structure"""
    mkdocs_path = Path("mkdocs.yml")
    
    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build navigation
    nav_lines = [
        "nav:",
        "  - Home: index.md",
        "  - Standard Names:",
        "    - Overview: overview.md",
        "    - By Category:"
    ]
    
    for category in sorted(categories):
        category_display = category.replace('-', ' ').title()
        nav_lines.append(f"      - {category_display}: tags/{category}.md")
    
    # Replace navigation section
    lines = content.split('\n')
    new_lines = []
    in_nav = False
    
    for line in lines:
        if line.startswith('nav:'):
            in_nav = True
            new_lines.extend(nav_lines)
        elif in_nav and line and not line.startswith(' ') and not line.startswith('\t'):
            in_nav = False
            new_lines.append(line)
        elif not in_nav:
            new_lines.append(line)
    
    with open(mkdocs_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    categories, names = create_basic_structure()
    update_navigation(categories)
    print("Basic structure created successfully!")