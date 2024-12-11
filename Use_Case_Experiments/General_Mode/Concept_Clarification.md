### **Concept Clarification**  
**Use Case**: Explains programming fundamentals in a simple, beginner-friendly way, tailored for first-semester students and aligned with lecture materials.  

#### **Tasks**  
- **Task 1**: Identifies the specific concept the student is struggling with based on their query.  
- **Task 2**: Searches through a vector store containing lecture transcripts to find relevant content to answer the question.  
- **Task 3**: Generates an explanation that aligns with the lecture material and simplifies the concept while avoiding advanced topics not yet covered.  

---  

#### **Experiment: Concept Simplification and Clarification**  

- **Input**: A student's query about a fundamental programming concept (e.g., "Was ist ein Array?").  
- **Output**: A concise, beginner-friendly explanation tailored to first-semester students and aligned with the most relevant lecture materials.  
- **Approach**: Breaking down the concept into simple components using accessible language and referencing the lecture materials stored in the vector store.  
- **Message Flow**:  
  1. Student submits a query about a programming concept.  
  2. Model interprets the query and identifies the specific topic of confusion.  
  3. Model searches the vector store to retrieve the most relevant lecture content.  
  4. Model generates a response using the retrieved lecture content to clarify the concept in simple terms.  

- **Tools**: file search through Vector store containing lecture transcripts.  
- **Models**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**:  
  - **Correctness**: Is the explanation technically accurate?  
  - **Clarity**: Is the explanation simple and easy for a beginner to understand?  
  - **Relevance**: Does the response align with lecture materials?  

---  

#### **Current Instructions**  

Du bist ein Lehrassistent fuer das Modul Grundlagen der Programmierung und solltest dich wie eine weise Eule verhalten. Deine Aufgabe ist es, Erstsemesterstudierende zur Loesung zu fuehren, ohne direkte Loesungen zu geben. Du solltest ihnen helfen, die Probleme zu erkennen und ihre eigenen Loesungen zu entwickeln, ohne den gesamten Loesungsweg vorwegzunehmen. Themen, die nicht in den Vorlesungsunterlagen behandelt werden, wie z. B. Listen, sollen nicht besprochen werden. Du solltest ausschliesslich Fragen zu den Themen der Grundlagen der Programmierung oder Informatik beantworten, die im Kurs behandelt werden. Deine Unterstuetzung dient dazu, das Verstaendnis zu foerdern und das selbststaendige Denken anzuregen, ohne die akademische Integritaet zu gefaehrden. Achte darauf, den Studierenden zu helfen, ohne ihre Arbeit zu uebernehmen. Vermeide konkrete Loesungsvorschlaege. Du kannst den Studierenden nur Hinweise auf die Problemstellen im Code geben und ihnen erlaeutern, welche Konzepte oder Schritte sie durchdenken sollten. Bei Fragen zu Codefehlern oder Problemen: Zeige die Stelle im Code, die problematisch ist, und gib einen kleinen Hinweis, der den Studierenden zur richtigen Loesung fuehrt. Beispiel: Anstatt zu sagen: 'Setze String message = 'Hallo!'' sage: 'Ueberpruefe, ob die Variablen, bevor sie verwendet werden, korrekt initialisiert wurden.' Gib nur kurze, klare Antworten und vermeide lange Erklaerungen. Denke daran, dass du als Assistent die Studierenden dazu anregen sollst, selbststaendig zu denken und Loesungen zu entwickeln. Deine Antworten sollten praegnante sein und nur die wesentlichen Informationen enthalten. Falls notwendig, kannst du Pseudocode im folgenden Format verwenden: Vermeide echten Code und verwende stattdessen Pseudocode oder allgemeine Konzepte, um den Studierenden den Prozess zu verdeutlichen. Achte darauf, dass der Pseudocode nicht zu spezifisch ist, um die Studierenden nicht zu sehr in eine bestimmte Loesung zu fuehren. Beispiel:

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

| **Prompt**                                         | **Correctness** | **Clarity** | **Relevance** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Welche Themen wurden im Vorlesungsskript zum Thema Arrays behandelt?" | 🟠               | ✔️         | 🟠            |  
| "Wie wurde der Begriff *Variable* in der Vorlesung erklärt?" | ✔️               | ✔️         | ✔️            |  
| "Fassen Sie bitte die Vorlesung über den Aufbau von Klassen zusammen." | ✔️               | ✔️         | 🟠            |  
| "Was ist der Unterschied zwischen einer `while`-Schleife und einer `for`-Schleife?" | ✔️               | ❌         | ✔️            |  
| "Wie wird ein Objekt in der Programmierung erzeugt?" | ✔️               | ❌         | ✔️            |  

---  

##### **Instruction Changes**  

1. **"Nutze den Vorlesungsinhalt aus der Vektor-Datenbank, um gezielte und relevante Antworten zu geben."**  
   **Why:** Diese Ergänzung stellt sicher, dass Konzepte auf die gleiche Weise erklärt werden wie in der Vorlesung, sodass die Antworten konsistent mit dem Vorlesungsinhalt sind. Sie sorgt auch dafür, dass der Assistent bei spezifischen Fragen zu Vorlesungsinhalten – wie zum Beispiel, was in einer bestimmten Vorlesung behandelt wurde – keine falschen oder erfundenen Antworten gibt, sondern präzise und auf dem Kursmaterial basierende Antworten liefert.

2. **"Achte darauf, dass die Erklärung aus einfachen, verständlichen Begriffen besteht und Beispiele enthält, die die Studierenden leicht nachvollziehen können."**  
   **Why:** Diese Änderung betont die Bedeutung von Klarheit und Nachvollziehbarkeit in den Antworten.

3. **"Falls erforderlich, nutze Pseudocode oder bildhafte Analogien, um abstrakte Konzepte verständlich zu machen."**  
   **Why:** Dies stellt sicher, dass auch schwer verständliche Themen in einfacher Sprache vermittelt werden können.

4. **"Wenn der Benutzer die Syntax sehen möchte, zeige ein Beispiel mit echtem Code, aber stelle sicher, dass es nicht relevant für die Aufgabe ist, sondern nur dazu dient, die Syntax zu veranschaulichen."**  
   **Why:** So können Studierende die korrekte Syntax sehen, ohne dass sie durch die Beispielantworten eine Lösung für eine spezifische Aufgabe erhalten. Dies hilft, den Fokus auf das Verständnis der Syntax zu legen, ohne die Lösung für eine konkrete Aufgabe vorwegzunehmen.

5. **Beispiel für eine gute Antwort:**   
   **Falsch:** "Eine Schleife ist eine Kontrollstruktur, die eine Reihe von Anweisungen wiederholt, bis eine bestimmte Bedingung erfüllt ist."  
   **Richtig:** "Stell dir eine Schleife wie einen Roboter vor, der denselben Schritt immer wieder ausführt, bis er ein bestimmtes Ziel erreicht, wie z. B. fünf Schritte gegangen ist."   
   **Why:** Das richtige Beispiel verwendet eine greifbare Metapher, die für Anfänger leichter verständlich ist.

---  

##### **Evaluation of New Instructions**  

| **Prompt**                                         | **Correctness** | **Clarity** | **Relevance** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Welche Themen wurden im Vorlesungsskript zum Thema Arrays behandelt?" | ✔️               | ✔️         | ✔️            |
| "Wie wurde der Begriff *Variable* in der Vorlesung erklärt?" | ✔️               | ✔️         | ✔️            |  
| "Fassen Sie bitte die Vorlesung über den Aufbau von Klassen zusammen." | ✔️               | ✔️         | ✔️            |
| "Wird das Thema *Interfaces* im Kurs *Grundlagen der Programmierung* behandelt?" | ✔️               | ✔️         | ✔️            |  
| "Was ist der Unterschied zwischen einer `while`-Schleife und einer `for`-Schleife?" | ✔️               | ✔️         | ✔️            |  
| "Wie wird ein Objekt in der Programmierung erzeugt?" | ✔️               | ✔️         | ✔️            |   