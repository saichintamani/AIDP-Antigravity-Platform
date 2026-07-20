#!/bin/bash

echo "==================================================="
echo "  Starting AIDP (Artificial Intelligence Discovery Platform)  "
echo "==================================================="
echo ""
echo "Building and starting Docker containers..."
docker-compose up --build -d

echo ""
echo "==================================================="
echo "AIDP is now running in the background!"
echo "-> Interactive Research Canvas: http://localhost:3000"
echo "-> Backend API: http://localhost:8000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo "==================================================="
