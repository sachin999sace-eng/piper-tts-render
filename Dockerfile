FROM rhasspy/piper:latest

# Minimal Python + Flask runtime for the HTTP API
RUN apt-get update \
 && apt-get install -y python3 python3-pip curl \
 && pip3 install --no-cache-dir flask waitress \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY server.py /app/server.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh && mkdir -p /app/models

# Where the voice model & config will live
ENV PIPER_MODEL=/app/models/model.onnx
ENV PIPER_CONFIG=/app/models/model.onnx.json
ENV PORT=5000

EXPOSE 5000
CMD ["/app/start.sh"]
