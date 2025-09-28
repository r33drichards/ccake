FROM python:3.11-slim

# Install system dependencies and MiniZinc
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install MiniZinc
ENV MINIZINC_VERSION=2.8.5
RUN wget -q https://github.com/MiniZinc/MiniZincIDE/releases/download/${MINIZINC_VERSION}/MiniZincIDE-${MINIZINC_VERSION}-x86_64.AppImage \
    && chmod +x MiniZincIDE-${MINIZINC_VERSION}-x86_64.AppImage \
    && ./MiniZincIDE-${MINIZINC_VERSION}-x86_64.AppImage --appimage-extract \
    && mv squashfs-root /opt/minizinc \
    && ln -s /opt/minizinc/usr/bin/minizinc /usr/local/bin/minizinc \
    && rm MiniZincIDE-${MINIZINC_VERSION}-x86_64.AppImage

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port if needed (adjust based on your app's needs)
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]