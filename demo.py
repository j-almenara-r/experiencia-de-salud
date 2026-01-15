#!/usr/bin/env python3
"""
Demo script for the Medical Patient Chatbot

This script demonstrates the key features of the system with example data.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services import TranscriptProcessor, PatientChatbot, DigitalTwinManager
from src.models import PatientDigitalTwin


# Example transcript for demonstration
EXAMPLE_TRANSCRIPT = """
Doctor: Good morning, I've reviewed your blood test results.
Patient: Good morning, doctor. How do they look?
Doctor: Your glucose levels are elevated. Your hemoglobin A1c is at 7.2%, which indicates type 2 diabetes.
Patient: Oh no, is that serious?
Doctor: It's manageable with proper treatment. I'm prescribing metformin 500mg, take one tablet twice daily with meals.
Patient: Are there any side effects?
Doctor: You might experience some stomach upset initially, but it usually subsides. Taking it with food helps.
Patient: I see. What else should I do?
Doctor: Diet is crucial - reduce simple carbohydrates and sugars. I also recommend 30 minutes of moderate exercise daily.
Patient: Okay, I can do that.
Doctor: I'd like to see you again in three months to monitor your levels. We'll need blood work done a week before that appointment.
Patient: Sounds good.
Doctor: Do you have any medication allergies?
Patient: I'm allergic to penicillin.
Doctor: Good to know, I'll note that in your file. Any other questions?
Patient: No, I think that covers everything. Thank you.
"""


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo():
    """Run the demonstration."""
    print_section("Medical Patient Chatbot - Demo")
    
    print("This demo will:")
    print("1. Create a patient digital twin")
    print("2. Process a medical consultation transcript")
    print("3. Show extracted medical information")
    print("4. Demonstrate the chat interface")
    print("\nNote: This demo requires an OpenAI API key in .env file")
    print("Press Enter to continue or Ctrl+C to exit...")
    input()
    
    # Initialize services
    print_section("Step 1: Initializing Services")
    print("Creating Digital Twin Manager...")
    twin_manager = DigitalTwinManager()
    print("✓ Digital Twin Manager ready")
    
    print("\nCreating Transcript Processor...")
    try:
        transcript_processor = TranscriptProcessor()
        print("✓ Transcript Processor ready")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("\nMake sure you have set OPENAI_API_KEY in your .env file")
        return
    
    print("\nCreating Patient Chatbot...")
    chatbot = PatientChatbot()
    print("✓ Patient Chatbot ready")
    
    # Create patient
    print_section("Step 2: Creating Patient Digital Twin")
    patient_id = "demo_patient_001"
    print(f"Creating digital twin for patient: {patient_id}")
    digital_twin = twin_manager.get_or_create_digital_twin(patient_id)
    print(f"✓ Digital twin created")
    
    # Process transcript
    print_section("Step 3: Processing Medical Consultation")
    print("Consultation transcript:")
    print("-" * 70)
    print(EXAMPLE_TRANSCRIPT)
    print("-" * 70)
    
    print("\nProcessing transcript with AI...")
    try:
        extracted_data = transcript_processor.process_transcript(
            transcript=EXAMPLE_TRANSCRIPT,
            doctor_specialty="Endocrinology"
        )
        print("✓ Transcript processed successfully")
        
        print("\n--- Extracted Information ---")
        print(f"Summary: {extracted_data.get('summary', 'N/A')}")
        print(f"\nConditions found: {len(extracted_data.get('conditions', []))}")
        for condition in extracted_data.get('conditions', []):
            print(f"  - {condition['name']} ({condition.get('status', 'unknown')})")
        
        print(f"\nMedications found: {len(extracted_data.get('medications', []))}")
        for med in extracted_data.get('medications', []):
            print(f"  - {med['name']} {med.get('dosage', '')} {med.get('frequency', '')}")
        
        print(f"\nAllergies found: {len(extracted_data.get('allergies', []))}")
        for allergy in extracted_data.get('allergies', []):
            print(f"  - {allergy}")
        
        print(f"\nRecommendations: {len(extracted_data.get('recommendations', []))}")
        for rec in extracted_data.get('recommendations', []):
            print(f"  - {rec}")
        
    except Exception as e:
        print(f"✗ Error processing transcript: {str(e)}")
        return
    
    # Update digital twin
    print_section("Step 4: Updating Digital Twin")
    print("Integrating extracted data into patient digital twin...")
    digital_twin = transcript_processor.update_digital_twin(
        digital_twin,
        extracted_data
    )
    twin_manager.save_digital_twin(digital_twin)
    print("✓ Digital twin updated and saved")
    
    print("\n--- Current Patient Profile ---")
    print(digital_twin.to_context_string())
    
    # Chat demonstration
    print_section("Step 5: Patient Chat Interface Demo")
    print("The patient can now ask questions about their medical information.")
    
    # Get suggested questions
    print("\nGenerating suggested questions...")
    try:
        suggestions = chatbot.get_suggested_questions(digital_twin)
        print("\nSuggested questions for the patient:")
        for i, question in enumerate(suggestions, 1):
            print(f"{i}. {question}")
    except Exception as e:
        print(f"Could not generate suggestions: {str(e)}")
        suggestions = [
            "What medications am I taking?",
            "What should I know about my diabetes?",
            "What lifestyle changes should I make?"
        ]
    
    # Example questions
    example_questions = [
        "What medications am I taking and what are they for?",
        "What is type 2 diabetes and how serious is it?",
        "What dietary changes should I make?"
    ]
    
    print("\n\nDemonstrating chat with example questions...")
    
    for i, question in enumerate(example_questions, 1):
        print("\n" + "-" * 70)
        print(f"Example Question {i}: {question}")
        print("-" * 70)
        
        try:
            response = chatbot.chat(
                patient_id=patient_id,
                digital_twin=digital_twin,
                user_message=question
            )
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")
        
        if i < len(example_questions):
            print("\nPress Enter to see next question...")
            input()
    
    # Summary
    print_section("Demo Complete!")
    print("This demonstration showed:")
    print("✓ Medical transcript processing with AI")
    print("✓ Automatic extraction of medical information")
    print("✓ Digital twin creation and management")
    print("✓ Conversational AI for patient questions")
    print("\nThe system is now ready to help patients understand their")
    print("medical information and make informed decisions!")
    print("\nTo use the full application, run: python app.py")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {str(e)}")
        import traceback
        traceback.print_exc()
