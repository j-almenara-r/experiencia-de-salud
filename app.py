#!/usr/bin/env python3
"""
Medical Patient Chatbot - Main Application

This is the main entry point for the medical patient chatbot system.
It provides a simple command-line interface for demonstration purposes.
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services import TranscriptProcessor, PatientChatbot, DigitalTwinManager
from src.models import PatientDigitalTwin


class MedicalChatbotApp:
    """Main application for the medical patient chatbot."""
    
    def __init__(self):
        """Initialize the application components."""
        self.twin_manager = DigitalTwinManager()
        self.transcript_processor = TranscriptProcessor()
        self.chatbot = PatientChatbot()
        self.current_patient_id = None
        self.current_twin = None
    
    def run(self):
        """Run the main application loop."""
        print("=" * 60)
        print("Medical Patient Chatbot - Digital Twin System")
        print("=" * 60)
        print("\nThis chatbot helps patients understand their medical information")
        print("and make informed decisions based on doctor consultations.\n")
        
        while True:
            print("\nMain Menu:")
            print("1. Create/Load Patient")
            print("2. Add Doctor Consultation Transcript")
            print("3. Chat with Patient Assistant")
            print("4. View Patient Information")
            print("5. List All Patients")
            print("6. Exit")
            
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == "1":
                self.load_or_create_patient()
            elif choice == "2":
                self.add_consultation_transcript()
            elif choice == "3":
                self.chat_session()
            elif choice == "4":
                self.view_patient_info()
            elif choice == "5":
                self.list_patients()
            elif choice == "6":
                print("\nThank you for using the Medical Patient Chatbot!")
                break
            else:
                print("\nInvalid option. Please try again.")
    
    def load_or_create_patient(self):
        """Load an existing patient or create a new one."""
        patient_id = input("\nEnter Patient ID: ").strip()
        
        if not patient_id:
            print("Error: Patient ID cannot be empty.")
            return
        
        self.current_twin = self.twin_manager.get_or_create_digital_twin(patient_id)
        self.current_patient_id = patient_id
        
        if len(self.current_twin.consultations) == 0:
            print(f"\nNew patient created: {patient_id}")
        else:
            print(f"\nLoaded existing patient: {patient_id}")
            print(f"Consultations: {len(self.current_twin.consultations)}")
            print(f"Active Conditions: {len(self.current_twin.get_active_conditions())}")
            print(f"Current Medications: {len(self.current_twin.get_current_medications())}")
    
    def add_consultation_transcript(self):
        """Add a doctor consultation transcript."""
        if not self.current_patient_id:
            print("\nError: Please load/create a patient first.")
            return
        
        print("\n--- Add Doctor Consultation Transcript ---")
        print("(Enter the transcript text. Type 'END' on a new line when done)\n")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        
        transcript = "\n".join(lines)
        
        if not transcript.strip():
            print("\nError: Transcript cannot be empty.")
            return
        
        doctor_specialty = input("\nDoctor's specialty (default: General Practice): ").strip()
        if not doctor_specialty:
            doctor_specialty = "General Practice"
        
        print("\nProcessing transcript...")
        try:
            extracted_data = self.transcript_processor.process_transcript(
                transcript=transcript,
                doctor_specialty=doctor_specialty,
            )
            
            self.current_twin = self.transcript_processor.update_digital_twin(
                self.current_twin,
                extracted_data,
            )
            
            self.twin_manager.save_digital_twin(self.current_twin)
            
            print("\n✓ Transcript processed successfully!")
            print(f"\nExtracted Information:")
            print(f"- Conditions: {len(extracted_data.get('conditions', []))}")
            print(f"- Medications: {len(extracted_data.get('medications', []))}")
            print(f"- Allergies: {len(extracted_data.get('allergies', []))}")
            print(f"- Recommendations: {len(extracted_data.get('recommendations', []))}")
            
        except Exception as e:
            print(f"\nError processing transcript: {str(e)}")
    
    def chat_session(self):
        """Start an interactive chat session."""
        if not self.current_patient_id:
            print("\nError: Please load/create a patient first.")
            return
        
        if len(self.current_twin.consultations) == 0:
            print("\nWarning: No consultation data available for this patient.")
            print("Consider adding a consultation transcript first for better responses.")
        
        print("\n" + "=" * 60)
        print("Patient Chat Session")
        print("=" * 60)
        print("\nYou can now ask questions about your medical information.")
        print("Type 'exit' to end the chat session.\n")
        
        # Get suggested questions
        print("Suggested questions:")
        try:
            suggestions = self.chatbot.get_suggested_questions(self.current_twin)
            for i, q in enumerate(suggestions, 1):
                print(f"{i}. {q}")
        except:
            print("(Unable to generate suggestions)")
        
        print("\n" + "-" * 60)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nChat session ended.")
                break
            
            if not user_input:
                continue
            
            try:
                response = self.chatbot.chat(
                    patient_id=self.current_patient_id,
                    digital_twin=self.current_twin,
                    user_message=user_input,
                )
                
                print(f"\nAssistant: {response}")
                
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    def view_patient_info(self):
        """View current patient information."""
        if not self.current_patient_id:
            print("\nError: Please load/create a patient first.")
            return
        
        print("\n" + "=" * 60)
        print(f"Patient Information: {self.current_patient_id}")
        print("=" * 60)
        print(self.current_twin.to_context_string())
        print("=" * 60)
    
    def list_patients(self):
        """List all patients in the system."""
        patients = self.twin_manager.list_patients()
        
        print("\n" + "=" * 60)
        print("Registered Patients")
        print("=" * 60)
        
        if not patients:
            print("No patients found.")
        else:
            for patient_id in patients:
                twin = self.twin_manager.get_digital_twin(patient_id)
                print(f"\n- {patient_id}")
                print(f"  Consultations: {len(twin.consultations)}")
                print(f"  Last updated: {twin.updated_at.strftime('%Y-%m-%d %H:%M')}")


def main():
    """Main entry point."""
    try:
        app = MedicalChatbotApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
