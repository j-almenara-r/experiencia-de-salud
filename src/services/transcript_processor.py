"""
Medical Transcript Processor

This service processes medical transcripts from doctor consultations
and extracts structured information to build/update patient digital twins.
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from ..models.digital_twin import (
    PatientDigitalTwin,
    Consultation,
    MedicalCondition,
    Medication,
)

load_dotenv()


class TranscriptProcessor:
    """Processes medical transcripts and extracts structured information."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the transcript processor.
        
        Args:
            api_key: OpenAI API key. If not provided, reads from environment.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4")
    
    def process_transcript(
        self,
        transcript: str,
        doctor_specialty: str = "General Practice",
        consultation_date: Optional[datetime] = None,
    ) -> Dict:
        """
        Process a medical transcript and extract structured information.
        
        Args:
            transcript: The raw transcript text from the consultation
            doctor_specialty: The specialty of the doctor conducting the consultation
            consultation_date: Date of the consultation (defaults to now)
        
        Returns:
            Dictionary containing extracted medical information
        """
        if consultation_date is None:
            consultation_date = datetime.now()
        
        system_prompt = """You are a medical information extraction AI. 
Your task is to analyze doctor-patient consultation transcripts and extract structured medical information.
Extract the following information when present:
1. Patient demographics (age, gender)
2. Medical conditions/diagnoses mentioned
3. Medications prescribed or discussed
4. Allergies mentioned
5. Key recommendations
6. Follow-up instructions
7. A brief summary of the consultation

Return the information as a JSON object with the following structure:
{
    "patient_info": {
        "age": <integer or null>,
        "gender": <string or null>
    },
    "conditions": [
        {
            "name": "<condition name>",
            "status": "active|chronic|resolved",
            "notes": "<additional context>"
        }
    ],
    "medications": [
        {
            "name": "<medication name>",
            "dosage": "<dosage>",
            "frequency": "<frequency>",
            "purpose": "<why prescribed>"
        }
    ],
    "allergies": ["<allergy1>", "<allergy2>"],
    "recommendations": ["<recommendation1>", "<recommendation2>"],
    "summary": "<brief summary of consultation>",
    "follow_up_needed": <boolean>,
    "follow_up_timeframe": "<timeframe if applicable>"
}

If information is not present in the transcript, use null or empty arrays as appropriate.
Be precise and only extract information that is explicitly stated or strongly implied."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this medical consultation transcript:\n\n{transcript}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            extracted_data = json.loads(response.choices[0].message.content)
            extracted_data["consultation_date"] = consultation_date
            extracted_data["doctor_specialty"] = doctor_specialty
            extracted_data["original_transcript"] = transcript
            
            return extracted_data
            
        except Exception as e:
            raise Exception(f"Error processing transcript: {str(e)}")
    
    def update_digital_twin(
        self,
        digital_twin: PatientDigitalTwin,
        extracted_data: Dict,
    ) -> PatientDigitalTwin:
        """
        Update a patient's digital twin with extracted information.
        
        Args:
            digital_twin: The patient's existing digital twin
            extracted_data: Extracted information from process_transcript
        
        Returns:
            Updated digital twin
        """
        # Update basic patient info if provided
        if extracted_data.get("patient_info"):
            patient_info = extracted_data["patient_info"]
            if patient_info.get("age") and not digital_twin.age:
                digital_twin.age = patient_info["age"]
            if patient_info.get("gender") and not digital_twin.gender:
                digital_twin.gender = patient_info["gender"]
        
        # Add consultation
        consultation = Consultation(
            date=extracted_data["consultation_date"],
            doctor_specialty=extracted_data["doctor_specialty"],
            transcript=extracted_data["original_transcript"],
            summary=extracted_data.get("summary", ""),
            recommendations=extracted_data.get("recommendations", []),
        )
        digital_twin.add_consultation(consultation)
        
        # Add conditions
        for condition_data in extracted_data.get("conditions", []):
            condition = MedicalCondition(
                name=condition_data["name"],
                status=condition_data.get("status", "active"),
                notes=condition_data.get("notes", ""),
                diagnosed_date=extracted_data["consultation_date"],
            )
            # Check if condition already exists
            existing = next(
                (c for c in digital_twin.conditions if c.name.lower() == condition.name.lower()),
                None
            )
            if not existing:
                digital_twin.add_condition(condition)
        
        # Add medications
        for med_data in extracted_data.get("medications", []):
            medication = Medication(
                name=med_data["name"],
                dosage=med_data.get("dosage", ""),
                frequency=med_data.get("frequency", ""),
                purpose=med_data.get("purpose", ""),
                start_date=extracted_data["consultation_date"],
            )
            # Check if medication already exists
            existing = next(
                (m for m in digital_twin.medications if m.name.lower() == medication.name.lower()),
                None
            )
            if not existing:
                digital_twin.add_medication(medication)
        
        # Add allergies
        for allergy in extracted_data.get("allergies", []):
            if allergy not in digital_twin.allergies:
                digital_twin.allergies.append(allergy)
        
        # Update medical summary
        self._update_medical_summary(digital_twin)
        
        return digital_twin
    
    def _update_medical_summary(self, digital_twin: PatientDigitalTwin):
        """Generate an updated medical summary for the digital twin."""
        try:
            context = digital_twin.to_context_string()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical AI assistant. Create a concise medical summary (2-3 paragraphs) based on the patient information provided."
                    },
                    {
                        "role": "user",
                        "content": f"Create a comprehensive medical summary for this patient:\n\n{context}"
                    }
                ],
                temperature=0.3,
            )
            
            digital_twin.medical_summary = response.choices[0].message.content
            
        except Exception as e:
            print(f"Warning: Could not generate medical summary: {str(e)}")
