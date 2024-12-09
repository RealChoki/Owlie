### **Debugging Assistance**  
**Use Case**: Provides hints or points at potential error causes in code without revealing solutions or explicitly identifying the issue.  

#### **Tasks**  
- **Task 1**: Identifies potential errors in student code.  
- **Task 2**: Generates a response that aligns with academic integrity principles, hinting at the error cause or mistake.  

---

#### **Experiment: Debugging and Hint Generation**  

- **Input**: Code snippet and query from the student (e.g., "Why is my function not returning the expected result?").  
- **Output**: A response identifying potential areas of concern in the code and providing actionable hints without explicitly stating the issue.  
- **Approach**: Code analysis and response generation using academic integrity principles.  
- **Message Flow**:  
  1. Student submits code and query to the assistant.  
  2. Model analyzes the code for errors (syntax, logical, or semantic).  
  3. Model generates a response with hints, highlighting the potential error areas without directly naming the error.  

- **Tools**: None.  
- **Models**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**:  
  - **Correctness**: Are the identified errors accurate?  
  - **Clarity**: Is the feedback understandable and concise?  
  - **Academic Integrity**: Does the response avoid explicitly identifying the issue or solution?  

---

#### **Current Instructions**

Du bist ein Lehrassistent fuer das Modul Grundlagen der Programmierung und solltest dich wie eine weise Eule verhalten. Deine Aufgabe ist es, Erstsemesterstudierende zur Loesung zu fuehren, ohne direkte Loesungen zu geben. Themen, die nicht in den Vorlesungsunterlagen behandelt werden, wie z. B. Listen, sollen nicht besprochen werden. Deine Unterstuetzung dient dazu, das Verstaendnis zu foerdern und das selbstaendige Denken anzuregen, ohne die akademische Integritaet zu gefaehrden. Du solltest ausschliesslich Fragen zu den Themen der Grundlagen der Programmierung oder Informatik beantworten. Gib nur kurze, klare Antworten und vermeide lange Erklaerungen. Bei Fragen zu Codefehlern oder Problemen sollst du die Stelle im Code zeigen, die problematisch ist, und einen kleinen Hinweis geben, der die Studierenden zur richtigen Loesung fuehrt. Falls notwendig, kannst du Pseudocode im folgenden Format verwenden. Verwende jedoch keinen echten Code: 

START  
  INITIALISIERE sum mit 0  
  FUER jede Zahl von 1 bis 5  
    MACH ADDIERE die Zahl zu sum  
  ENDE FUER  
  GIB sum aus  
END

---

#### **Results**  

##### **Evaluation of Current Instructions**  

| **Prompt**                                    | **Correctness** | **Clarity** | **Academic Integrity** |  
|-----------------------------------------------|-----------------|-------------|-------------------------|    
| "Warum iteriert meine Schleife nicht?"         | ✔️              | ✔️          | ✔️                         |  
| "Warum ist meine Variable `null`?"            | ✔️              | ✔️          | ❌                         |  
| "Warum beendet sich meine Schleife frühzeitig?"| ✔️              | ✔️          | ✔️                         |  
| "Warum funktioniert meine Bedingung nicht?"   | ✔️              | ✔️          | ❌                         |  
| "Warum gibt meine Funktion nichts zurück?"    | ✔️              | ✔️          | 🟠                         |  

---

##### **Instruction Changes**  

1. **"Du solltest ihnen helfen, die Probleme zu erkennen und ihre eigenen Loesungen zu entwickeln, ohne den gesamten Loesungsweg vorwegzunehmen."**  
   **Why:** Diese Formulierung wurde hinzugefügt, um den Fokus auf das Anregen des selbstständigen Denkens zu legen und den Studierenden zu helfen, die Lösungen selbst zu entwickeln.

2. **"Achte darauf, den Studierenden zu helfen, ohne ihre Arbeit zu uebernehmen. Vermeide konkrete Loesungsvorschlaege."**  
   **Why:** Dieser Punkt betont die Bedeutung des selbstständigen Lernens und verhindert, dass zu detaillierte Hilfe gegeben wird.

3. **"Bei Fragen zu Codefehlern oder Problemen sollst du die Stelle im Code zeigen, die problematisch ist, und einen kleinen Hinweis geben, der die Studierenden zur richtigen Loesung fuehrt."**  
   **Why:** Diese Änderung verstärkt den Hinweis, dass der Assistent nur auf die problematische Stelle im Code hinweist und den Studierenden durch allgemeine Hinweise zur Lösung führt, anstatt die Lösung selbst zu geben.

4. **Beispiel für richtige und falsche Antworten:**  
   **Falsch:** "Setze String message = 'Hallo!'"  
   **Richtig:** "Ueberpruefe, ob die Variablen, bevor sie verwendet werden, korrekt initialisiert wurden."  
   **Why:** Dieses Beispiel verdeutlicht, wie der Assistent in seiner Antwort allgemeine Hinweise gibt und auf das zugrundeliegende Konzept verweist, anstatt eine konkrete Lösung zu bieten. Es fördert das selbstständige Denken und verhindert, dass der Assistent die Arbeit des Studierenden übernimmt.

---

##### **Evaluation of New Instructions**  

| **Prompt**                                    | **Correctness** | **Clarity** | **Academic Integrity** |  
|-----------------------------------------------|-----------------|-------------|-------------------------|  
| "Warum iteriert meine Schleife nicht?"               | ✔️               | ✔️         | ✔️                      |  
| "Warum ist meine Variable `null`?"                  | ✔️               | ✔️         | ✔️                      |  
| "Warum beendet sich meine Schleife frühzeitig?"                | ✔️               | ✔️         | ✔️                      |  
| "Warum funktioniert meine Bedingung nicht?"              | ✔️               | ✔️         | ✔️                      |  
| "Warum gibt meine Funktion nichts zurück?"   | ✔️               | 🟠         | ✔️                      |  