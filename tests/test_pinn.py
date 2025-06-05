"""Tests for PINN implementation."""

import pytest
import torch
import numpy as np
from src.pinn.pinn_utils import PINN, create_training_data, wave_equation_residual


@pytest.fixture
def model():
    """Create a test PINN model."""
    return PINN(
        input_dim=2,
        hidden_layers=[10, 10],
        output_dim=1
    )


def test_pinn_initialization():
    """Test PINN model initialization."""
    model = PINN(
        input_dim=2,
        hidden_layers=[10, 10],
        output_dim=1
    )
    
    # Check if model is instance of nn.Module
    assert isinstance(model, torch.nn.Module)
    
    # Check if network has correct number of layers
    expected_layers = 5  # 2 hidden layers * 2 (linear + activation) + 1 output layer
    assert len(model.network) == expected_layers


def test_pinn_forward(model):
    """Test PINN forward pass."""
    batch_size = 10
    x = torch.randn(batch_size, 2)
    output = model(x)
    
    # Check output shape
    assert output.shape == (batch_size, 1)
    
    # Check if output is tensor
    assert isinstance(output, torch.Tensor)


def test_compute_derivatives(model):
    """Test derivative computation."""
    batch_size = 10
    x = torch.randn(batch_size, 2, requires_grad=True)
    
    # Compute first derivative
    derivative = model.compute_derivatives(x)
    
    # Check derivative shape
    assert derivative.shape == (batch_size, 2)
    
    # Check if derivative is tensor
    assert isinstance(derivative, torch.Tensor)


def test_create_training_data():
    """Test training data creation."""
    n_points = 100
    x_range = (-1, 1)
    t_range = (0, 1)
    
    x, t = create_training_data(n_points, x_range, t_range)
    
    # Check shapes
    assert x.shape == (n_points,)
    assert t.shape == (n_points,)
    
    # Check ranges
    assert torch.all(x >= x_range[0]) and torch.all(x <= x_range[1])
    assert torch.all(t >= t_range[0]) and torch.all(t <= t_range[1])


def test_wave_equation_residual(model):
    """Test wave equation residual computation."""
    n_points = 10
    x = torch.randn(n_points, device=model.network[0].weight.device)
    t = torch.randn(n_points, device=model.network[0].weight.device)
    
    residual = wave_equation_residual(model, x, t)
    
    # Check residual shape
    assert residual.shape == (n_points,)
    
    # Check if residual is tensor
    assert isinstance(residual, torch.Tensor) 