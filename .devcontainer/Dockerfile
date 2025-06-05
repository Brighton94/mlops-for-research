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

# Switch to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Install Python packages
WORKDIR /workspace
COPY pyproject.toml ../README.md ./
RUN pip install --no-cache-dir ".[dev]"

# Install DVC and configure it
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
RUN pip install --no-cache-dir "dvc[all]>=3.59.0" && \
    dvc config --global core.analytics false && \
    echo 'export PATH="/home/${USERNAME}/.local/bin:$PATH"' >> /home/${USERNAME}/.bashrc

# Set up MLflow
ENV MLFLOW_TRACKING_URI=/workspace/mlruns

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"] 