FROM python:3.11.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libspatialindex-dev \
    build-essential \
    libpq-dev \
    libgeos-dev \
    libproj-dev \
    proj-data \
    proj-bin \
    libgdal-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir \
    networkx==3.2.1 \
    folium==0.15.1 \
    numpy==1.26.3 \
    osmnx==1.9.1 \
    geopandas==0.14.3 \
    matplotlib==3.8.2

CMD ["bash"]
