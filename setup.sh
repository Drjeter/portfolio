#!/bin/bash

echo "🚀 Django Portfolio Setup Script"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    
    # Update .env with generated secret key (works on both macOS and Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/your-secret-key-here/$SECRET_KEY/" .env
    else
        sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
    fi
    
    echo "✓ .env file created with generated SECRET_KEY"
    echo ""
    echo "⚠️  IMPORTANT: Update .env file with your database credentials!"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p static/css static/js static/images
mkdir -p media/projects media/blog
mkdir -p staticfiles

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Update .env with your PostgreSQL database URL"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Collect static files: python manage.py collectstatic"
echo "4. Run the development server: python manage.py runserver"
echo ""
echo "Visit http://localhost:8000 to see your portfolio!"
echo "Admin panel: http://localhost:8000/admin"
echo ""
