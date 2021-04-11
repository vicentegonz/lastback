# Environment setter image
FROM python:3.8-slim-buster AS environment

# Receive DJANGO_ENV as a build arg, default to production
ARG DJANGO_ENV=production

# Set up environmental variables
ENV DJANGO_ENV=${DJANGO_ENV} \
    LANG=C.UTF-8 \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.1.5

# Set up base workdir
WORKDIR /app

# Install OS package dependencies
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    # Install poetry
    pip install "poetry==$POETRY_VERSION"

# Setup the virtualenv
RUN python -m venv /venv

# Copy project dependency files to image
COPY pyproject.toml poetry.lock ./

# Export and install all the dependencies pip
# (this allows for the virtual environment to be used correctly)
RUN poetry export --format requirements.txt --output fulldependencies.txt && \
    /venv/bin/pip install --requirement fulldependencies.txt && \
    rm fulldependencies.txt

# --------------------------------------------------------

# Final image
FROM python:3.8-slim-buster AS final

# Receive DJANGO_ENV as a build arg, default to production
ARG DJANGO_ENV=production

# Set up environmental variables
ENV DJANGO_ENV=${DJANGO_ENV} \
    LANG=C.UTF-8

# Set up base workdir
WORKDIR /app

# Get virtual environment
COPY --from=environment /venv /venv

# Use executables from the virtual env
ENV PATH="/venv/bin:$PATH"

# Copy files to image
COPY . .

# Add a script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

# Run as non-root user
RUN useradd -m nonrootuser
USER nonrootuser

# Start the main process.
CMD ["/bin/bash", "./run.sh"]
