"""Tests for the data processing module."""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data.processing import DataProcessor


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
        "feature1": [1, 2, np.nan, 4, 5],
        "feature2": ["a", "b", "c", np.nan, "e"],
        "target": [0, 1, 0, 1, 0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = Path(temp_dir) / "input"
        output_dir = Path(temp_dir) / "output"
        input_dir.mkdir()
        output_dir.mkdir()
        yield input_dir, output_dir


def test_data_processor_initialization(temp_dirs):
    """Test DataProcessor initialization."""
    input_dir, output_dir = temp_dirs
    processor = DataProcessor(input_dir, output_dir)
    assert processor.data_dir == input_dir
    assert processor.output_dir == output_dir
    assert isinstance(processor.config, dict)


def test_load_data(temp_dirs, sample_data):
    """Test loading data from files."""
    input_dir, _ = temp_dirs
    # Save sample data
    sample_data.to_csv(input_dir / "test.csv", index=False)

    processor = DataProcessor(input_dir, temp_dirs[1])
    loaded_data = processor.load_data("*.csv")

    assert isinstance(loaded_data, pd.DataFrame)
    assert len(loaded_data) == len(sample_data)
    assert all(col in loaded_data.columns for col in sample_data.columns)


def test_clean_data(sample_data):
    """Test data cleaning functionality."""
    processor = DataProcessor(Path("dummy"), Path("dummy"))
    cleaned_data = processor.clean_data(sample_data)

    assert isinstance(cleaned_data, pd.DataFrame)
    assert not cleaned_data.isna().any().any()
    assert len(cleaned_data) == len(sample_data)


def test_split_data(sample_data):
    """Test data splitting functionality."""
    processor = DataProcessor(Path("dummy"), Path("dummy"))
    splits = processor.split_data(
        sample_data, target_col="target", test_size=0.4, val_size=0.2
    )

    assert isinstance(splits, dict)
    assert all(key in splits for key in ["train", "val", "test"])
    assert all(isinstance(df, pd.DataFrame) for df in splits.values())

    # Check split sizes
    total_size = len(sample_data)
    assert len(splits["train"]) == int(total_size * 0.4)
    assert len(splits["val"]) == int(total_size * 0.2)
    assert len(splits["test"]) == int(total_size * 0.4)


def test_save_data(temp_dirs, sample_data):
    """Test saving data to files."""
    _, output_dir = temp_dirs
    processor = DataProcessor(Path("dummy"), output_dir)

    data_dict = {"train": sample_data, "test": sample_data}
    processor.save_data(data_dict)

    assert (output_dir / "train.csv").exists()
    assert (output_dir / "test.csv").exists()


def test_process_pipeline(temp_dirs, sample_data):
    """Test the complete processing pipeline."""
    input_dir, output_dir = temp_dirs
    # Save sample data
    sample_data.to_csv(input_dir / "test.csv", index=False)

    processor = DataProcessor(input_dir, output_dir)
    result = processor.process_pipeline(
        file_pattern="*.csv", target_col="target", test_size=0.4, val_size=0.2
    )

    assert isinstance(result, dict)
    assert all(key in result for key in ["train", "val", "test"])
    assert all(isinstance(df, pd.DataFrame) for df in result.values())

    # Check if files were saved
    assert (output_dir / "train.csv").exists()
    assert (output_dir / "val.csv").exists()
    assert (output_dir / "test.csv").exists()


def test_error_handling(temp_dirs):
    """Test error handling in data processing."""
    input_dir, output_dir = temp_dirs
    processor = DataProcessor(input_dir, output_dir)

    # Test loading non-existent files
    with pytest.raises(FileNotFoundError):
        processor.load_data("nonexistent.csv")

    # Test processing with invalid data
    with pytest.raises(ValueError):
        processor.process_pipeline()
