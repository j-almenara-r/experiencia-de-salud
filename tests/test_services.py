"""
Test suite for DigitalTwinManager service
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from src.services.digital_twin_manager import DigitalTwinManager
from src.models.digital_twin import PatientDigitalTwin, MedicalCondition


class TestDigitalTwinManager:
    """Tests for DigitalTwinManager."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def manager(self, temp_dir):
        """Create a manager with temporary directory."""
        return DigitalTwinManager(data_dir=temp_dir)
    
    def test_create_digital_twin(self, manager):
        """Test creating a new digital twin."""
        twin = manager.create_digital_twin("patient_001")
        
        assert twin.patient_id == "patient_001"
        assert isinstance(twin, PatientDigitalTwin)
        
        # Check that it was saved
        saved_twin = manager.get_digital_twin("patient_001")
        assert saved_twin is not None
        assert saved_twin.patient_id == "patient_001"
    
    def test_save_and_load_digital_twin(self, manager):
        """Test saving and loading a digital twin."""
        twin = PatientDigitalTwin(
            patient_id="patient_002",
            age=45,
            gender="Female"
        )
        twin.add_condition(MedicalCondition(
            name="Hypertension",
            status="active"
        ))
        
        manager.save_digital_twin(twin)
        
        loaded_twin = manager.get_digital_twin("patient_002")
        
        assert loaded_twin is not None
        assert loaded_twin.patient_id == "patient_002"
        assert loaded_twin.age == 45
        assert loaded_twin.gender == "Female"
        assert len(loaded_twin.conditions) == 1
        assert loaded_twin.conditions[0].name == "Hypertension"
    
    def test_get_nonexistent_digital_twin(self, manager):
        """Test getting a digital twin that doesn't exist."""
        twin = manager.get_digital_twin("nonexistent")
        assert twin is None
    
    def test_get_or_create_existing(self, manager):
        """Test get_or_create with existing twin."""
        original = manager.create_digital_twin("patient_003")
        original.age = 50
        manager.save_digital_twin(original)
        
        retrieved = manager.get_or_create_digital_twin("patient_003")
        
        assert retrieved.patient_id == "patient_003"
        assert retrieved.age == 50
    
    def test_get_or_create_new(self, manager):
        """Test get_or_create with new twin."""
        twin = manager.get_or_create_digital_twin("patient_004")
        
        assert twin.patient_id == "patient_004"
        assert isinstance(twin, PatientDigitalTwin)
    
    def test_list_patients(self, manager):
        """Test listing all patients."""
        manager.create_digital_twin("patient_001")
        manager.create_digital_twin("patient_002")
        manager.create_digital_twin("patient_003")
        
        patients = manager.list_patients()
        
        assert len(patients) == 3
        assert "patient_001" in patients
        assert "patient_002" in patients
        assert "patient_003" in patients
    
    def test_delete_digital_twin(self, manager):
        """Test deleting a digital twin."""
        manager.create_digital_twin("patient_005")
        
        # Verify it exists
        assert manager.get_digital_twin("patient_005") is not None
        
        # Delete it
        result = manager.delete_digital_twin("patient_005")
        assert result is True
        
        # Verify it's gone
        assert manager.get_digital_twin("patient_005") is None
    
    def test_delete_nonexistent_digital_twin(self, manager):
        """Test deleting a digital twin that doesn't exist."""
        result = manager.delete_digital_twin("nonexistent")
        assert result is False
