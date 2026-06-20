FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir aiogram google-generativeai moviepy
CMD ["python", "bot.py"]
