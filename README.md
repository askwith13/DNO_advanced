# CDST Diagnostic Network Optimization Platform

## Overview

A comprehensive web-based diagnostic network optimization platform that intelligently allocates Culture and Drug Sensitivity Testing (CDST) laboratory resources, optimizes test distributions, and minimizes operational costs while maximizing accessibility and utilization across healthcare networks.

**Developed by PATH** - An international organization dedicated to advancing health equity worldwide.

## Key Features

- **Multi-Objective Optimization**: Balances distance, time, cost, utilization, and accessibility
- **Interactive Visualization**: Geographic mapping and analytics dashboards
- **Flexible Input System**: Support for CSV, Excel, and JSON data formats
- **Real-time Optimization**: Dynamic reallocation based on changing conditions
- **Comprehensive Reporting**: Executive summaries and implementation guides

## Technical Stack

- **Frontend**: Streamlit (Python-based web framework)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with PostGIS for geospatial data
- **Optimization**: OR-Tools (Google's optimization library)
- **Mapping**: Leaflet with OpenStreetMap
- **Routing**: OpenStreetMap Routing API with Haversine fallback

## Project Structure

```
cdst-optimization-platform/
├── docs/                           # Documentation
│   ├── technical-requirements.md
│   ├── api-specifications.md
│   ├── user-stories.md
│   └── implementation-roadmap.md
├── backend/                        # FastAPI backend
│   ├── app/
│   ├── models/
│   ├── services/
│   └── requirements.txt
├── frontend/                       # Streamlit frontend
│   ├── pages/
│   ├── components/
│   └── requirements.txt
├── database/                       # Database schemas and migrations
├── optimization/                   # Optimization algorithms
├── data/                          # Sample data and templates
└── deployment/                    # Docker and deployment configs
```

## Quick Start

1. Clone the repository
2. Set up the development environment
3. Install dependencies
4. Run the application

Detailed setup instructions are provided in the implementation roadmap.

## License

Copyright © 2024 PATH. All rights reserved.
