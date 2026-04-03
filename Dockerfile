# 1. Use a lightweight Python 3.10 image
FROM python:3.10-slim


RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean

# 2. Set the working directory inside the Linux container
WORKDIR /app

# 3. Create a non-root user named 'etluser' for security
# This prevents the app from having "Admin" rights inside the container
RUN groupadd -r etluser && useradd -r -g etluser etluser

# 4. Copy ONLY the requirements file first
# This makes builds faster because Docker caches this step
COPY requirements.txt .

# 5. Install Pandas, SQLAlchemy, and your DB drivers
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy your source code and data folders into the container
COPY src/ ./src/
COPY data/ ./data/

# 7. Give 'etluser' ownership of the /app folder
RUN chown -R etluser:etluser /app

# 8. Switch from 'root' to 'etluser'
USER etluser

# 9. The command to run your orchestrator when the container starts
ENTRYPOINT ["python", "src/main.py"]