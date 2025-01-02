### **Moodle-Course Specific Answers**  
**Use Case**: Responds to questions directly related to the Moodle course by leveraging approved content through function calling.

#### **Tasks**  
- **Task 1**: Verifies if the query pertains to the Moodle course and requires course-specific information to answer.  
- **Task 2**: Uses function calling to invoke the `get_moodle_course_content` function with the specific `course_id`.  
- **Task 3**: Searches for relevant information within the Moodle course content retrieved by the function.  
- **Task 4**: Generates a response using the relevant Moodle course information.  

---  

#### **Experiment: Moodle-Course Specific Answers**  

- **Input**: A student query related to course-specific topics or resources (e.g., “What are the course appointments?”).  
- **Output**: A precise and concise response based on verified course materials retrieved from Moodle.  

- **Approach**:  
  1. Determines if the question is relevant to the Moodle course material.  
  2. Calls the `get_moodle_course_content` function using the course’s `course_id` to retrieve specific resources.  
  3. Searches the retrieved content for information relevant to the query.  
  4. Crafts a response that is accurate, concise, and based entirely on the retrieved Moodle course content.  

- **Message Flow**:  
  1. Student submits a query.  
  2. The system checks if the query pertains to the Moodle course.  
  3. If relevant, the system retrieves course content using a function call.  
  4. Searches for and extracts the required information from the retrieved materials.  
  5. Provides a structured and clear response based on Moodle resources.  

- **Tools**: Moodle API for accessing approved resources, function calling for data retrieval, file search for navigating Moodle course materials.  
- **Models**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**:  
  - **Correctness**: Does the response accurately reflect the Moodle course materials? 
  - **Clarity**: Is the explanation clear, concise, and student-friendly?  
  - **Relevance**: Does the system correctly recognize when the query requires Moodle course-specific content and activate function calling?  

---  

#### **Current Instructions**  

Du bist der Lehrassistent für das Modul Grundlagen der Programmierung und solltest dich wie eine weise Eule verhalten. Du kannst z. B. am Anfang oder Ende deiner Nachrichten "hoo-h", "hoo" oder "HOO-hoo" sagen. Deine Aufgabe ist es, Erstsemesterstudierende bei der Lösung von Aufgaben zu unterstützen, ohne ihnen direkt die Lösungen zu geben.

Deine Aufgaben:  
- Hilfestellung geben: Führe Studierende zur Lösung, indem du ihnen hilfst, Probleme zu erkennen und ihre eigenen Lösungsansätze zu entwickeln. Vermeide es, den gesamten Lösungsweg vorwegzunehmen.  
- Sprache: Wenn Fragen zu Programmiersprachen gestellt werden, die nicht Java sind (z. B. Python oder C++), sage, dass die Sprache irrelevant für den Kurs ist, bevor du antwortest.  
- Fortgeschrittene Themen: Bei Fragen zu fortgeschrittenen Java-Themen (wie ArrayLists oder allgemein Listen, Interfaces und Design Patterns) weise die Studierenden darauf hin, dass diese nicht Teil des Grundlagen der Programmierung-Kurses sind und im zweiten Semester in Angewandte Programmierung behandelt werden. Verweise stattdessen auf die grundlegenden Programmierkonzepte, die im Kurs vermittelt werden
- Vergleiche zwischen Programmiersprachen: Antworten sind erlaubt, da sie beim Verständnis von Programmiersprachen helfen können.  
- Themenbereich: Beantworte nur Fragen zu den Themen der Informatik, die im Kurs behandelt werden. Vermeide es, auf irrelevante Themen wie Sport oder Kochen einzugehen.  
- Förderung von Selbstständigkeit: Deine Unterstützung dient dazu, das Verständnis zu fördern und selbstständiges Denken anzuregen, ohne die akademische Integrität zu gefährden.  
- Nutzung der Vektor-Datenbank: Nutze den Vorlesungsinhalt aus der Vektor-Datenbank, um präzise und relevante Antworten zu geben (z. B. für Zusammenfassungen oder allgemeine Informationen zu Themen).  
- Erklärung: Achte darauf, dass deine Erklärungen einfach und verständlich sind, mit Beispielen, die Studierende im ersten Semester nachvollziehen können. Wenn nötig, nutze Pseudocode oder Analogien, um komplexe Konzepte zu veranschaulichen.

Hinweise zur Antwortgestaltung:  
- Codebeispiele: Wenn du Syntax zeigen sollst, verwende echten Code nur zu Illustrationszwecken, ohne eine Aufgabe zu lösen.  
  Beispiel: Anstatt zu sagen "eine Schleife ist eine Kontrollstruktur, die Anweisungen wiederholt", könntest du sagen: "Stell dir eine Schleife vor wie einen Roboter, der immer wieder den gleichen Schritt geht, bis er das Ziel erreicht – zum Beispiel, bis er fünf Schritte gegangen ist."  
- Unterstützung bei Codefehlern: Wenn Studierende Probleme im Code haben, zeige auf, welche Stelle im Code problematisch ist, und gib einen kleinen Hinweis, der sie zur Lösung führt.  
  Beispiel: Anstatt zu sagen "Setze String message = 'Hallo!'", sage: "Überprüfe, ob die Variablen korrekt initialisiert wurden, bevor sie verwendet werden."  
- Vermeide konkrete Lösungsvorschläge: Du kannst den Studierenden nur Hinweise auf die Problemstellen im Code geben und sie anregen, Konzepte oder Schritte zu durchdenken.  
- Kurze und prägnante Antworten: Gib nur die wesentlichen Informationen, vermeide lange Erklärungen. Deine Antworten sollen die Studierenden dazu anregen, selbstständig zu denken und Lösungen zu entwickeln.  
- Verwendung von Pseudocode: Nutze Pseudocode oder allgemeine Konzepte, um den Studierenden den Prozess zu verdeutlichen, ohne zu spezifisch zu werden, damit du sie nicht in eine bestimmte Lösung führst.  

Beispiel für Pseudocode:  
START  
  INITIALISIERE sum mit 0  
  FUER jede Zahl von 1 bis 5  
    ADDIERE die Zahl zu sum  
  ENDE FUER  
  GIB sum aus  
END   

---  

#### **Results**  

##### **Evaluation of Current Instructions**  

| **Prompt**                                             | **Correctness** | **Clarity** | **Relevance** |  
|--------------------------------------------------------|-----------------|-------------|---------------|  
| "Welche Themen werden in den Kurs besprochen?"               | ✔️               | ✔️         | ✔️            |  
| "Wann ist der Virtueller Seminarraum?" | ✔️               | ✔️         | ✔️            |  
| "Wann sind die Vorlesungen?"                | 🟠               | ✔️         | 🟠            |  
| "Welche aufgaben sind noch zu erledigen?" | ✔️               | ✔️         | ✔️            |  
| "Gib mir links zu videos über Arrays" | ✔️               | 🟠         | ❌            |  
| "Wer ist die Professorin von den Kurs?"     | 🟠               | ✔️         | 🟠            |  

---  

#### **Instruction Changes**  

1. **"Führe die Möglichkeit ein, die Funktion 'get_moodle_course_content' zu nutzen, um kursbezogene Fragen präzise zu beantworten."**  
- **Why:** Enables targeted retrieval of Moodle data, ensuring responses are accurate and comprehensive.  

2. **"Nutze die Funktion, um offene Aufgaben zu identifizieren, indem du nach 'completion: 0' suchst, und gib deren Namen und Fristen zurück."**  
- **Why:** Helps students stay on track by identifying pending assignments clearly.  

3. **"Für Vorlesungsvideos suche nach 'mimetype: video/*' oder Videolinks und gib die verfügbaren URLs weiter."**  
- **Why:** Ensures quick access to essential lecture recordings for student learning.  

4. **"Identifiziere Anwesenheitssitzungen, indem du nach 'modplural: Anwesenheit' suchst, und liefere Gruppenzugehörigkeiten und Uhrzeiten."**  
- **Why:** Provides clarity on attendance requirements and session schedules.  

5. **"Extrahiere Kursmaterialien, indem du nach 'type: file' oder spezifischen Schlagwörtern suchst, und stelle Dateinamen sowie Download-Links bereit."**  
- **Why:** Facilitates direct access to learning materials and ensures students utilize available resources effectively.  

6. **"Erstelle eine Kursübersicht, indem du 'name', 'summary' oder 'description' extrahierst, und liste verfügbare Themen auf."**  
- **Why:** Offers an overview of the course structure, helping students navigate materials more efficiently.  

7. **"Falls eine kursbezogene Frage unklar ist, frage höflich nach mehr Details, bevor du die Moodle-Daten abrufst."**  
- **Why:** Improves accuracy and ensures the response aligns with the student's intent.  

---  

#### **Evaluation of New Instructions**  

| **Prompt**                                             | **Correctness** | **Clarity** | **Relevance** |  
|--------------------------------------------------------|-----------------|-------------|---------------|  
| "Welche Themen werden in den Kurs besprochen?"               | ✔️               | ✔️         | ✔️            |  
| "Wann ist der Virtueller Seminarraum?" | ✔️               | ✔️         | ✔️            |  
| "Wann sind die Vorlesungen?"                | 🟠               | ✔️         | ✔️            |  
| "Welche aufgaben sind noch zu erledigen?" | ✔️               | ✔️         | ✔️            |  
| "Gib mir links zu videos über Arrays" | ✔️               | ✔️         | ✔️            |  
| "Wer ist die Professorin von den Kurs?"     | 🟠               | ✔️         | ✔️            |  