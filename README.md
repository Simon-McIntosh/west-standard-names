# WEST Tokamak: Standard Names

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://west-standard-names.github.io/west-standard-names/)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

Comprehensive standard names documentation for the WEST (W Environment in Steady-state Tokamak) facility, based on DD version 3.42.2.

## Overview

This project provides a searchable, well-organized documentation of standard names used in WEST tokamak data, including:

- **Core Physics**: Electron density, temperature, pressure, and effective charge
- **Equilibrium**: Plasma boundary parameters, flux surfaces, and magnetic field quantities
- **Magnetics**: Magnetic field probes, flux loops, and diagnostic measurements
- **Coils & Control**: PF coil parameters and passive loop characteristics
- **Diagnostics**: Interferometry, spectroscopy, and radiation measurements
- **Heating**: Ion cyclotron heating parameters
- **Fueling**: Fueling system measurements

## Documentation

📚 **[View the Standard Names Documentation →](https://west-standard-names.github.io/west-standard-names/standard-names/)**

The documentation includes:

- Complete list of all standard names organized by category
- Detailed descriptions and units for each quantity
- LaTeX-rendered mathematical expressions
- Search functionality for quick reference

## Installation

This is primarily a documentation project. To build the documentation locally:

```bash
# Clone the repository
git clone https://github.com/west-standard-names/west-standard-names.git
cd west-standard-names

# Install dependencies (requires Python 3.12+)
pip install -e .

# Serve the documentation locally
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.

## Project Structure

```
standard_names/
├── core-physics/          # Core plasma parameters
├── equilibrium/           # Equilibrium reconstruction quantities
├── magnetics/            # Magnetic diagnostics
├── coils-and-control/    # Coil and control parameters
├── interferometry/       # Interferometry measurements
├── spectroscopy/         # Spectroscopic diagnostics
├── radiation-diagnostics/ # Radiation measurements
├── ic-heating/           # Ion cyclotron heating
└── fueling/              # Fueling system parameters
```

Each standard name is defined in a YAML file with:

- Standard name identifier
- Unit of measurement
- Detailed description
- Related tags and categories

## Contributing

Contributions are welcome! To add or update standard names:

1. Add or edit YAML files in the appropriate `standard_names/` subdirectory
2. Follow the existing format for consistency
3. Submit a pull request with your changes

## Building Documentation

The documentation is automatically built and deployed via GitHub Actions when changes are pushed to the `main` branch.

To build locally:

```bash
mkdocs build
```

## License

This project documents standard names for the WEST tokamak facility.

## Contact

For questions or suggestions, please [open an issue](https://github.com/west-standard-names/west-standard-names/issues).
