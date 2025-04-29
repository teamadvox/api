# Step 1: Use an official Python image as a base
FROM python:3.11-slim

# Step 2: Install Tesseract and other required dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the requirements.txt to the working directory
COPY requirements.txt .

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the entire app into the working directory
COPY . .

# Step 7: Expose the port that Render has configured for your app
EXPOSE 10000

# Step 8: Run the FastAPI app with Uvicorn on port 10000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
