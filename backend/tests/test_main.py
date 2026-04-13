"""
Tests for main application module
"""

from fastapi.testclient import TestClient


class TestMainApp:
    """Tests for main FastAPI application"""

    def test_root_endpoint(self, client):
        """Test GET / endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["message"] == "Welcome to IBM Blueboard API"

    def test_health_check_endpoint(self, client):
        """Test GET /health endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "environment" in data
        assert data["status"] == "healthy"

    def test_startup_event(self, client):
        """Test that startup event is triggered"""
        # The startup event sets APP_START_TIME
        from app.startup import APP_START_TIME

        assert APP_START_TIME is not None
        # Make a request to ensure app is running
        response = client.get("/api/v1/system/info")
        assert response.status_code == 200

    def test_shutdown_event(self):
        """Test that shutdown event can be triggered"""
        from app.main import app

        # Create a new test client that will trigger startup/shutdown
        with TestClient(app) as test_client:
            # Make a request to ensure app started
            response = test_client.get("/api/v1/system/info")
            assert response.status_code == 200

        # Client context manager exit triggers shutdown event
        # If no exception is raised, shutdown was successful
