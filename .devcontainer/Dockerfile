##############
# Base image #
##############
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-24.04
ENV NODE_VERSION=24.1.0

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    # general stuff
    sudo git bash unattended-upgrades curl vim clang zip \
    # postgres stuff
    libpq-dev postgresql-client

ENV EDITOR=vim
ARG CONTAINER_USER=vscode

# Install uv for python versioning and deps
COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /bin/uv
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

ENV NVM_DIR="/opt/nvm"
RUN mkdir $NVM_DIR
# prepend node to path
ENV PATH="$NVM_DIR/versions/node/v${NODE_VERSION}/bin/:${PATH}"

# install nvm and current node
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R ${CONTAINER_USER} /commandhistory \
    && echo "$SNIPPET" >> "/home/${CONTAINER_USER}/.bashrc"

USER $CONTAINER_USER
