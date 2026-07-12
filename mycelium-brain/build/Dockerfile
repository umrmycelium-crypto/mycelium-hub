# Mycelium Brain Docker Image
# Distributes the custom branched models

FROM ollama/ollama:latest

# Set up entrypoint
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["serve"]
