### **Independent Problem-Solving**  
**Use Case**: Encourages students to solve programming tasks independently by offering guidance that fosters critical thinking and conceptual understanding.  

#### **Tasks**  
- **Task 1**: Analyzes the student's task and question to identify the root issue or misunderstanding.  
- **Task 2**: Generates a response that aligns with academic integrity principles, using pseudocode and asking thought-provoking questions to guide the student toward the correct path.  

---  

#### **Experiment: Guiding Independent Problem-Solving**  

- **Input**: A student's query about a programming task (e.g., "I need to write a function that prints out numbers from an array. How do I do that?").  
- **Output**: A response that encourages the student to think critically about the problem and revisit fundamental programming concepts.  
- **Approach**: Focus on non-directive guidance to promote self-discovery and conceptual understanding.  
- **Message Flow**:  
  1. The student submits their query about the task.  
  2. The model analyzes the query to identify relevant programming concepts or potential misunderstandings.  
  3. The model generates a response that hints at the solution process without directly providing answers.  

- **Tools**: None.  
- **Models**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**:  
  - **Correctness**: Does the guidance effectively address the student's query?  
  - **Clarity**: Is the feedback clear, understandable, and encouraging?  
  - **Support for Independence**: Does the response promote independent thinking and reinforce conceptual understanding?   

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

| **Prompt**                                    | **Correctness** | **Clarity** | **Support for Independence** |  
|-----------------------------------------------|-----------------|-------------|------------------------------|  
| "Wie überprüfe ich, ob eine Zahl gerade oder ungerade ist?" | ✔️               | ✔️         | ✔️                           |  
| "Wie kann ich die Ausgabe von Zahlen in absteigender Reihenfolge erreichen?" | ✔️               | ✔️         | ✔️                           |  
| "Wie kann ich mehrere Bedingungen in einer `if`-Anweisung überprüfen?" | ✔️               | ✔️         | ✔️                           |  
| "Wie kann ich den folgenden Muster augeben?"              | ✔️               | 🟠         | ✔️                           |  
| "Wie gebe ich größte Zahl in Arrays aus?"   | ✔️               | ✔️         | ✔️                           |  
  
