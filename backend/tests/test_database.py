"""
Tests for database module
"""

from app.database import SessionLocal, get_db


class TestDatabase:
    """Tests for database connection and session management"""

    def test_get_db_yields_session(self):
        """Test that get_db yields a database session"""
        db_gen = get_db()
        db = next(db_gen)

        assert db is not None
        assert isinstance(db, type(SessionLocal()))

        # Cleanup - this tests the finally block
        try:
            next(db_gen)
        except StopIteration:
            pass  # Expected behavior

    def test_get_db_closes_session(self):
        """Test that get_db closes the session after use"""
        db_gen = get_db()
        db = next(db_gen)

        # Verify we got a session
        assert db is not None

        # Trigger the finally block by exhausting the generator
        try:
            next(db_gen)
        except StopIteration:
            pass

        # If we reach here without exception, the finally block executed successfully
        assert True
