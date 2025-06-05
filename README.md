# MLOps for Research

A template repository for implementing MLOps practices in research projects. This repository provides a structured approach to data exploration, preparation, and benchmarking in research settings.

## Features

- 📊 **Data Exploration**: Jupyter notebooks for exploratory data analysis
- 🔄 **Data Preparation**: ETL pipelines for research data
- ⚡ **Benchmarking**: Tools for performance benchmarking
- 🧪 **Testing**: Unit tests for research code
- 📈 **Documentation**: Clear documentation of data processing steps

## Project Structure

```
.
├── notebooks/              # Jupyter notebooks
│   ├── 01_eda_and_data_prep.ipynb
│   ├── benchmark_etl.ipynb
│   └── benchmark_vectorization.ipynb
├── src/                    # Source code
│   ├── data/              # Data processing modules
│   ├── utils/             # Utility functions
│   └── __init__.py
├── tests/                 # Test suite
│   └── test_data_processing.py
├── .devcontainer/         # Development container configuration
├── .github/              # GitHub Actions workflows
└── requirements.txt      # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.11+
- Jupyter Notebook
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mlops-for-research.git
   cd mlops-for-research
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Data Exploration**:
   - Open `notebooks/01_eda_and_data_prep.ipynb` to explore your dataset
   - Use the provided functions in `src/data/` for data processing

2. **Benchmarking**:
   - Run `notebooks/benchmark_etl.ipynb` to benchmark your ETL pipeline
   - Use `notebooks/benchmark_vectorization.ipynb` to test vectorization performance

3. **Testing**:
   ```bash
   pytest tests/
   ```

## Development

### Adding New Features

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Add tests in `tests/`
3. Implement the feature in `src/`
4. Run tests:
   ```bash
   pytest
   ```

### Code Quality

- Format code:
  ```bash
  ruff format .
  ```

- Lint code:
  ```bash
  ruff check .
  ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 