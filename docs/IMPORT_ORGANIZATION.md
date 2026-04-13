# Import Organization Guide

Automated tools to organize and clean imports in IBM Blueboard.

## 🔧 Tools

**Frontend:** ESLint + eslint-plugin-import + eslint-plugin-unused-imports
**Backend:** isort + autoflake

## 📝 Usage

```bash
# Organize all imports (frontend + backend)
make organize-imports

# Frontend only
make organize-imports-frontend
cd frontend && npm run organize-imports

# Backend only
make organize-imports-backend
cd backend && python3 -m autoflake --remove-all-unused-imports --in-place --recursive app/ tests/ && python3 -m isort app/ tests/
```

## 🎨 Import Order

**Frontend (JavaScript/React):**

1. React imports
2. External packages
3. Carbon Design System (@carbon/\*)
4. Internal modules (relative imports)

**Backend (Python):**

1. Standard library
2. Third-party (FastAPI, SQLAlchemy, etc.)
3. First-party (app.\*)
4. Local (relative imports)

## 🔄 VS Code Auto-organize

Already configured in `.vscode/settings.json` - imports organize automatically on save.

## 🚀 Best Practices

- Run `make organize-imports` before committing
- Review changes to ensure no important imports were removed
- Configuration files (`.eslintrc.json`, `.isort.cfg`) are committed for team consistency
