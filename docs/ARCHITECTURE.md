# Architecture

## System Overview

IBM Blueboard: Microservices architecture with 3 independent services.

```
Frontend (React:3000) → Backend (FastAPI:8000) → Database (PostgreSQL:5432)
```

## Stack

| Layer     | Technology                   | Purpose                              |
| --------- | ---------------------------- | ------------------------------------ |
| Frontend  | React 18 + Vite + IBM Carbon | UI with data visualizations          |
| Backend   | FastAPI + SQLAlchemy         | REST API and business logic          |
| Database  | PostgreSQL 18                | Data persistence (7 tables, 3 views) |
| Container | Podman                       | Service isolation                    |

## Frontend Structure

```
components/
├── ui/              # PageHeader, LoadingState, ErrorState, Settings components
├── data-display/    # StatCard, DataTableWrapper, AlertSection, AlertCard, TopPromotionsROI, TopReturnReasons
├── dashboard/       # KPITile, RechartsWidget, InfoTile, DraggableDashboardGrid
└── layout/          # AppLayout, Navigation

pages/               # 10 pages (Dashboard, Products, Sales, Customers, Satisfaction, Analytics, Settings, Inventory, Promotions, Returns)
styles/              # SCSS with themes (g10/g100), utilities, components
store/               # AppStore, ThemeStore (with scroll/pagination preservation), SettingsStore, CacheStore
config/              # dashboardConfig, settingsConfig, app.config (centralized exports via index.js)
contexts/            # ThemeContext, SettingsContext
hooks/               # useDashboardData, useTheme, useFetchData (centralized exports via index.js)
services/
└── api/             # Domain-driven API modules (analytics, products, sales, customers, satisfaction, inventory, promotions, returns, system)
```

**Key Libraries:**

- `@carbon/react` - Design system
- `recharts` - Data visualization
- `react-router-dom` - Routing
- `axios` - HTTP client
- `react-grid-layout` - Draggable dashboard

## Backend Structure

```
app/
├── models/      # SQLAlchemy ORM (7 models)
├── schemas/     # Pydantic schemas for validation
├── services/    # Business logic layer
├── routers/     # API endpoints (9 routers)
├── config.py    # Configuration
├── database.py  # DB connection
├── startup.py   # Startup events
└── main.py      # FastAPI app

tests/           # 128 tests with 100% coverage
├── models/      # Model tests
├── schemas/     # Schema validation tests
├── services/    # Service layer tests
└── routers/     # API endpoint tests
```

**API Endpoints:**

- `/api/v1/analytics` - Dashboard KPIs, trends, quick stats
- `/api/v1/products` - Product catalog
- `/api/v1/sales` - Sales transactions
- `/api/v1/customers` - Customer data
- `/api/v1/satisfaction` - Reviews
- `/api/v1/inventory` - Inventory with alerts
- `/api/v1/promotions` - Promotions with ROI
- `/api/v1/returns` - Returns with analysis
- `/api/v1/system` - System information

## Database Schema

**Tables:** products, customers, sales, satisfaction, inventory, returns, promotions  
**Views:** product_performance, customer_lifetime_value, monthly_sales_summary

See `DATABASE.md` for details.

## Environment Variables

**Root (.env):**

```env
DATABASE_URL=postgresql://user:pass@database:5432/blueboard
CORS_ORIGINS=["http://localhost:3000"]
VITE_API_URL=http://localhost:8000/api/v1
```

## Podman Network

Services communicate via `blueboard-network`:

- Frontend → Backend: `http://backend:8000`
- Backend → Database: `postgresql://database:5432`

## Development

**With Makefile (recommended):**

```bash
make start              # Start all services
make generate-data      # Generate test data
make test               # Run 128 tests (100% coverage)
make organize-imports   # Organize code imports
make logs               # View logs
make stop               # Stop services
```

**Code Quality:**

- **Frontend:** ESLint with import organization (auto-fix on save)
- **Backend:** isort + autoflake for import management
- **Testing:** 128 tests with 100% code coverage
- **VS Code:** Auto-organize imports configured in `.vscode/settings.json`

**Access:**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

## Deployment

**Development:** `make start` or `podman compose up -d`
**Production:** Use Gunicorn+Uvicorn, Nginx reverse proxy, SSL, secrets management
