FROM python:3.12-slim
USER root
WORKDIR /app
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY /src .