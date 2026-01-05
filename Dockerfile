FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/app/
COPY scripts/ /app/scripts/
COPY sample_prs/ /app/sample_prs/
COPY app/templates/ /app/app/templates/

# Expose port
EXPOSE 80

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
