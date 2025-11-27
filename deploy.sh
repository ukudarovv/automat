#!/bin/bash

# Deployment script for AvtoMat

set -e

echo "🚀 Starting deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo -e "${RED}Error: .env.production file not found!${NC}"
    echo "Please create .env.production with required variables:"
    echo "  - SECRET_KEY"
    echo "  - TELEGRAM_BOT_TOKEN"
    echo "  - POSTGRES_PASSWORD"
    echo "  - MINI_APP_URL"
    exit 1
fi

# Load environment variables
export $(cat .env.production | grep -v '^#' | xargs)

echo -e "${YELLOW}📦 Building Docker images...${NC}"
docker-compose -f docker-compose.prod.yml build

echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker-compose -f docker-compose.prod.yml down

echo -e "${YELLOW}🚀 Starting containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d

echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

echo -e "${YELLOW}📊 Checking service status...${NC}"
docker-compose -f docker-compose.prod.yml ps

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Services are running:"
echo "  - Backend API: http://194.110.54.230/api/"
echo "  - Frontend: http://194.110.54.230/"
echo "  - Admin: http://194.110.54.230/admin/"
echo ""
echo "To view logs: docker-compose -f docker-compose.prod.yml logs -f"

