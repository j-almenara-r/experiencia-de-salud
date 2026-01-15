# Example Medical Consultation Transcripts

These examples can be used to test the transcript processing functionality.

## Example 1: Initial Diabetes Consultation

```
Doctor: Buenos días, señor García. He revisado sus análisis de sangre.
Paciente: Buenos días, doctor. ¿Cómo están los resultados?
Doctor: Sus niveles de glucosa están elevados. Su hemoglobina A1c está en 7.2%, lo cual indica diabetes tipo 2.
Paciente: Oh, vaya. ¿Es grave?
Doctor: Es manejable con tratamiento adecuado. Voy a prescribirle metformina 500mg, tome una tableta dos veces al día con las comidas.
Paciente: ¿Tiene efectos secundarios?
Doctor: Puede experimentar molestias estomacales al principio, pero suelen desaparecer. Tome la medicación con alimentos para minimizar esto.
Paciente: Entiendo. ¿Hay algo más que deba hacer?
Doctor: Sí, es importante que controle su dieta - reduzca los carbohidratos simples y azúcares. También le recomiendo 30 minutos de ejercicio moderado al día.
Paciente: De acuerdo.
Doctor: Quiero verle de nuevo en tres meses para monitorear sus niveles. También necesitará hacerse análisis de sangre una semana antes de esa cita.
Paciente: Perfecto, lo anotaré.
Doctor: ¿Tiene alguna alergia a medicamentos?
Paciente: Soy alérgico a la penicilina.
Doctor: Bien, lo anoto en su expediente. ¿Alguna otra pregunta?
Paciente: No, creo que está todo claro. Gracias.
```

## Example 2: Hypertension Follow-up

```
Doctor: Good afternoon, Mrs. Johnson. How have you been feeling on the blood pressure medication?
Patient: Much better, doctor. The headaches have stopped.
Doctor: Excellent. Let me check your blood pressure today... 128 over 82. That's a significant improvement from 150 over 95 last month.
Patient: That's great news!
Doctor: Yes. The lisinopril 10mg once daily is working well for you. Continue taking it every morning.
Patient: I have been taking it consistently.
Doctor: Good. Any side effects? Dizziness, dry cough?
Patient: No, none at all.
Doctor: Perfect. Have you been monitoring your sodium intake as we discussed?
Patient: Yes, I've been cooking at home more and reading labels.
Doctor: Excellent. Keep up with that. Also, how's the walking routine?
Patient: I'm walking about 20 minutes most days.
Doctor: Try to increase that to 30 minutes daily if possible. It will help maintain healthy blood pressure levels.
Patient: I'll work on that.
Doctor: Great. Let's see you again in two months, and continue the same medication regimen.
```

## Example 3: Multi-condition Management

```
Doctor: Hello, Mr. Patel. Let's review how things are going with your conditions.
Patient: Hello, doctor.
Doctor: First, your type 2 diabetes. Your last A1c was 6.8%, down from 7.5%. The metformin 1000mg twice daily is working well.
Patient: That's good to hear.
Doctor: For your hypertension, I'm seeing good control with the current combination - amlodipine 5mg and losartan 50mg, both once daily.
Patient: Yes, I take them both in the morning.
Doctor: Good. Now, I'm concerned about your cholesterol. Your LDL is at 160. I'd like to start you on atorvastatin 20mg, take it before bedtime.
Patient: Is that necessary?
Doctor: Given your diabetes and hypertension, elevated cholesterol increases your cardiovascular risk. This medication will help reduce that risk significantly.
Patient: Okay, I understand.
Doctor: Any issues with the medications? No muscle pain or digestive problems?
Patient: No, everything has been fine.
Doctor: Excellent. Continue monitoring your blood glucose at home. I want to see you in three months with updated blood work.
Patient: Will do.
```

## Example 4: Allergy and New Symptoms

```
Doctor: Hi Sarah, I see you're here about some new symptoms?
Patient: Yes, I've been having trouble breathing and my chest feels tight.
Doctor: When did this start?
Patient: About a week ago, especially when I'm outside.
Doctor: Have you had allergies before?
Patient: Not that I know of.
Doctor: Given the season and your symptoms, this looks like seasonal allergies - allergic rhinitis. I'm going to prescribe cetirizine 10mg, take one tablet daily.
Patient: Will that help with the breathing?
Doctor: Yes, it should. If symptoms persist after a week, we may add a nasal spray. Also, try to stay indoors on high pollen days and use air conditioning.
Patient: Okay. Is there anything I should avoid?
Doctor: If you notice the antihistamine makes you drowsy, take it at bedtime instead. Also, are you allergic to any medications?
Patient: I had a reaction to amoxicillin once - got a rash.
Doctor: Good to know. I'll note that as a penicillin allergy. This medication is safe for you.
Patient: Thank you, doctor.
```

## Example 5: Post-Surgery Follow-up

```
Doctor: Good morning, Tom. How's the knee feeling after the surgery?
Patient: Much better, though still a bit stiff.
Doctor: That's normal at this stage. Let me examine it... The incision is healing nicely, no signs of infection.
Patient: That's a relief.
Doctor: Continue taking the ibuprofen 400mg three times daily for pain and inflammation. You should take it with food.
Patient: I've been doing that.
Doctor: Good. Now, are you doing the physical therapy exercises?
Patient: Yes, twice a day as instructed.
Doctor: Excellent. Keep that up. The stiffness will improve with continued therapy. You should start feeling significant improvement in about two weeks.
Patient: When can I go back to work?
Doctor: You can return to desk work next week, but no heavy lifting for at least six weeks.
Patient: Understood.
Doctor: Any pain that's not controlled by the ibuprofen?
Patient: No, it's manageable.
Doctor: Great. I want to see you again in four weeks. If you notice any increased redness, swelling, or discharge from the incision, call the office immediately.
Patient: Will do. Thanks, doctor.
```

## Usage Instructions

To use these examples:

1. Copy the transcript text (without the language tags)
2. Run the application: `python app.py`
3. Select option 1 to create/load a patient
4. Select option 2 to add a consultation transcript
5. Paste the transcript
6. Type "END" on a new line
7. Enter the doctor's specialty (or use the default)

After processing, you can use option 3 to chat with the assistant about the information extracted from the consultation.
