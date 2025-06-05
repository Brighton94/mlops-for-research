"""Physics-Informed Neural Network (PINN) utilities."""

import torch
import torch.nn as nn
from typing import Tuple, Optional


class PINN(nn.Module):
    """Physics-Informed Neural Network implementation."""
    
    def __init__(
        self,
        input_dim: int,
        hidden_layers: list[int],
        output_dim: int,
        activation: nn.Module = nn.Tanh(),
    ):
        """Initialize PINN model.
        
        Args:
            input_dim: Dimension of input features
            hidden_layers: List of neurons in each hidden layer
            output_dim: Dimension of output
            activation: Activation function to use
        """
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_layers:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                activation
            ])
            prev_dim = hidden_dim
            
        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network."""
        return self.network(x)
    
    def compute_derivatives(
        self,
        x: torch.Tensor,
        order: int = 1
    ) -> torch.Tensor:
        """Compute derivatives of the network output with respect to input.
        
        Args:
            x: Input tensor
            order: Order of derivative to compute
            
        Returns:
            Tensor containing the derivatives
        """
        x.requires_grad_(True)
        y = self.forward(x)
        
        if order == 1:
            return torch.autograd.grad(
                y, x,
                grad_outputs=torch.ones_like(y),
                create_graph=True
            )[0]
        else:
            raise NotImplementedError("Higher order derivatives not implemented yet")


def create_training_data(
    n_points: int,
    x_range: Tuple[float, float],
    t_range: Tuple[float, float],
    device: Optional[torch.device] = None
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Create training data points for the PINN.
    
    Args:
        n_points: Number of points to generate
        x_range: Range of x values (min, max)
        t_range: Range of t values (min, max)
        device: Device to place tensors on
        
    Returns:
        Tuple of (x, t) tensors
    """
    x = torch.linspace(x_range[0], x_range[1], n_points, device=device)
    t = torch.linspace(t_range[0], t_range[1], n_points, device=device)
    return x, t


def wave_equation_residual(
    model: PINN,
    x: torch.Tensor,
    t: torch.Tensor,
    c: float = 1.0
) -> torch.Tensor:
    """Compute the residual of the wave equation.
    
    The wave equation is: u_tt = c^2 * u_xx
    
    Args:
        model: PINN model
        x: Spatial coordinates
        t: Temporal coordinates
        c: Wave speed
        
    Returns:
        Residual of the wave equation
    """
    # Combine inputs
    inputs = torch.stack([x, t], dim=1)
    
    # Compute first derivatives
    u_t = model.compute_derivatives(inputs)
    u_x = model.compute_derivatives(inputs)
    
    # Compute second derivatives
    u_tt = model.compute_derivatives(inputs)
    u_xx = model.compute_derivatives(inputs)
    
    # Compute residual
    residual = u_tt - (c**2) * u_xx
    return residual 