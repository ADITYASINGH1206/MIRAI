import pytest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
import json

def test_1_app_initialization():
    """Test 1 - Initialization: Initialize app and assert no exceptions on landing page."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert at.session_state["current_page"] == "landing"
    assert len(at.button) > 0


def test_2_session_state_mock_data():
    """Test 2 - Session State Mock Data: Assert mock DataFrames and data structures load on start."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert "activity_log" in at.session_state
    assert not at.session_state["activity_log"].empty
    assert "sticky_notes" in at.session_state
    assert len(at.session_state["sticky_notes"]) == 4
    assert "mermaid_code" in at.session_state
    assert "quiz_data" in at.session_state
    assert len(at.session_state["quiz_data"]) == 5
    assert "revision_notes" in at.session_state


def test_3_workspace_navigation_and_tabs():
    """Test 3 - Navigation & Tabs: Switch to workspace and verify tabs, containers and metrics render."""
    at = AppTest.from_file("app.py").run()
    at.session_state["current_page"] = "workspace"
    at.run()
    
    assert not at.exception
    assert at.session_state["current_page"] == "workspace"
    assert len(at.tabs) >= 1
    assert len(at.metric) >= 3
    assert len(at.button) >= 2


def test_4_form_submission_and_api_mocking():
    """Test 4 - Form Submission & API Mocking: Simulate AI synthesis form submit with mocked Gemini API."""
    mock_payload = {
        "mermaid": "graph TD\n  A[Test Start] --> B[Test End]",
        "sticky_notes": [
            "Mock Fact 1",
            "Mock Fact 2",
            "Mock Fact 3",
            "Mock Fact 4"
        ],
        "revision_notes": "# Mock Revision Guide\n\n- Point 1\n- Point 2"
    }
    
    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_payload)
    
    with patch("google.generativeai.GenerativeModel.generate_content", return_value=mock_response):
        at = AppTest.from_file("app.py").run()
        at.session_state["current_page"] = "workspace"
        at.run()
        
        # Ingest text into the master input text_area and submit
        if len(at.text_area) > 0:
            at.text_area[0].input("Lecture on Advanced Operating Systems and Memory Virtualization")
            # Click master submit button
            at.button[1].click()
            at.run()
        
        assert not at.exception
        assert at.session_state["mermaid_code"] == "graph TD\n  A[Test Start] --> B[Test End]"
        assert at.session_state["sticky_notes"][0] == "Mock Fact 1"
        assert "# Mock Revision Guide" in at.session_state["revision_notes"]
