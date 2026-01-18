FROM kivy/buildozer:latest

# Create a non-root user
RUN useradd -m -s /bin/bash builduser && \
    chown -R builduser:builduser /home/builduser && \
    mkdir -p /app && \
    chown -R builduser:builduser /app

# Set working directory
WORKDIR /app

# Switch to non-root user
USER builduser

# Set environment variables
ENV PATH="/home/builduser/.local/bin:$PATH"

# Command to run buildozer
CMD ["buildozer", "android", "debug"]