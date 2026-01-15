"""
Test suite for Digital Twin models
"""

import pytest
from datetime import datetime
from src.models.digital_twin import (
    PatientDigitalTwin,
    MedicalCondition,
    Medication,
    Consultation,
)


class TestMedicalCondition:
    """Tests for MedicalCondition model."""
    
    def test_create_condition(self):
        """Test creating a medical condition."""
        condition = MedicalCondition(
            name="Type 2 Diabetes",
            status="chronic",
            notes="Diagnosed 2 years ago"
        )
        assert condition.name == "Type 2 Diabetes"
        assert condition.status == "chronic"
        assert condition.notes == "Diagnosed 2 years ago"
    
    def test_condition_defaults(self):
        """Test default values for medical condition."""
        condition = MedicalCondition(name="Hypertension")
        assert condition.status == "active"
        assert condition.notes == ""
        assert condition.diagnosed_date is None


class TestMedication:
    """Tests for Medication model."""
    
    def test_create_medication(self):
        """Test creating a medication."""
        med = Medication(
            name="Metformin",
            dosage="500mg",
            frequency="twice daily",
            purpose="Blood sugar control"
        )
        assert med.name == "Metformin"
        assert med.dosage == "500mg"
        assert med.frequency == "twice daily"
        assert med.purpose == "Blood sugar control"
    
    def test_medication_defaults(self):
        """Test default values for medication."""
        med = Medication(
            name="Aspirin",
            dosage="81mg",
            frequency="once daily"
        )
        assert med.purpose == ""
        assert med.start_date is None
        assert med.end_date is None


class TestConsultation:
    """Tests for Consultation model."""
    
    def test_create_consultation(self):
        """Test creating a consultation."""
        now = datetime.now()
        consultation = Consultation(
            date=now,
            doctor_specialty="Cardiology",
            transcript="Doctor: Hello...",
            summary="Routine checkup"
        )
        assert consultation.date == now
        assert consultation.doctor_specialty == "Cardiology"
        assert consultation.transcript == "Doctor: Hello..."
        assert consultation.summary == "Routine checkup"


class TestPatientDigitalTwin:
    """Tests for PatientDigitalTwin model."""
    
    def test_create_digital_twin(self):
        """Test creating a patient digital twin."""
        twin = PatientDigitalTwin(patient_id="patient_001")
        assert twin.patient_id == "patient_001"
        assert twin.age is None
        assert twin.gender is None
        assert len(twin.conditions) == 0
        assert len(twin.medications) == 0
        assert len(twin.allergies) == 0
        assert len(twin.consultations) == 0
    
    def test_add_condition(self):
        """Test adding a condition to digital twin."""
        twin = PatientDigitalTwin(patient_id="patient_001")
        condition = MedicalCondition(name="Diabetes", status="chronic")
        
        twin.add_condition(condition)
        
        assert len(twin.conditions) == 1
        assert twin.conditions[0].name == "Diabetes"
    
    def test_add_medication(self):
        """Test adding a medication to digital twin."""
        twin = PatientDigitalTwin(patient_id="patient_001")
        med = Medication(
            name="Metformin",
            dosage="500mg",
            frequency="twice daily"
        )
        
        twin.add_medication(med)
        
        assert len(twin.medications) == 1
        assert twin.medications[0].name == "Metformin"
    
    def test_add_consultation(self):
        """Test adding a consultation to digital twin."""
        twin = PatientDigitalTwin(patient_id="patient_001")
        consultation = Consultation(
            date=datetime.now(),
            doctor_specialty="General Practice",
            transcript="Test transcript"
        )
        
        twin.add_consultation(consultation)
        
        assert len(twin.consultations) == 1
        assert twin.consultations[0].doctor_specialty == "General Practice"
    
    def test_get_active_conditions(self):
        """Test getting active conditions."""
        twin = PatientDigitalTwin(patient_id="patient_001")
        twin.add_condition(MedicalCondition(name="Diabetes", status="active"))
        twin.add_condition(MedicalCondition(name="Old Injury", status="resolved"))
        twin.add_condition(MedicalCondition(name="Hypertension", status="active"))
        
        active = twin.get_active_conditions()
        
        assert len(active) == 2
        assert all(c.status == "active" for c in active)
    
    def test_get_current_medications(self):
        """Test getting current medications."""
        twin = PatientDigitalTwin(patient_id="patient_001")
        
        # Add current medication
        current_med = Medication(
            name="Metformin",
            dosage="500mg",
            frequency="twice daily",
            start_date=datetime.now()
        )
        twin.add_medication(current_med)
        
        # Add past medication
        past_date = datetime(2020, 1, 1)
        past_med = Medication(
            name="Old Med",
            dosage="100mg",
            frequency="once daily",
            start_date=past_date,
            end_date=past_date
        )
        twin.add_medication(past_med)
        
        current_meds = twin.get_current_medications()
        
        assert len(current_meds) == 1
        assert current_meds[0].name == "Metformin"
    
    def test_to_context_string(self):
        """Test generating context string."""
        twin = PatientDigitalTwin(
            patient_id="patient_001",
            age=45,
            gender="Male"
        )
        twin.add_condition(MedicalCondition(
            name="Type 2 Diabetes",
            status="active",
            notes="Diagnosed 2 years ago"
        ))
        twin.add_medication(Medication(
            name="Metformin",
            dosage="500mg",
            frequency="twice daily",
            purpose="Blood sugar control"
        ))
        twin.allergies.append("Penicillin")
        twin.medical_summary = "Patient with type 2 diabetes under good control."
        
        context = twin.to_context_string()
        
        assert "patient_001" in context
        assert "45" in context
        assert "Male" in context
        assert "Type 2 Diabetes" in context
        assert "Metformin" in context
        assert "Penicillin" in context
        assert "Blood sugar control" in context
