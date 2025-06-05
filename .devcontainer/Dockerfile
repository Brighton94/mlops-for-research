FROM python:3.11-bookworm

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Switch to non-root user
USER $USERNAME
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Install Python packages using uv and pyproject.toml
WORKDIR /workspace
COPY pyproject.toml .
RUN uv pip install --system -e ".[dev]"

# Set up DVC
RUN dvc config --global core.analytics false

# Set up MLflow
ENV MLFLOW_TRACKING_URI=http://localhost:5000

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"] 