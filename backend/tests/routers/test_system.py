"""
Tests for system endpoints
"""

from unittest.mock import patch

from fastapi import status


class TestSystemRouter:
    """Tests for system endpoints"""

    def test_system_info(self, client):
        """Test GET /api/v1/system/info"""
        response = client.get("/api/v1/system/info")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "api_status" in data
        assert "environment" in data
        assert "build_date" in data
        assert "database" in data
        assert data["api_status"] == "connected"
        assert data["environment"] == "development"

    def test_system_info_db_error(self, client, db_session):
        """Test system info with database connection error"""
        # This test simulates a database error by using a mock
        with patch("app.routers.system.text") as mock_text:
            mock_text.side_effect = Exception("Database connection error")
            response = client.get("/api/v1/system/info")

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
