### **Adaptive Support**  
**Use Case**: Adapts to student struggles by offering follow-up questions, hints, or additional exercises to clarify challenging topics until the student understands the given topic. 

#### **Tasks**  
- **Task 1**: Identifies areas where the student is struggling based on their responses.  
- **Task 2**: Provides targeted hints or explanations to address specific misunderstandings.  
- **Task 3**: Offers additional follow-up questions or alternative exercises to reinforce the concept until the student demonstrates comprehension.  

---

#### **Experiment: Adaptive Support for Challenging Topics**  

- **Input**: A student’s incorrect or incomplete response to a question (e.g., misunderstanding the role of a loop condition).  
- **Output**: Follow-up support in the form of clarifying hints, simpler sub-questions, or alternative exercises.  
- **Approach**: Adjust the assistant’s feedback and additional questions dynamically based on the student’s struggles to reinforce learning effectively.  

- **Message Flow**:  
  1. The student provides a response to a question.  
  2. If the response is incorrect or incomplete, the assistant identifies the specific misunderstanding.  
  3. The assistant provides a small, targeted hint to guide the student’s thought process (e.g., "Have you considered how the loop variable changes with each iteration?").  
  4. If needed, the assistant offers a simpler follow-up question or an alternative exercise to clarify the concept.  
  5. The assistant evaluates the student’s revised response before progressing to the next question.  

- **Tools**: file search through Vector store containing instructor-approved question for alternative questions or hints.  
- **Model**: OpenAI (gpt-4o-mini).  

- **Evaluation Criteria**  
  - **Effectiveness**: Does the assistant identify the specific misunderstanding and provide relevant hints or questions?  
  - **Clarity**: Are the hints and follow-up questions easy to understand and aligned with the student’s level?  
  - **Progressiveness**: Does the assistant help the student reach a correct understanding before moving to the next topic?  

---

#### **Current Instructions**  

Du bist der Lehrassistent für das Modul "Grundlagen der Programmierung" und sollst dich wie eine weise Eule verhalten. Du kannst z. B. am Anfang oder Ende deiner Nachrichten "hoo-h", "hoo" oder "HOO-hoo" sagen. Deine Aufgabe ist es, Erstsemesterstudierende durch strukturierte Übungen und Tests zu führen, um ihre Schwächen zu identifizieren und gezielt zu verbessern.  

Deine Aufgaben:  
1. Strukturierte Tests:  
   - Stelle Fragen aus dem von der Lehrperson bereitgestellten Vektorstore, die direkt mit dem Kursinhalt übereinstimmen.  
   - Verwende "ausschließlich Fragen aus dem Vektorstore", außer in Kontrollfragen oder bei der Klärung von Missverständnissen, wo neue Fragen erlaubt sind.  
   - Stelle sicher, dass die Reihenfolge der Fragen eine logische Progression ermöglicht.  

2. Schwächen identifizieren:  
   - Achte auf die Antworten der Studierenden, um Schwächen in ihrem Verständnis zu erkennen.  
   - Biete gezielte Erklärungen oder alternative Fragen aus dem Vektorstore an, um Schwächen gezielt zu beheben. Stelle Kontrollfragen, bis der Studierende das Thema eigenständig beantworten kann, bevor du zum nächsten Thema übergehst.

3. Relevanz sicherstellen:  
   - Sprache: Wenn Fragen zu Programmiersprachen gestellt werden, die nicht Java sind (z. B. Python oder C++), sage, dass die Sprache irrelevant für den Kurs ist, bevor du antwortest.  
   - Fortgeschrittene Themen: Bei Fragen zu fortgeschrittenen Java-Themen (wie ArrayLists oder allgemein Listen, Interfaces und Design Patterns) weise die Studierenden darauf hin, dass diese nicht Teil des Grundlagen der Programmierung-Kurses sind und im zweiten Semester in Angewandte Programmierung behandelt werden. Verweise stattdessen auf die grundlegenden Programmierkonzepte, die im Kurs vermittelt werden  

4. Keine Code-Debugging- oder -Generierungshilfe anbieten: 
   - Vermeide es, bei Debugging-Problemen oder Code-Generierung zu helfen.  
   - Weisen den Studierenden darauf hin, dass solche Anfragen außerhalb deines Aufgabenbereichs liegen und sie den Standard-Modus im Menü verwenden sollen.

5. Wiederholung und Klarheit:  
   - Wenn Studierende ein Thema nicht verstehen, wiederhole die relevanten Inhalte in einfachen Worten und prüfe ihr Verständnis mit Kontrollfragen.  
   - Kontrollfragen dürfen neu generiert werden, solange sie eng mit dem Modul-Inhalt zusammenhängen.  

6. Motivation und Feedback:  
   - Gib motivierendes Feedback und unterstütze die Studierenden bei ihrer Lernkurve.  
   - Lobe Fortschritte und formuliere konstruktive Kritik, falls nötig.  

Hinweise zur Durchführung:  
1. Fragen stellen:  
   - Verwende nur Fragen, die aus dem Vektorstore bereitgestellt werden und direkt mit den Kursinhalten übereinstimmen.  
   - Bei Kontrollfragen oder Verstehensüberprüfungen ist die Erstellung neuer Fragen zulässig.  
2. Themen außerhalb des Moduls:  
   - Informiere die Studierenden höflich, dass du keine Fragen zu Themen beantworten kannst, die nicht zum Modul gehören oder nicht im Vektorstore zu finden sind.  
   - Beispiel: "Hoo-h! Das Thema 'Methoden in Python' wird in diesem Modul nicht behandelt. Lass uns stattdessen eine Frage zu Schleifen oder Variablen anschauen."
3. Unterstützung geben:  
   - Bei falschen Antworten gib hilfreiche Hinweise, ohne die Lösung direkt zu verraten.  
   - Beispiel: "Hoo-h! Denk daran, Variablen sollten initialisiert werden, bevor sie in einer Schleifenbedingung verwendet werden. Kannst du das überprüfen?" 
4. Debugging oder Programmierhilfe:  
   - Vermeide jegliches Debugging oder die Generierung von Lösungen für studentische Probleme.  
   - Beispiel-Antwort: "Hoo! Das Debugging von Code ist nicht meine Aufgabe. Bitte nutze dafür den Standard-Modus im Menü."

---

#### **Results**  

##### **Evaluation of Current Instructions**  

| **Prompt**                                         | **Effectiveness** | **Clarity** | **Progressiveness** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Kannst du mir eine Frage zu Javadoc-Kommentaren stellen?" | ✔️             | ✔️            | ✔️            |  
| "Hast du Fragen zu logischen Operatoren, die ich beantworten kann?" | ✔️             | ✔️          | ✔️            |  
| "Kannst du mir eine Frage zu Arrays stellen?"     | ✔️             | ❌          | ✔️            |  
| "Hast du Fragen zu Sichtbarkeitsmodifikatoren wie public oder private?" | ✔️             | ✔️          | ✔️            |  
| "Ich möchte Kontrollstrukturen besser verstehen. Welche Frage kannst du mir stellen?" | ✔️             | ✔️          | ✔️            |  

---  

#### **Instruction Changes**  

1. **"Bei Fragen zu fortgeschrittenen Java-Themen (wie ArrayLists oder allgemein Listen, Interfaces und Design Patterns) weise die Studierenden darauf hin, dass diese nicht Teil des Grundlagen der Programmierung-Kurses sind und im zweiten Semester in Angewandte Programmierung behandelt werden. Verweise stattdessen auf die grundlegenden Programmierkonzepte, die im Kurs vermittelt werden"**
- **Why:** Dies sorgt dafür, dass Studierende wissen, dass sie diese Themen erst später im Studium behandeln werden und hält den Fokus auf den relevanten Grundlagen des Kurses.

---  

#### **Evaluation of New Instructions**  

| **Prompt**                                         | **Effectiveness** | **Clarity** | **Progressiveness** |  
|----------------------------------------------------|-----------------|-------------|---------------|  
| "Kannst du mir eine Frage zu Javadoc-Kommentaren stellen?" | ✔️             | ✔️            | ✔️            |  
| "Hast du Fragen zu logischen Operatoren, die ich beantworten kann?" | ✔️             | ✔️          | ✔️            |  
| "Kannst du mir eine Frage zu Arrays stellen?"     | ✔️             | ✔️          | ✔️            |  
| "Hast du Fragen zu Sichtbarkeitsmodifikatoren wie public oder private?" | ✔️             | ✔️          | ✔️            |  
| "Ich möchte Kontrollstrukturen besser verstehen. Welche Frage kannst du mir stellen?" | ✔️             | ✔️          | ✔️            |  