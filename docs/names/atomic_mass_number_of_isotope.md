# atomic_mass_number_of_isotope

{% set item = standard_name_detail('atomic_mass_number_of_isotope') %}

## Description

{{ item.description if item else 'No description available.' }}

## Details

{% if item %}
| Property | Value |
|----------|--------|
| **Standard Name** | `{{ item.name }}` |
| **Unit** | {{ item.unit if item.unit else 'Not specified' }} |
| **Kind** | {{ item.kind if item.kind else 'Not specified' }} |
| **Status** | {{ item.status if item.status else 'Unknown' }} |
| **Category** | {{ item._category.replace('-', ' ').title() if item._category else 'Unknown' }} |
| **Tags** | {{ format_tags(item.tags) if item.tags else 'None' }} |

## Documentation

{{ item.documentation if item.documentation else 'No detailed documentation available.' }}

## Navigation

{% if item.tags %}
- **Category**: [{{ item._category.replace('-', ' ').title() }}](../tags/{{ item.tags[0] }}.md)
{% endif %}
- **All Names**: [Overview](../overview.md)
{% else %}
Standard name not found.
{% endif %}

---

*This standard name is part of the WEST tokamak standard names using DD version 3.42.2.*
