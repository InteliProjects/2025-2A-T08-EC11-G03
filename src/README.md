# Animal Data API

This directory contains a FastAPI application for animal telemetry data with InfluxDB backend and Jupyter notebooks for data analysis.

## Requirements

-   Python 3.12+
-   [UV](https://docs.astral.sh/uv/) package manager

## Setup

1. Initialize the virtual environment and install dependencies:

```bash
make venv
```

## Usage

### Running the FastAPI Application

```bash
make run
```

The API will be available at `http://localhost:5000`

### Starting Jupyter Notebooks

To work with the notebooks, activate the virtual environment first:

```bash
source .venv/bin/activate
jupyter notebook
```

Or run directly with UV:

```bash
uv run jupyter notebook
```

### Available Commands

-   `make venv` - Initialize virtual environment and sync dependencies
-   `make run` - Run the FastAPI application
-   `make help` - Show all available commands

## Project Structure

-   `app/` - FastAPI application code
    -   `main.py` - Application entry point
    -   `controllers/` - API route handlers
    -   `services/` - Business logic
    -   `repositories/` - Data access layer
    -   `config/` - Configuration management
    -   `utils/` - Utility functions
-   `*.ipynb` - Jupyter notebooks for data analysis
-   `.venv/` - UV virtual environment (auto-generated)

## Environment Variables

Create a `.env` file in the project root with your InfluxDB configuration:

```
INFLUX_URL=your_influx_url
INFLUX_ORG=your_org
INFLUX_BUCKET=your_bucket
INFLUX_TOKEN=your_token
```

## API Endpoints

-   `GET /` - Health check
-   `GET /api/animals/all` - Get all animal telemetry data
