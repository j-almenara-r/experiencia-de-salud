"""
Digital Twin Model for Patient Medical Information

This module defines the data structure for patient digital twins,
storing medical history, current conditions, and consultation notes.
"""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MedicalCondition(BaseModel):
    """Represents a medical condition or diagnosis."""
    name: str
    diagnosed_date: Optional[datetime] = None
    status: str = "active"  # active, resolved, chronic
    notes: str = ""


class Medication(BaseModel):
    """Represents a prescribed medication."""
    name: str
    dosage: str
    frequency: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    purpose: str = ""


class Consultation(BaseModel):
    """Represents a doctor consultation."""
    date: datetime
    doctor_specialty: str
    transcript: str
    summary: str = ""
    recommendations: List[str] = Field(default_factory=list)
    follow_up: Optional[datetime] = None


class PatientDigitalTwin(BaseModel):
    """
    Digital Twin of a patient containing all medical information
    extracted from doctor consultations and medical records.
    """
    patient_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Basic Information
    age: Optional[int] = None
    gender: Optional[str] = None
    
    # Medical History
    conditions: List[MedicalCondition] = Field(default_factory=list)
    medications: List[Medication] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    
    # Consultation History
    consultations: List[Consultation] = Field(default_factory=list)
    
    # Summary and Context
    medical_summary: str = ""
    current_health_status: str = ""
    
    def add_consultation(self, consultation: Consultation):
        """Add a new consultation to the patient's history."""
        self.consultations.append(consultation)
        self.updated_at = datetime.now()
    
    def add_condition(self, condition: MedicalCondition):
        """Add a new medical condition."""
        self.conditions.append(condition)
        self.updated_at = datetime.now()
    
    def add_medication(self, medication: Medication):
        """Add a new medication."""
        self.medications.append(medication)
        self.updated_at = datetime.now()
    
    def get_active_conditions(self) -> List[MedicalCondition]:
        """Get all active medical conditions."""
        return [c for c in self.conditions if c.status == "active"]
    
    def get_current_medications(self) -> List[Medication]:
        """Get all current medications."""
        now = datetime.now()
        return [
            m for m in self.medications
            if (m.end_date is None or m.end_date > now)
        ]
    
    def to_context_string(self) -> str:
        """
        Generate a comprehensive context string for the LLM
        containing all relevant patient information.
        """
        context_parts = [
            f"Patient ID: {self.patient_id}",
            f"Age: {self.age if self.age else 'Unknown'}",
            f"Gender: {self.gender if self.gender else 'Unknown'}",
            "",
            "ACTIVE MEDICAL CONDITIONS:",
        ]
        
        active_conditions = self.get_active_conditions()
        if active_conditions:
            for condition in active_conditions:
                context_parts.append(f"- {condition.name}: {condition.notes}")
        else:
            context_parts.append("- None recorded")
        
        context_parts.extend(["", "CURRENT MEDICATIONS:"])
        current_meds = self.get_current_medications()
        if current_meds:
            for med in current_meds:
                context_parts.append(
                    f"- {med.name} ({med.dosage}, {med.frequency}): {med.purpose}"
                )
        else:
            context_parts.append("- None recorded")
        
        context_parts.extend(["", "ALLERGIES:"])
        if self.allergies:
            for allergy in self.allergies:
                context_parts.append(f"- {allergy}")
        else:
            context_parts.append("- None recorded")
        
        context_parts.extend(["", "MEDICAL SUMMARY:", self.medical_summary])
        
        context_parts.extend(["", "RECENT CONSULTATIONS:"])
        recent_consultations = sorted(
            self.consultations, key=lambda x: x.date, reverse=True
        )[:3]
        for consultation in recent_consultations:
            context_parts.append(
                f"- {consultation.date.strftime('%Y-%m-%d')} "
                f"({consultation.doctor_specialty}): {consultation.summary}"
            )
        
        return "\n".join(context_parts)
