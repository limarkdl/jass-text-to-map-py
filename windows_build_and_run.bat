@echo off

docker stop jass-2024-assignment-limarkdl >nul 2>&1
docker rm jass-2024-assignment-limarkdl >nul 2>&1

docker build --no-cache -t jass-2024-limarkdl .

echo.
echo.
echo.


docker run -it --name jass-2024-assignment-limarkdl -v "%cd%":/task2/ jass-2024-limarkdl

start "" "%cd%\output.png"

pause "\nPress any key to continue..."