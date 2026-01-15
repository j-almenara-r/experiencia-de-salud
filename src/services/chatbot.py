"""
Patient Chatbot Service

This service provides the conversational interface for patients to ask
questions about their medical information and get informed answers.
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from ..models.digital_twin import PatientDigitalTwin

load_dotenv()


class PatientChatbot:
    """Chatbot service for patient interactions."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the patient chatbot.
        
        Args:
            api_key: OpenAI API key. If not provided, reads from environment.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4")
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def get_system_prompt(self, digital_twin: PatientDigitalTwin) -> str:
        """
        Generate system prompt with patient context.
        
        Args:
            digital_twin: The patient's digital twin
        
        Returns:
            System prompt string
        """
        patient_context = digital_twin.to_context_string()
        
        return f"""You are a specialized medical assistant chatbot helping a patient understand their medical information and make informed decisions.

PATIENT INFORMATION:
{patient_context}

YOUR ROLE:
- Answer patient questions clearly and compassionately
- Help patients understand their medical conditions, medications, and treatments
- Provide context for medical decisions based on their specific situation
- Explain medical terminology in simple language
- Suggest questions they might want to ask their doctor
- Remind them to consult their doctor for medical advice

IMPORTANT GUIDELINES:
- Always be clear that you're providing information, not medical advice
- Encourage patients to discuss concerns with their healthcare provider
- Be honest about uncertainty and limitations
- Use simple, patient-friendly language
- Be empathetic and supportive
- Respect patient privacy and confidentiality
- If asked about something not in the patient's record, clearly state that

SAFETY:
- Never recommend stopping or changing medications without doctor consultation
- Always encourage seeking immediate medical attention for emergencies
- Do not diagnose new conditions
- Do not recommend specific treatments not already prescribed"""
    
    def chat(
        self,
        patient_id: str,
        digital_twin: PatientDigitalTwin,
        user_message: str,
        include_history: bool = True,
    ) -> str:
        """
        Process a patient's question and generate a response.
        
        Args:
            patient_id: Unique identifier for the patient
            digital_twin: The patient's digital twin
            user_message: The patient's question or message
            include_history: Whether to include conversation history
        
        Returns:
            The chatbot's response
        """
        # Initialize conversation history if needed
        if patient_id not in self.conversation_history:
            self.conversation_history[patient_id] = []
        
        # Build messages for the API call
        messages = [
            {"role": "system", "content": self.get_system_prompt(digital_twin)}
        ]
        
        # Add conversation history if requested
        if include_history:
            messages.extend(self.conversation_history[patient_id])
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
            )
            
            assistant_message = response.choices[0].message.content
            
            # Store in conversation history
            self.conversation_history[patient_id].append(
                {"role": "user", "content": user_message}
            )
            self.conversation_history[patient_id].append(
                {"role": "assistant", "content": assistant_message}
            )
            
            # Keep only last 10 exchanges (20 messages) to manage context length
            if len(self.conversation_history[patient_id]) > 20:
                self.conversation_history[patient_id] = self.conversation_history[patient_id][-20:]
            
            return assistant_message
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def clear_history(self, patient_id: str):
        """Clear conversation history for a patient."""
        if patient_id in self.conversation_history:
            self.conversation_history[patient_id] = []
    
    def get_suggested_questions(self, digital_twin: PatientDigitalTwin) -> List[str]:
        """
        Generate suggested questions based on patient's medical information.
        
        Args:
            digital_twin: The patient's digital twin
        
        Returns:
            List of suggested questions
        """
        patient_context = digital_twin.to_context_string()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical assistant. Generate 5 relevant questions a patient might want to ask based on their medical information. Return only the questions, one per line."
                    },
                    {
                        "role": "user",
                        "content": f"Based on this patient information, what questions might they have?\n\n{patient_context}"
                    }
                ],
                temperature=0.8,
                max_tokens=300,
            )
            
            questions = response.choices[0].message.content.strip().split("\n")
            # Clean up questions (remove numbering, extra whitespace)
            questions = [q.strip().lstrip("0123456789.-) ") for q in questions if q.strip()]
            
            return questions[:5]
            
        except Exception as e:
            print(f"Warning: Could not generate suggested questions: {str(e)}")
            return [
                "What are my current medications and what are they for?",
                "What should I know about my medical conditions?",
                "Are there any side effects I should watch for?",
                "What lifestyle changes should I consider?",
                "When should I schedule my next appointment?",
            ]
