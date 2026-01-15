# Architecture Documentation

## System Overview

The Medical Patient Chatbot system is designed to bridge the gap between medical consultations and patient understanding. It creates a "digital twin" of each patient by processing doctor consultations and provides an AI-powered interface for patients to ask questions about their medical information.

## Core Components

### 1. Digital Twin Model

The digital twin is the central data structure representing a patient's complete medical profile.

**Key Features:**
- Stores patient demographics (age, gender)
- Maintains medical conditions with status (active, chronic, resolved)
- Tracks medications with dosage and frequency
- Records allergies
- Preserves consultation history
- Generates contextual summaries

**Data Structure:**
```
PatientDigitalTwin
├── patient_id: str
├── demographics: {age, gender}
├── conditions: [MedicalCondition]
├── medications: [Medication]
├── allergies: [str]
├── consultations: [Consultation]
└── medical_summary: str
```

### 2. Transcript Processing Pipeline

Processes raw medical transcripts to extract structured information.

**Flow:**
1. **Input**: Raw text transcript from doctor-patient consultation
2. **LLM Processing**: OpenAI GPT-4 analyzes the transcript using structured prompts
3. **Extraction**: Identifies conditions, medications, allergies, recommendations
4. **Validation**: Checks for duplicates and conflicts
5. **Integration**: Updates the patient's digital twin
6. **Summary Generation**: Creates/updates medical summary

**Extraction Categories:**
- Patient demographics
- Medical conditions/diagnoses
- Medications (name, dosage, frequency, purpose)
- Allergies
- Clinical recommendations
- Follow-up requirements

### 3. Conversational AI Interface

Provides natural language interaction for patients.

**Features:**
- **Context-Aware**: Uses full patient history for accurate responses
- **Safe Responses**: Always reminds patients this is information, not medical advice
- **Conversation Memory**: Maintains chat history for coherent dialogue
- **Suggested Questions**: Generates relevant questions based on patient data
- **Emergency Detection**: Encourages seeking immediate care when appropriate

**System Prompt Structure:**
1. Patient context (conditions, medications, history)
2. Role definition (information provider, not diagnostician)
3. Safety guidelines (no prescription changes, emergency awareness)
4. Communication style (clear, empathetic, patient-friendly)

### 4. Data Management

Handles persistence and retrieval of patient digital twins.

**Storage:**
- Local JSON files (one per patient)
- Directory structure: `data/digital_twins/{patient_id}.json`
- Serialization handles datetime objects automatically

**Operations:**
- Create new digital twin
- Load existing digital twin
- Save updates
- List all patients
- Delete patient data (with caution)

## Data Flow Diagrams

### Consultation Processing Flow

```
Doctor Consultation (Audio/Text)
          ↓
    Transcription
          ↓
  Transcript Processor
    (LLM Analysis)
          ↓
  Structured Data Extraction
          ↓
    Digital Twin Update
          ↓
      Storage
```

### Patient Interaction Flow

```
Patient Question
       ↓
Load Digital Twin
       ↓
Build Context (Full Medical History)
       ↓
Generate System Prompt
       ↓
LLM Processing (with context)
       ↓
Response Generation
       ↓
Conversation History Update
       ↓
Display to Patient
```

## Security Considerations

### Data Privacy
- **Local Storage**: Patient data stored locally by default
- **Minimal Cloud Exposure**: Only processed text sent to OpenAI API
- **No PII in Logs**: Careful logging to avoid exposing patient information
- **Anonymized IDs**: Use patient IDs instead of names

### Safety Mechanisms
- **Disclaimer System**: Every response includes appropriate medical disclaimers
- **No Prescription Changes**: Explicitly warns against medication changes without doctor
- **Emergency Detection**: Encourages immediate medical attention for emergencies
- **Scope Limitations**: Clear about what the system can and cannot do

### Future Security Enhancements
- End-to-end encryption for stored data
- User authentication and authorization
- Audit logging for compliance
- HIPAA compliance measures
- Data retention policies

## LLM Integration

### Models Used
- **Primary**: GPT-4 (for complex medical reasoning)
- **Embeddings**: text-embedding-3-small (for potential RAG implementation)
- **Temperature Settings**:
  - 0.3 for extraction (consistency)
  - 0.7 for chat (natural conversation)

### Prompt Engineering

**Extraction Prompt Strategy:**
- Structured JSON output format
- Explicit field definitions
- Conservative extraction (only explicit information)
- Handling of uncertainty

**Chat Prompt Strategy:**
- Patient-specific context injection
- Clear role definition
- Safety guidelines
- Empathetic tone instructions

### Cost Optimization
- Conversation history truncation (keep last 10 exchanges)
- Efficient context building
- Batch processing where possible
- Model selection based on task complexity

## Scalability Considerations

### Current Limitations
- File-based storage (suitable for demo/small scale)
- Single-threaded processing
- In-memory conversation history

### Future Scalability Improvements
1. **Database Integration**: PostgreSQL or MongoDB for patient data
2. **Caching Layer**: Redis for conversation history
3. **API Architecture**: RESTful API for multi-client support
4. **Async Processing**: Queue-based transcript processing
5. **Load Balancing**: Multiple API instances
6. **Vector Database**: ChromaDB for semantic search over medical history

## Extension Points

### Adding New Features

1. **Voice Input**: 
   - Integrate speech recognition (SpeechRecognition library included)
   - Real-time transcription
   - Audio file upload

2. **Web Interface**:
   - Flask/FastAPI backend
   - React/Vue frontend
   - WebSocket for real-time chat

3. **Medical Knowledge Base**:
   - Integration with medical databases (PubMed, UpToDate)
   - RAG (Retrieval Augmented Generation) for evidence-based answers
   - Drug interaction checking

4. **Multi-language Support**:
   - Translation layer
   - Language detection
   - Localized medical terminology

5. **Healthcare Provider Portal**:
   - Review patient questions
   - Add structured data
   - Override/correct AI extractions

## Testing Strategy

### Unit Tests
- Model validation
- Data serialization/deserialization
- Service layer functionality

### Integration Tests
- End-to-end transcript processing
- Chat conversation flows
- Data persistence

### Mock Testing
- LLM API responses
- File system operations
- Error conditions

## Deployment Options

### Development
```bash
python app.py
```

### Production Considerations
1. **Environment Variables**: Proper secret management
2. **Process Management**: systemd, supervisor, or PM2
3. **Monitoring**: Logging, error tracking (Sentry)
4. **Database**: Migration to proper database
5. **Reverse Proxy**: nginx for web deployment
6. **SSL/TLS**: HTTPS for web interface
7. **Backup Strategy**: Regular data backups

## Compliance and Regulations

### Considerations for Medical Applications
- **HIPAA**: Health Insurance Portability and Accountability Act (US)
- **GDPR**: General Data Protection Regulation (EU)
- **Medical Device Regulations**: FDA, CE marking
- **Professional Standards**: Clinical decision support guidelines
- **Liability**: Clear disclaimers about non-diagnostic nature

**Current Status**: This is a demonstration/educational tool, NOT approved for clinical use.

## Performance Metrics

### Key Metrics to Monitor
- Transcript processing time
- Response latency
- Token usage (cost)
- Extraction accuracy
- User satisfaction
- System uptime

### Optimization Opportunities
- Prompt optimization for fewer tokens
- Model fine-tuning for medical domain
- Caching frequent queries
- Pre-computed summaries
