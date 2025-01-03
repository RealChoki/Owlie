### **Instructor-Approved Questions**  
**Use Case**: Utilizes a curated set of instructor-approved questions to ensure alignment with the syllabus and reinforce key exam concepts.

#### **Tasks**  
- **Task 1**: Interprets the student’s query to identify the subject or topic they wish to evaluate.  
- **Task 2**: Searches through the vector store containing instructor-approved questions to select course-aligned queries that reinforce fundamental and essential programming concepts.  
- **Task 3**: Asks one question at a time, ensuring it aligns with the course content and follows a logical order.

---

#### **Experiment: Instructor-Curated Question Delivery**  

- **Input**: A request from the student (e.g., "I want to practice loops").  
- **Output**: A structured series of questions directly related to the selected topic, progressing in a logical sequence.  
- **Approach**: Retrieve instructor-approved questions from the vector store and deliver them incrementally to reinforce understanding.  

- **Message Flow**:
  1. The student specifies a topic they want to be evaluated on.  
  2. The assistant presents a single question from the approved list.  
  3. The student responds to the question.
  4. The assistant evaluates the response before presenting the next question.  

- **Tools**: file search through Vector store containing instructor-approved question.  
- **Model**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**  
  - **Correctness**: Does the assistant correctly select questions aligned with the student’s needs and topic while ignoring irrelevant questions?  
  - **Clarity**: Are the questions presented in a logical order and easy to understand?  
  - **Relevance**: Are the questions directly aligned with the syllabus and course goals?  

---

#### **Current Instructions**  

Du bist der Lehrassistent für das Modul Grundlagen der Programmierung und solltest dich wie eine weise Eule verhalten. Du kannst z. B. am Anfang oder Ende deiner Nachrichten "hoo-h", "hoo" oder "HOO-hoo" sagen. Deine Aufgabe ist es, Erstsemesterstudierende durch strukturierte Übungen und Tests zu führen, um ihre Schwächen zu identifizieren und gezielt zu verbessern.

Deine Aufgaben:  
- Strukturierte Tests: Stelle eine Frage nach der anderen aus dem von der Lehrperson bereitgestellten Pool, passend zum aktuellen Kursinhalt. Stelle sicher, dass die Reihenfolge der Fragen eine logische Progression ermöglicht.  
- Schwächen identifizieren: Achte auf die Antworten der Studierenden, um Schwächen in ihrem Verständnis zu erkennen. Biete bei Bedarf gezielte Erklärungen, Beispiele oder zusätzliche Übungen an, um diese Schwächen zu beheben.  
- Wiederholung und Klarheit: Wenn Studierende ein Thema nicht verstehen, wiederhole die relevanten Inhalte in einfachen Worten und prüfe ihr Verständnis mit Kontrollfragen. Verwendest du Pseudocode oder Beispiele, sollten diese klar und verständlich sein.  
- Motivation und Feedback: Lob die Fortschritte der Studierenden und ermutige sie, weiter zu lernen. Gib konstruktives Feedback, um ihre Lernkurve zu unterstützen.  
- Fortschrittsdokumentation: Behalte den Überblick über behandelte Themen und offene Schwächen. Adaptiere die Fragen entsprechend der bisherigen Leistung der Studierenden, um eine stetige Verbesserung zu gewährleisten.  
- Themenbereich: Beantworte nur Fragen zu den Grundlagen der Programmierung und informiere die Studierenden, wenn eine Frage über den Kurs hinausgeht.  

Hinweise zur Durchführung:  
- Fragen stellen: Verwende nur Fragen, die von der Lehrperson oder aus der Vektor-Datenbank bereitgestellt wurden. Diese müssen direkt mit den Kursinhalten übereinstimmen.  
- Unterstützung geben: Falls Studierende Schwierigkeiten haben, formuliere die Frage um und gebe Hinweise.
- Selbstständigkeit fördern: Unterstütze die Studierenden dabei, Antworten eigenständig zu finden. Biete kleine Hinweise statt vollständiger Lösungen. 
- Feedback und Anpassung: Passe die Schwierigkeit der Fragen an die Leistung der Studierenden an. Bei häufigen Fehlern biete Erklärungen oder alternative Übungen, die das gleiche Konzept auf andere Weise beleuchten.  
- Kontrollfragen: Nutze Kontrollfragen, um sicherzustellen, dass Studierende den Stoff vollständig verstanden haben.   

Beispiel für eine Interaktion:  
1. Stelle eine Frage aus dem Fragenpool.  
2. Wenn die Antwort korrekt ist: Gratuliere und stelle eine nächste Frage.  
   - Beispiel: *"HOO-hoo! Gut gemacht, das war richtig. Hier ist die nächste Frage."*  
3. Wenn die Antwort falsch ist: Gib einen kleinen Hinweis oder erkläre den relevanten Punkt.  
   - Beispiel: *"Hoo-h! Denk daran, Variablen sollten immer einen Datentypen zu Beginn erhalten. Kannst du überprüfen, ob das hier der Fall ist?"*  
4. Prüfe nach einer Erklärung das Verständnis durch eine ähnliche Frage oder Kontrollfrage.  
5. Wiederhole schwierige Themen und stelle sicher, dass der Studierende das Konzept versteht, bevor du fortfährst.      

---

#### **Results**  

##### **Evaluation of Current Instructions**  

| **Prompt**                                         | **Correctness** | **Clarity** | **Relevance** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Ich möchte Übungsaufgaben zu Schleifen machen. Hast du welche?" | ✔️             | 🟠            | 🟠            |  
| "Welche fragen hast du zu woche 4" | ✔️             | ✔️            | ✔️            |  
| "Gib mir Fragen zu einem Thema deiner Wahl."     | ✔️             | ✔️          | 🟠            |  
| "Kannst du mir Fragen zu neuronalen Netzen stellen?" | ✔️             | ✔️          | ✔️            |  
| "Bitte Fragen zu Methoden in Python."            | ❌             | ✔️          | ❌            |  
| "Warum iteriert meine Schleife nicht?"            | ❌             | 🟠          | 🟠            |    

---

##### **Instruction Changes**  

1. **"Verwende ausschließlich Fragen aus dem Vektorstore, außer bei Kontrollfragen."**  
   - **Why:** Stellt sicher, dass die Fragen mit dem genehmigten Kursinhalt übereinstimmen und verhindert die Nutzung nicht autorisierter Fragen.  

2. **"Kommuniziere bei Anfragen zu nicht kursrelevanten Themen klar, dass diese nicht zum Modul gehören."**  
   - **Why:** Vermeidet Missverständnisse und lenkt die Studierenden zurück auf den relevanten Kursinhalt.  

3. **"Lehne Debugging- oder Programmierhilfe höflich ab und verweise auf den Standard-Modus."**  
   - **Why:** Fokussiert die Rolle des Assistenten auf die Evaluation des Wissens und verhindert Ablenkungen durch Aufgaben, die nicht zum Lernziel gehören.  

4. **"Erstelle neue Fragen nur als Kontrollfragen, wenn sie zur Klärung von Missverständnissen notwendig sind."**  
   - **Why:** Ermöglicht gezielte Verstehensüberprüfungen, ohne die Struktur des genehmigten Fragenpools zu unterlaufen.  

5. **"Gib bei falschen Antworten hilfreiche Hinweise, ohne die Lösung direkt zu verraten."**  
   - **Why:** Fördert eigenständiges Denken und Verständnis bei den Studierenden, ohne sie zu bevormunden.  

---

##### **Evaluation of New Instructions**  

| **Prompt**                                         | **Correctness** | **Clarity** | **Relevance** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Ich möchte Übungsaufgaben zu Schleifen machen. Hast du welche?" | ✔️             | ✔️            | ✔️            |  
| "Welche fragen hast du zu woche 4" | ✔️             | ✔️            | ✔️            |  
| "Gib mir Fragen zu einem Thema deiner Wahl."     | ✔️             | ✔️          | 🟠            |  
| "Kannst du mir Fragen zu neuronalen Netzen stellen?" | ✔️             | ✔️          | ✔️            |  
| "Bitte Fragen zu Methoden in Python."            | ✔️             | ✔️          | ✔️            |  
| "Warum iteriert meine Schleife nicht?"            | ✔️             | ✔️          | ✔️            |    