# Docker command to build the application
docker build -t flask-receipt-app .
# Docker command to run the application
docker run -p 5001:5001 flask-receipt-app