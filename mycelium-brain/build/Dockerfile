# Mycelium Brain Docker Image
# Distributes the custom mycelium-brain:latest model with Ollama

FROM ollama/ollama:latest

# Set up working directory
WORKDIR /app

# Copy Modelfile for reference
COPY Modelfile /app/Modelfile

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# Expose Ollama port
EXPOSE 11434

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
