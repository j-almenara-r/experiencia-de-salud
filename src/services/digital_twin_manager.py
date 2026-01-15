"""
Digital Twin Manager

This service manages the storage and retrieval of patient digital twins.
"""

import os
import json
from typing import Optional, Dict
from pathlib import Path
from datetime import datetime

from ..models.digital_twin import PatientDigitalTwin


class DigitalTwinManager:
    """Manages patient digital twins - creation, storage, and retrieval."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the digital twin manager.
        
        Args:
            data_dir: Directory to store patient data. Defaults to ./data
        """
        self.data_dir = Path(data_dir or os.getenv("DATA_DIR", "./data"))
        self.data_dir.mkdir(exist_ok=True)
        self.twins_dir = self.data_dir / "digital_twins"
        self.twins_dir.mkdir(exist_ok=True)
    
    def create_digital_twin(self, patient_id: str) -> PatientDigitalTwin:
        """
        Create a new digital twin for a patient.
        
        Args:
            patient_id: Unique identifier for the patient
        
        Returns:
            New PatientDigitalTwin instance
        """
        digital_twin = PatientDigitalTwin(
            patient_id=patient_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.save_digital_twin(digital_twin)
        return digital_twin
    
    def get_digital_twin(self, patient_id: str) -> Optional[PatientDigitalTwin]:
        """
        Retrieve a patient's digital twin.
        
        Args:
            patient_id: Unique identifier for the patient
        
        Returns:
            PatientDigitalTwin if found, None otherwise
        """
        file_path = self.twins_dir / f"{patient_id}.json"
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse datetime strings back to datetime objects
            data = self._parse_datetimes(data)
            
            return PatientDigitalTwin(**data)
            
        except Exception as e:
            raise Exception(f"Error loading digital twin for patient {patient_id}: {str(e)}")
    
    def save_digital_twin(self, digital_twin: PatientDigitalTwin):
        """
        Save a patient's digital twin to storage.
        
        Args:
            digital_twin: The digital twin to save
        """
        file_path = self.twins_dir / f"{digital_twin.patient_id}.json"
        
        try:
            # Convert to dict and handle datetime serialization
            data = json.loads(digital_twin.model_dump_json())
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Error saving digital twin: {str(e)}")
    
    def get_or_create_digital_twin(self, patient_id: str) -> PatientDigitalTwin:
        """
        Get an existing digital twin or create a new one.
        
        Args:
            patient_id: Unique identifier for the patient
        
        Returns:
            PatientDigitalTwin instance
        """
        digital_twin = self.get_digital_twin(patient_id)
        if digital_twin is None:
            digital_twin = self.create_digital_twin(patient_id)
        return digital_twin
    
    def list_patients(self) -> list[str]:
        """
        List all patient IDs with digital twins.
        
        Returns:
            List of patient IDs
        """
        patient_files = self.twins_dir.glob("*.json")
        return [f.stem for f in patient_files]
    
    def delete_digital_twin(self, patient_id: str) -> bool:
        """
        Delete a patient's digital twin.
        
        Args:
            patient_id: Unique identifier for the patient
        
        Returns:
            True if deleted, False if not found
        """
        file_path = self.twins_dir / f"{patient_id}.json"
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def _parse_datetimes(self, data: Dict) -> Dict:
        """
        Recursively parse datetime strings back to datetime objects.
        
        Args:
            data: Dictionary containing serialized data
        
        Returns:
            Dictionary with datetime objects
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and self._is_datetime_string(value):
                    try:
                        data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        pass
                elif isinstance(value, dict):
                    data[key] = self._parse_datetimes(value)
                elif isinstance(value, list):
                    data[key] = [self._parse_datetimes(item) if isinstance(item, dict) else item for item in value]
        return data
    
    def _is_datetime_string(self, value: str) -> bool:
        """Check if a string looks like a datetime."""
        return (
            isinstance(value, str) and
            len(value) > 10 and
            ('T' in value or '-' in value) and
            any(char.isdigit() for char in value)
        )
