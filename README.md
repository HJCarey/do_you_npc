# Do You NPC

An AI-powered NPC generation system for tabletop RPGs and game development, featuring a web interface and database backend for managing personas, prompts, and campaigns.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Git

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd do_you_npc
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install the package in development mode with all dependencies
pip install -e ".[dev]"
```

### 4. Database Setup
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres createdb do_you_npc
sudo -u postgres createuser jake

# Grant permissions
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE do_you_npc TO jake;"
```

### 5. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your database settings
# Default values should work for local PostgreSQL setup:
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=do_you_npc
# DB_USER=jake
# DB_PASSWORD=
```

### 6. Database Migration
```bash
# Run database migrations to set up tables
alembic upgrade head
```

### 7. Set Up Pre-commit Hooks (Optional)
```bash
# Install pre-commit hooks for code quality
pre-commit install
```

## Running the Application

### Streamlit Web Interface
```bash
streamlit run do_you_npc/app.py
```
Access the application at `http://localhost:8501`

### FastAPI Server
```bash
uvicorn do_you_npc.api.main:app --host 0.0.0.0 --port 8000 --reload
```
- API available at `http://localhost:8000`
- Interactive API docs at `http://localhost:8000/docs`

### Test Database Connection
```bash
python tests/test_database.py
```

## Development

### Code Quality Tools
```bash
# Lint and auto-fix code
ruff check --fix .

# Format code
black .

# Sort imports
isort .

# Type checking
mypy .

# Run all pre-commit hooks
pre-commit run --all-files
```

### Database Operations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Check migration status
alembic current

# Run specific migration
alembic upgrade <revision>
```

### Testing
```bash
# Basic vectorstore test
python tests/simple_test.py

# Full system demo
python tests/test_vectorstore_system.py

# Database connectivity test
python tests/test_database.py
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check database exists: `sudo -u postgres psql -l`
- Verify user permissions: `sudo -u postgres psql -c "\du"`

### Permission Errors
- Ensure your user has proper database permissions
- Check that the database user matches your system user for peer authentication

### Import Errors
- Ensure the package is installed in development mode: `pip install -e .`
- Activate your virtual environment before running commands