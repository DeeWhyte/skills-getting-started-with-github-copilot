"""
Tests for Mergington High School Activities API.

All tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the functionality being tested
- Assert: Verify the results
"""
import pytest


class TestGetActivities:
    """Test GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        Arrange: Fresh activities data provided by fixture
        Act: Call GET /activities
        Assert: Verify status 200, all activities returned with correct structure
        """
        # Arrange: (handled by client fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        # Verify all activities are present
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        
    def test_get_activities_has_correct_structure(self, client):
        """
        Test that each activity has the correct data structure.
        
        Arrange: Fresh activities data provided by fixture
        Act: Call GET /activities
        Assert: Verify each activity has required fields and correct participant counts
        """
        # Arrange: (handled by client fixture)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert: Check structure of a sample activity
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        
        # Verify participant count matches
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint."""

    def test_signup_adds_participant_to_activity(self, client):
        """
        Test that signing up adds a participant to an activity.
        
        Arrange: Fresh activities, prepare new email to add
        Act: POST to signup endpoint with new email
        Assert: Verify participant added and count incremented
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "alex@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert: Check response
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert new_email in response.json()["message"]
        
        # Verify participant was actually added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 3  # Was 2, now 3

    def test_signup_returns_success_message(self, client):
        """
        Test that signup returns a proper success message.
        
        Arrange: Fresh activities, new email
        Act: POST to signup endpoint
        Assert: Verify response contains correct success message format
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "charlie@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {new_email}" in data["message"]
        assert activity_name in data["message"]


class TestRemoveParticipant:
    """Test DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_deletes_from_activity(self, client):
        """
        Test that removing a participant deletes them from an activity.
        
        Arrange: Fresh activities with existing participants
        Act: DELETE participant endpoint
        Assert: Verify participant removed and count decremented
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        
        # Assert: Check response
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        
        # Verify participant was actually removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 1  # Was 2, now 1

    def test_remove_participant_returns_success_message(self, client):
        """
        Test that remove returns a proper success message.
        
        Arrange: Fresh activities with existing participants
        Act: DELETE participant endpoint
        Assert: Verify response contains correct success message format
        """
        # Arrange
        activity_name = "Programming Class"
        email_to_remove = "emma@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Removed {email_to_remove}" in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_decrements_count(self, client):
        """
        Test that removing a participant correctly updates the participant count.
        
        Arrange: Fresh activities, note initial count
        Act: DELETE a participant
        Assert: Verify count decremented by exactly 1
        """
        # Arrange
        activity_name = "Gym Class"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        email_to_remove = "john@mergington.edu"
        
        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        
        # Assert
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
