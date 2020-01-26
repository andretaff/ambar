docker stop ambar-forecast
docker rm ambar-forecast
docker build --tag andretaff/ambar-forecast .
docker run --name ambar-forecast -p 5000:5000 andretaff/ambar-forecast




