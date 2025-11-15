FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy your project files to /app
COPY . .

# Install system deps if needed
RUN apt-get update && apt-get install -y ffmpeg

# Install Python libs
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python", "main.py"]
