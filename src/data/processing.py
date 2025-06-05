"""Generic data processing module for research projects."""

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


class DataProcessor:
    """Generic data processor for research projects."""

    def __init__(
        self,
        data_dir: str | Path,
        output_dir: str | Path,
        config: dict[str, Any] | None = None,
    ):
        """Initialize the data processor.

        Args:
            data_dir: Directory containing the input data.
            output_dir: Directory to save processed data.
            config: Optional configuration dictionary.

        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config or {}

    def load_data(self, file_pattern: str = "*.csv") -> pd.DataFrame:
        """Load data from files matching the pattern.

        Args:
            file_pattern: Glob pattern to match data files.

        Returns:
            pd.DataFrame: Combined data from all matching files.

        """
        data_files = list(self.data_dir.glob(file_pattern))
        if not data_files:
            raise FileNotFoundError(f"No files found matching pattern: {file_pattern}")

        dfs = []
        for file in data_files:
            try:
                df = pd.read_csv(file)
                dfs.append(df)
                logger.info(f"Loaded data from {file}")
            except Exception as e:
                logger.error(f"Error loading {file}: {str(e)}")
                continue

        if not dfs:
            raise ValueError("No data could be loaded from any files")

        return pd.concat(dfs, ignore_index=True)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the input data.

        Args:
            df: Input DataFrame.

        Returns:
            pd.DataFrame: Cleaned DataFrame.

        """
        # Remove duplicate rows
        df = df.drop_duplicates()

        # Handle missing values
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])

        return df

    def split_data(
        self,
        df: pd.DataFrame,
        target_col: str | None = None,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42,
    ) -> dict[str, pd.DataFrame]:
        """Split data into train, validation, and test sets.

        Args:
            df: Input DataFrame.
            target_col: Column to use for stratified splitting.
            test_size: Proportion of data to use for testing.
            val_size: Proportion of data to use for validation.
            random_state: Random seed for reproducibility.

        Returns:
            Dict containing train, validation, and test DataFrames.

        """
        # First split: train and temp
        train_df, temp_df = train_test_split(
            df,
            test_size=test_size + val_size,
            random_state=random_state,
            stratify=df[target_col] if target_col else None,
        )

        # Second split: validation and test
        val_ratio = val_size / (test_size + val_size)
        val_df, test_df = train_test_split(
            temp_df,
            test_size=1 - val_ratio,
            random_state=random_state,
            stratify=temp_df[target_col] if target_col else None,
        )

        return {"train": train_df, "val": val_df, "test": test_df}

    def save_data(self, data_dict: dict[str, pd.DataFrame], prefix: str = ""):
        """Save processed data to files.

        Args:
            data_dict: Dictionary of DataFrames to save.
            prefix: Optional prefix for output filenames.

        """
        for name, df in data_dict.items():
            output_file = self.output_dir / f"{prefix}{name}.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"Saved {name} data to {output_file}")

    def process_pipeline(
        self,
        file_pattern: str = "*.csv",
        target_col: str | None = None,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42,
    ) -> dict[str, pd.DataFrame]:
        """Run the complete data processing pipeline.

        Args:
            file_pattern: Glob pattern to match data files.
            target_col: Column to use for stratified splitting.
            test_size: Proportion of data to use for testing.
            val_size: Proportion of data to use for validation.
            random_state: Random seed for reproducibility.

        Returns:
            Dict containing processed train, validation, and test DataFrames.

        """
        # Load data
        df = self.load_data(file_pattern)
        logger.info(f"Loaded {len(df)} rows of data")

        # Clean data
        df = self.clean_data(df)
        logger.info(f"Cleaned data: {len(df)} rows remaining")

        # Split data
        data_dict = self.split_data(
            df,
            target_col=target_col,
            test_size=test_size,
            val_size=val_size,
            random_state=random_state,
        )

        # Save processed data
        self.save_data(data_dict)

        return data_dict
