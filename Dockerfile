# ------------------------------------------
# 🧠 Dockerfile - LangGraph + Neo4j + Ollama
# ------------------------------------------
FROM python:3.11-slim

# Crear usuario no root
RUN adduser --disabled-password --gecos "" appuser
USER appuser
WORKDIR /app

# Copiar archivos del proyecto
COPY --chown=appuser:appuser . /app

# Instalar dependencias del sistema (para neo4j y compilación)
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
USER appuser

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Variables por defecto (puedes sobreescribir con docker-compose)
ENV NEO4J_URI=bolt://neo4j:7687
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=neo4j_pass
ENV OLLAMA_MODEL=llama3:8b
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV PYTHONUNBUFFERED=1

# Puerto (por si más adelante agregas API o UI)
EXPOSE 8000

# Comando por defecto: ejecutar prueba con pregunta
CMD ["python", "-m", "src.main", "¿Cómo seleccionar ETFs según perfil, producto y operativa?"]
