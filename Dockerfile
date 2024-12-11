FROM --platform=linux/amd64 ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Africa/Lagos

# Set environment variables using ARGs
ENV DATABASE_USER=doadmin
ENV DATABASE_PASSWORD=AVNS_dyy_KmcQ6bdSrMRWR21
ENV DATABASE_HOST=skyeyez-pg-do-user-14267660-0.a.db.ondigitalocean.com
ENV DATABASE_PORT=25060
ENV DATABASE_NAME=train-table
ENV DATABASE_SSLMODE=require

ENV KAFKA_SASL_MECHANISM=SCRAM-SHA-256
ENV KAFKA_HOST=db-kafka-nyc3-03596-do-user-14267660-0.j.db.ondigitalocean.com
ENV KAFKA_SASL_PORT=25073
ENV KAFKA_SASL_USERNAME=doadmin
ENV KAFKA_SASL_PASSWORD=AVNS_TZ0Zkn33dwQT9D8o_TI
ENV KAFKA_SECURITY_PROTOCOL=SASL_SSL
ENV GROUP_ID=consumer-queue-group

# Install software-properties-common to add PPAs
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
# Update package list
RUN apt-get update
# Install Python 3.11 and its development packages
RUN apt-get install -y python3.11 python3.11-venv python3.11-dev
# Install pip for Python 3
RUN apt-get install -y python3-pip
# Install other required packages
RUN apt-get install -y curl git make

# Create a symbolic link for python to point to python3.11
RUN ln -s /usr/bin/python3.11 /usr/bin/python

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Display environment variables for debugging
RUN echo "DATABASE_USER=${DATABASE_USER}" && \
    echo "DATABASE_PASSWORD=${DATABASE_PASSWORD}" && \
    echo "DATABASE_HOST=${DATABASE_HOST}" && \
    echo "DATABASE_PORT=${DATABASE_PORT}" && \
    echo "DATABASE_NAME=${DATABASE_NAME}" && \
    echo "DATABASE_SSLMODE=${DATABASE_SSLMODE}" && \
    echo "KAFKA_SASL_MECHANISM=${KAFKA_SASL_MECHANISM}" && \
    echo "KAFKA_HOST=${KAFKA_HOST}" && \
    echo "KAFKA_SASL_PORT=${KAFKA_SASL_PORT}" \
    echo "KAFKA_SASL_USERNAME=${KAFKA_SASL_USERNAME}" && \
    echo "KAFKA_SASL_PASSWORD=${KAFKA_SASL_PASSWORD}" && \
    echo "KAFKA_SECURITY_PROTOCOL=${KAFKA_SECURITY_PROTOCOL}" && \
    echo "GROUP_ID=${GROUP_ID}" && \
    sleep 5

# Use --ignore-installed flag to force installation
# RUN python -m pip install --upgrade pip && \
#     pip install --no-cache-dir --ignore-installed -r requirements.txt

RUN apt-get install --no-install-recommends -y python3-pip && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install PostgreSQL development libraries for pg_config
RUN apt-get update && apt-get install -y libpq-dev

COPY pyproject.toml ./

RUN pip install --ignore-installed blinker

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

ENTRYPOINT ["make", "start_prod"]