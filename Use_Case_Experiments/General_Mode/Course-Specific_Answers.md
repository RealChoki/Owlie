### **Course-Specific Answers**  
**Use Case**: Offers information tied strictly to course content, avoiding irrelevant or advanced topics.

#### **Tasks**  
- **Task 1**: Determines if the query is relevant to the course material. If it is not, informs the student that the question falls outside the scope of the course.  
- **Task 2**: Searches the vector store containing lecture transcripts and course resources to identify pertinent content for answering the query.  
- **Task 3**: Crafts responses that strictly reflect course coverage, avoiding speculation or introducing topics beyond the course's scope.  

---  

#### **Experiment: Focusing on Course-Specific Answers**  

- **Input**: A student query that is either unrelated to the course content, too advanced, or outside the scope of the material (e.g., "Was sind Interfaces?", "Wie mache ich Pfannkuchen?").  
- **Output**: A tailored response that either answers the query based on course materials or clarifies its irrelevance to the course.  
- **Approach**:  
  1. Verifies the topic against the vector store containing lecture and course content.  
  2. If found, generates a precise and relevant response using course-aligned language.  
  3. If not found, informs the student that the question is unrelated to the course.  

- **Message Flow**:  
  1. Student submits a query.  
  2. The system identifies if the query pertains to the course.  
  3. Searches the vector store for relevant lecture material.  
  4. Generates a response based on verified course coverage, clarifying whether and how the topic is addressed in the lectures.  

- **Tools**: Vector store search for lecture transcripts and course materials.  
- **Models**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**:  
  - **Correctness**: Does the response accurately represent the course material?  
  - **Clarity**: Is the explanation clear and student-friendly?  
  - **Relevance**: Does the response align strictly with the course material?  

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
| "Könnten Sie mir bitte ein Rezept für Pfannkuchen geben?"                | ✔️               | ✔️         | ✔️            |  
| "Was sind Interfaces, und wie werden sie verwendet?" | ❌               | ✔️         | ❌            |  
| "Was ist ein Singleton, und wie wird er verwendet?" | ❌               | 🟠         | ❌            |  
| "Wie erstellt man Python-Dictionaries?"           | ❌               | ✔️         | ❌            |  
| "Wie sieht eine schleife in Python zum vergleich zu Java?"           | 🟠               | ✔️         | ❌            |  
| "Wie fügt man eine Zahl in ein Array ein oder entfernt sie?" | ✔️               | ✔️         | ✔️            |  
| "Warum ist eine `ArrayList` im Vergleich zu Arrays vorteilhafter?" | ❌               | ✔️         | ❌            |    

---  

#### **Instruction Changes**  

1. **"Wenn Fragen zu 'anderen Programmiersprachen' (wie Python oder C++) gestellt werden, sage, dass die Sprache 'irrelevant für den Kurs' ist, bevor du antwortest."**
- **Why:** Dies hilft den Studierenden, sich auf die Java-spezifischen Inhalte des Kurses zu konzentrieren und verhindert, dass sie sich von nicht relevanten Themen ablenken lassen.

2. **"Bei Fragen zu 'fortgeschrittenen Java-Themen' (wie Interfaces, Listen oder Design Patterns), erinnere die Studierenden daran, dass diese Themen 'nicht Teil des Grundlagen der Programmierung-Kurses' sind, sondern im 'zweiten Semester' in 'Angewandte Programmierung' behandelt werden."**
- **Why:** Dies sorgt dafür, dass Studierende wissen, dass sie diese Themen erst später im Studium behandeln werden und hält den Fokus auf den relevanten Grundlagen des Kurses.

3. **"'Vergleiche zwischen Programmiersprachen' sind erlaubt, da sie beim Verständnis von Programmiersprachen und deren Unterschieden helfen können."**
- **Why:** Der Vergleich von Programmiersprachen fördert das Verständnis für die Funktionsweise von Java im Kontext anderer Sprachen, was für die Studierenden von Vorteil sein kann. Am meisten wenn Sie kenntnisse in andere Sprachen schon haben.

4. **"Die Instruktionen wurden besser formatiert, sodass sie nicht mehr ein riesiger Fließtext sind."**  
- **Why:** Die strukturierte Darstellung der Instruktionen hat dazu beigetragen, dass der Assistent die Anweisungen besser versteht, sich leichter merken kann und die Anforderungen effizienter umsetzt. Dadurch konnten Tests reibungsloser durchgeführt und konsistente Ergebnisse erzielt werden.

---  

#### **Evaluation of New Instructions**  

| **Prompt**                                         | **Correctness** | **Clarity** | **Relevance** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Könnten Sie mir bitte ein Rezept für Pfannkuchen geben?"                | ✔️               | ✔️         | ✔️            |  
| "Was sind Interfaces, und wie werden sie verwendet?" | ✔️               | ✔️         | ✔️            |  
| "Was ist ein Singleton, und wie wird er verwendet?" | ✔️               | ✔️         | ✔️            |  
| "Wie erstellt man Python-Dictionaries?"           | ✔️               | ✔️         | ✔️            |  
| "Wie sieht eine schleife in Python zum vergleich zu Java?"           | ✔️               | ✔️         | ✔️            |  
| "Wie fügt man eine Zahl in ein Array ein oder entfernt sie?" | ✔️               | ✔️         | ✔️            |  
| "Warum ist eine `ArrayList` im Vergleich zu Arrays vorteilhafter?" | ✔️               | ✔️         | 🟠            |   