# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Command to run the app
ENTRYPOINT ["streamlit", "run", "kenya_optimizer_pro.py", "--server.port=8501", "--server.address=0.0.0.0"]
