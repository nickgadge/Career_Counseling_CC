# 1. Use a lightweight Python image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy all files into the container
COPY . /app

# 4. Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Expose port 5000
EXPOSE 5000

# 6. Start Flask using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
