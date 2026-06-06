FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ ./scripts/
COPY prompts/ ./prompts/
RUN mkdir -p output logs reports
CMD ["python3", "scripts/content_generator.py"]
