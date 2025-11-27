#!/bin/bash
# Remote deployment script - run this on the server

set -e

echo "🚀 Starting remote deployment..."

# Update system
echo "📦 Updating system..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker installed. Please log out and log back in."
    exit 0
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw --force enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "⚠️  .env.production not found. Creating from example..."
    if [ -f .env.production.example ]; then
        cp .env.production.example .env.production
        echo "📝 Please edit .env.production and fill in required values:"
        echo "   - SECRET_KEY"
        echo "   - TELEGRAM_BOT_TOKEN"
        echo "   - POSTGRES_PASSWORD"
        echo ""
        echo "Then run this script again."
        exit 1
    else
        echo "❌ .env.production.example not found!"
        exit 1
    fi
fi

# Build React app (will be built in Docker)
echo "📦 React app will be built in Docker container..."

# Build and start Docker containers
echo "🐳 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

echo "🚀 Starting containers..."
docker-compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to start..."
sleep 15

# Check service status
echo "📊 Service status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Services available at:"
echo "  - Frontend: http://194.110.54.230/"
echo "  - API: http://194.110.54.230/api/"
echo "  - Admin: http://194.110.54.230/admin/"
echo ""
echo "To view logs: docker-compose -f docker-compose.prod.yml logs -f"

