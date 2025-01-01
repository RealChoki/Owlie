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
  - **Relevance**: Does the assistant appropriately handle queries outside the Moodle course's scope by notifying the student?  

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
| "Wann sind die Vorlesungen?"                | ❌               | ✔️         | ❌            |  
| "Welche aufgaben sind noch zu erledigen?" | ❌               | ✔️         | ❌            |  
| "Wer ist die Professorin von den Kurs?"     | ✔️               | ✔️         | ✔️            |  

---  

#### **Instruction Changes**  

1. **"Limit answers strictly to Moodle resources. If a query extends beyond the approved material, explain politely and redirect students as needed."**  
- **Why:** To ensure responses remain accurate and aligned with the course's intended learning outcomes.  

2. **"Use the Moodle API to retrieve specific data when available, such as assignment deadlines or detailed lecture notes."**  
- **Why:** Provides students with timely and precise information.  

3. **"Encourage students to refer to specific sections of Moodle materials for in-depth learning, ensuring they utilize the provided resources effectively."**  
- **Why:** Reinforces the habit of using course materials and fosters independent learning.  

4. **"Avoid answers that imply knowledge beyond the scope of the course or Moodle materials, keeping responses relevant to the curriculum."**  
- **Why:** Helps maintain focus on the course's intended objectives and avoids confusing students with extraneous information.  

---  

#### **Evaluation of New Instructions**  

| **Prompt**                                             | **Correctness** | **Clarity** | **Relevance** |  
|--------------------------------------------------------|-----------------|-------------|---------------|  
| "What is the deadline for Assignment 2?"               | ✔️               | ✔️         | ✔️            |  
| "Can you explain the recursion examples in Lecture 3?" | ✔️               | ✔️         | ✔️            |  
| "What are advanced sorting algorithms?"                | ✔️               | ✔️         | ✔️            |  
| "Can you help me solve a programming problem unrelated to the course?" | ✔️               | ✔️         | ✔️            |  
| "Where can I find more information about hashing?"     | ✔️               | ✔️         | ✔️            |  