#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PYTHON_VERSION=3.11
DB_FILE="blog.db"

# Check the Python version if it's newer than `PYTHON_VERSION`, if not, exit.
if [[ "$(python3 --version | awk '{print $2}')" < "$PYTHON_VERSION" ]]; then
    echo -e "${RED}Python version must be at least $PYTHON_VERSION${NC}"
    exit 1
fi

# Create the virtual environment if it does not exist.
if [ ! -d "env" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv env
else
    echo -e "${GREEN}Virtual environment already exists, do nothing${NC}"
fi

# Activate the virtual environment and install the dependencies.
source ./env/bin/activate
pip3 install -Uq pip
pip3 install -qr requirements.txt

# Init the database if it does not exist.
if [ ! -f "$DB_FILE" ]; then
    echo -e "${GREEN}Creating database...${NC}"
    python3 init_db.py
else
    echo -e "${GREEN}Database already exists, do nothing${NC}"
fi

# Check and assign the port number.
if [ -z "$1" ]; then
    echo -e "${GREEN}No port number provided, using default port 8080${NC}"
    PORT=8080
else
    PORT=$1
fi

# Run the server.
echo -e "${GREEN}Running the server...${NC}"
set -x
python3 run.py --port=$PORT
