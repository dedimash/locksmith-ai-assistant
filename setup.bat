@echo off
REM Create necessary directories
mkdir call_logs
mkdir logs
mkdir website\static

REM Display instructions
echo === Locksmith AI Assistant Setup ===
echo Directories created successfully.
echo Starting Docker containers...

REM Start Docker containers
docker-compose up -d

REM Check if containers are running
echo Checking if containers are running...
docker ps | findstr locksmith-ai-assistant

echo.
echo === Setup Complete ===
echo You can access the Locksmith AI Assistant at: http://localhost:5000
echo.
echo To view logs, run: docker-compose logs -f
echo To stop the service, run: docker-compose down
