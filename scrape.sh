#!/bin/bash

# Activate the virtual environment
source /home/DickiData/edl-webscraping/env/bin/activate

# Navigate to the project directory
cd /home/DickiData/edl-webscraping/websoket_fol

# Start the Gunicorn server with Uvicorn worker
python scrape.py