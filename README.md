# IBM Blueboard

> Data visualization dashboard for cosmetics industry analytics

[![React](https://img.shields.io/badge/React-18-61dafb?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql)](https://www.postgresql.org/)

## Overview

Microservices dashboard for analyzing cosmetics sales and customer satisfaction with interactive visualizations.

**Features:**

- Real-time KPIs (revenue, sales, satisfaction, basket)
- Interactive charts with drag & drop layout
- Product, customer, and sales analytics
- RESTful API with auto-docs
- Fully containerized with Docker/Podman

## Quick Start

### Prerequisites

**macOS:**

```bash
brew install git make podman podman-compose
podman machine init && podman machine start
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install -y git make podman podman-compose
systemctl --user enable --now podman.socket
```

**Windows:** Use WSL2 + Ubuntu or [Podman Desktop](https://podman-desktop.io/)

### Installation (4 steps)

```bash
# 1. Clone and configure
git clone <repository-url>
cd ibm-blueboard
cp .env.example .env

# 2. Start services (wait ~30s)
make start

# 3. Generate test data
make generate-data

# 4. Open browser
open http://localhost:3000
```

**Access:**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Usage

### Essential Commands

```bash
make start            # Start all services
make stop             # Stop all services
make logs             # View logs
make status           # Check services
make test             # Run backend tests
make help             # Show all commands
make organize-imports # Organize imports (frontend + backend)
make format           # Format all code (frontend, backend, database, config)
```

### Development

```bash
make dev                        # Start with live logs
make shell-backend              # Access backend shell
make shell-database             # Access PostgreSQL shell
make generate-data              # Regenerate test data
make clean                      # Clean everything
make format-frontend            # Format frontend code with Prettier
make format-backend             # Format backend code with Black
make format-database            # Format SQL files with pg_format
make format-config              # Format docker-compose and Markdown files
make organize-imports-frontend  # Organize frontend imports
make organize-imports-backend   # Organize backend imports
```

## Tech Stack

| Layer        | Technology                                            |
| ------------ | ----------------------------------------------------- |
| Frontend     | React 18 + Vite + IBM Carbon Design System + Recharts |
| Backend      | FastAPI + SQLAlchemy + Pydantic                       |
| Database     | PostgreSQL 18 (7 tables, 3 views)                     |
| Container    | Docker/Podman                                         |
| Testing      | Pytest (128 tests, 100% coverage)                     |
| Code Quality | ESLint + isort + autoflake                            |

## API Endpoints

**Analytics:**

- `GET /api/v1/analytics/dashboard` - Dashboard KPIs with trends
- `GET /api/v1/analytics/kpi-trends` - Historical KPI data
- `GET /api/v1/analytics/quick-stats` - Quick statistics
- `GET /api/v1/analytics/sales-trends` - Sales over time
- `GET /api/v1/analytics/top-products` - Best sellers
- `GET /api/v1/analytics/category-distribution` - Category breakdown
- `GET /api/v1/analytics/satisfaction-stats` - Satisfaction metrics
- `GET /api/v1/analytics/regional-performance` - Regional analysis

**Resources:**

- `GET /api/v1/products` - Products catalog
- `GET /api/v1/sales` - Sales transactions
- `GET /api/v1/customers` - Customer data
- `GET /api/v1/satisfaction` - Customer reviews
- `GET /api/v1/inventory` - Inventory with low stock alerts
- `GET /api/v1/promotions` - Promotions with ROI analysis
- `GET /api/v1/returns` - Returns with reason analysis

**System:**

- `GET /api/v1/system/info` - System information

Full interactive docs: http://localhost:8000/docs

## Data Model

Generated with Faker:

- **100 products** (6 categories: Skincare, Makeup, Haircare, Fragrance, Body Care, Tools)
- **500 customers** (5 segments: VIP, Premium, Regular, Occasional, New)
- **2,500 sales** (18 months history)
- **1,200 reviews** (multi-criteria satisfaction)
- **100 inventory** records
- **30 promotions**
- **150 returns**

## Testing

```bash
make test              # Run all 128 tests
make test-verbose      # Verbose output
make test-coverage     # Coverage report (100%)
```

**Test suite:**

- 128 tests with 100% code coverage
- Schema validation (Pydantic)
- Service layer (business logic)
- Router tests (API endpoints)
- Model tests (SQLAlchemy)
- Isolated test database (`blueboard_test`)

## Local Development (without containers)

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Documentation

- [Architecture](./docs/ARCHITECTURE.md) - System design & patterns
- [Cache](./docs/CACHE.md) - Caching strategy
- [Data Generation](./docs/DATA_GENERATION.md) - Test data details
- [Database](./docs/DATABASE.md) - Schema & relationships
- [Import Organization](./docs/IMPORT_ORGANIZATION.md) - Code organization tools

## Make Commands Reference

```bash
# Service Management
make start              # Start all services
make stop               # Stop all services
make restart            # Restart all services
make status             # Show services status
make dev                # Start with live logs

# Logs
make logs               # All services logs
make logs-backend       # Backend logs only
make logs-frontend      # Frontend logs only
make logs-database            # Database logs only

# Build & Clean
make build              # Rebuild all containers
make build-backend      # Rebuild backend only
make build-frontend     # Rebuild frontend only
make clean              # Stop and remove everything

# Development
make shell-backend      # Backend container shell
make shell-frontend     # Frontend container shell
make shell-database     # PostgreSQL shell
make generate-data      # Generate test data
make clear-data         # Clear all data

# Testing
make test               # Run backend tests (128 tests)
make test-verbose       # Tests with verbose output
make test-coverage      # Tests with coverage report (100%)

# Code Quality
make organize-imports           # Organize all imports
make organize-imports-frontend  # Frontend imports only
make organize-imports-backend   # Backend imports only

# Utilities
make help               # Show all commands
make setup              # Setup Podman machine
```

## License

MIT

---

**Version**: 2.0.0 | **Status**: Production Ready
