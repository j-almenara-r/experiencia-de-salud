# Experiencia de Salud - Medical Patient Chatbot

Un chatbot especializado basado en LLM para pacientes médicos que crea gemelos digitales mediante el análisis de consultas médicas y responde preguntas en tiempo real para ayudar a los pacientes a tomar decisiones informadas.

## 🎯 Descripción

Este proyecto implementa un sistema de chatbot médico inteligente que:

1. **Escucha a los médicos**: Procesa transcripciones de consultas médicas
2. **Crea gemelos digitales**: Construye perfiles completos de pacientes con toda su información médica estructurada
3. **Responde preguntas**: Proporciona asistencia en tiempo real a los pacientes para ayudarles a tomar decisiones informadas sobre su salud

## ✨ Características

- 🏥 **Procesamiento de transcripciones médicas**: Extrae automáticamente información estructurada de las conversaciones médico-paciente
- 👤 **Gemelos digitales de pacientes**: Mantiene perfiles completos con condiciones médicas, medicamentos, alergias e historial de consultas
- 💬 **Chatbot conversacional**: Interfaz de chat para que los pacientes obtengan respuestas sobre su información médica
- 🔒 **Enfoque en privacidad**: Almacenamiento local de datos con consideraciones de seguridad
- 🧠 **Contexto inteligente**: Utiliza todo el historial médico del paciente para proporcionar respuestas precisas y personalizadas
- 📊 **Resúmenes médicos**: Genera resúmenes comprensivos automáticamente
- 💡 **Preguntas sugeridas**: Propone preguntas relevantes basadas en la información del paciente

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- Clave API de OpenAI

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/j-almenara-r/experiencia-de-salud.git
cd experiencia-de-salud
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY
```

4. Ejecutar la aplicación:
```bash
python app.py
```

## 📖 Uso

### Interfaz de Línea de Comandos

La aplicación proporciona un menú interactivo con las siguientes opciones:

1. **Crear/Cargar Paciente**: Inicializa o carga un gemelo digital de paciente
2. **Añadir Transcripción de Consulta**: Procesa una nueva transcripción médica
3. **Chat con Asistente**: Inicia una sesión de chat para hacer preguntas
4. **Ver Información del Paciente**: Muestra el perfil completo del paciente
5. **Listar Todos los Pacientes**: Ve todos los pacientes registrados

### Ejemplo de Flujo de Trabajo

```python
from src.services import TranscriptProcessor, PatientChatbot, DigitalTwinManager

# Inicializar servicios
twin_manager = DigitalTwinManager()
processor = TranscriptProcessor()
chatbot = PatientChatbot()

# Crear o cargar gemelo digital
digital_twin = twin_manager.get_or_create_digital_twin("patient_001")

# Procesar transcripción médica
transcript = """
Doctor: Buenos días. Veo que tiene diabetes tipo 2.
Paciente: Sí, me la diagnosticaron hace dos años.
Doctor: Le voy a prescribir metformina 500mg, dos veces al día.
Paciente: ¿Tiene efectos secundarios?
Doctor: Puede tener molestias estomacales al principio...
"""

extracted_data = processor.process_transcript(
    transcript=transcript,
    doctor_specialty="Endocrinología"
)

digital_twin = processor.update_digital_twin(digital_twin, extracted_data)
twin_manager.save_digital_twin(digital_twin)

# Chatear con el asistente del paciente
response = chatbot.chat(
    patient_id="patient_001",
    digital_twin=digital_twin,
    user_message="¿Qué medicamentos estoy tomando y para qué sirven?"
)
print(response)
```

## 🏗️ Arquitectura

### Componentes Principales

1. **Digital Twin Model** (`src/models/digital_twin.py`)
   - Define la estructura de datos para gemelos digitales de pacientes
   - Gestiona condiciones médicas, medicamentos, alergias y consultas

2. **Transcript Processor** (`src/services/transcript_processor.py`)
   - Procesa transcripciones médicas usando LLM
   - Extrae información estructurada
   - Actualiza gemelos digitales

3. **Patient Chatbot** (`src/services/chatbot.py`)
   - Proporciona interfaz conversacional
   - Mantiene contexto de la conversación
   - Genera respuestas personalizadas

4. **Digital Twin Manager** (`src/services/digital_twin_manager.py`)
   - Gestiona almacenamiento y recuperación de gemelos digitales
   - Maneja persistencia de datos

## 🔒 Seguridad y Privacidad

- **Almacenamiento local**: Todos los datos se almacenan localmente por defecto
- **Sin datos en la nube**: Las transcripciones procesadas solo se envían a la API de OpenAI para procesamiento
- **Identificación anónima**: Usa IDs de pacientes en lugar de información personal
- **Advertencias claras**: El chatbot siempre aclara que proporciona información, no consejo médico

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=src tests/
```

## 📝 Estructura del Proyecto

```
experiencia-de-salud/
├── app.py                          # Aplicación principal CLI
├── requirements.txt                # Dependencias de Python
├── .env.example                    # Plantilla de configuración
├── README.md                       # Esta documentación
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── digital_twin.py        # Modelos de datos
│   ├── services/
│   │   ├── __init__.py
│   │   ├── transcript_processor.py # Procesamiento de transcripciones
│   │   ├── chatbot.py             # Servicio de chatbot
│   │   └── digital_twin_manager.py # Gestión de gemelos digitales
│   └── utils/
│       └── __init__.py
├── tests/                          # Tests unitarios
└── data/                           # Almacenamiento de datos (creado automáticamente)
    └── digital_twins/              # Gemelos digitales de pacientes
```

## 🛣️ Roadmap

- [ ] Interfaz web con Flask/FastAPI
- [ ] Procesamiento de audio en tiempo real para transcripciones
- [ ] Integración con sistemas EMR/EHR
- [ ] Soporte multiidioma
- [ ] Mejoras en privacidad y cifrado
- [ ] Panel de control para profesionales médicos
- [ ] Exportación de informes para pacientes
- [ ] Integraciones con dispositivos de salud

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## ⚠️ Aviso Legal

Este software es solo para fines demostrativos y educativos. NO es un dispositivo médico ni debe usarse para diagnóstico o tratamiento. Los pacientes siempre deben consultar con profesionales médicos calificados para decisiones relacionadas con su salud.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 👥 Autores

- José Almenara

## 🙏 Agradecimientos

- OpenAI por proporcionar la tecnología LLM
- La comunidad de código abierto por las herramientas y bibliotecas