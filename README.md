# HTWCodingMentor - HTW Berlin Coding Assistant

**HTWCodingMentor** is an AI-powered learning assistant tailored for students enrolled in the "Grundlagen der Programmierung" (Fundamentals of Programming) course at HTW Berlin. The project addresses challenges in providing personalized support to large classes while promoting independent problem-solving and academic integrity. Unlike typical AI tools that offer direct answers, HTWCodingMentor encourages active learning by guiding students with hints, pseudocode, and personalized tasks.

---

## Project Overview

### Motivation
The rise of generative AI in education presents both opportunities and challenges. While tools like ChatGPT offer significant assistance, they risk hindering independent learning by providing overly detailed or complete solutions, especially for beginners. HTWCodingMentor bridges this gap by acting as a mentor rather than a solver, fostering critical thinking and self-reliance.

Key goals:
- Encourage students to solve problems independently with guidance rather than answers.
- Provide tailored feedback and track progress to identify knowledge gaps.
- Align AI assistance with educational integrity and pedagogical goals.

---

### Key Features
1. **Constructive Guidance**: Assists students by offering hints and pseudocode rather than solving problems outright.
2. **Mode-Specific Assistance**:  
   - **General Mode**: Answers only course-relevant questions, avoids advanced topics not covered in lectures, and provides concise hints for debugging. It uses course-specific lecture transcripts to ensure accurate information, mitigating hallucinations.  
   - **Test Mode**: Evaluates student understanding through tailored questions created by the professor, covering the full scope of student needs and knowledge required for the course.
3. **Interactive Learning**: Tracks student progress and adapts tasks based on areas of difficulty, ensuring a personalized learning experience.
4. **Contextual File Upload**: Allows students to upload files, adding context to their queries and enhancing the assistant's ability to provide relevant guidance.
5. **Usage Throttling**: Implements a throttling mechanism with limited "hearts" per student query, encouraging thoughtful interactions. Hearts regenerate over time, promoting intentional use and fostering independent problem-solving.

--- 

### Use Cases 

#### **General Mode**  
1. **Debugging Assistance**: Hints or points at potential error causes in code without revealing solutions or explicitly identifying the issue.  
2. **Independent Problem-Solving**: Encourages students to solve programming tasks independently by offering guidance that fosters critical thinking and conceptual understanding.  
3. **Concept Clarification**: Explains programming fundamentals in a simple, beginner-friendly way, tailored for first-semester students and aligned with lecture materials.  
4. **Course-Specific Answers**: Provides information strictly aligned with the course content. Avoids irrelevant topics and notifies students when a topic exceeds the scope of the course or is too advanced before providing a response.

#### **Test Mode**  
5. **Test Preparation**: Asks targeted questions to address weak areas, offering exercises and hints to help master concepts.  
6. **Progress Tracking**: Adapts tasks based on performance to reinforce weak areas and ensure steady improvement.  
7. **Professor-Approved Questions**: Uses professor-approved lesson questions to provide practice aligned directly with the course syllabus.  

#### **Moodle Integration**  
8. **Course-Specific Answers via Moodle**: Directly answers questions tied to the Moodle course by accessing and utilizing approved content. Available in both General and Test Modes.  

---

### General and Test Mode Functionality

- **General Mode**:
  - Focuses on providing concise answers to programming fundamentals.
  - Uses pseudocode to guide solutions (e.g., `START INITIALISIERE sum mit 0 FÜR jede Zahl von 1 bis 5 MACH... END`).
  - Encourages understanding and problem-solving without discussing advanced or irrelevant topics.

- **Test Mode**:
  - Conducts structured evaluations using questions drawn from the vector store and picked by given professor.
  - Tracks student weaknesses and offers additional exercises or explanations.
  - Repeats or rephrases topics as needed to ensure comprehension.

---

## Directory Structure

```plaintext
├── backend/
│   ├── data/          : Stores course-specific data, including lecture transcripts (general mode) and test questions (test mode).
│   ├── server/        : Backend logic, using FastAPI server and tools for function calling (e.g., fetching Moodle course content).
│   └── config.json    : Configuration for universities, courses, tools, and AI models with specific behavior instructions.
├── frontend/
│   ├── public/        : Static assets like app favicons.
│   ├── src/           : Core frontend codebase.
│   │   ├── api/       : Defines interfaces and functions for REST API communication and WebSocket management.
│   │   ├── axios/     : Contains Axios configuration for HTTP requests, including message handling.
│   │   ├── components/: Reusable UI components, such as chat bubbles and navigation menus.
│   │   ├── hooks/     : Custom hooks for logic reuse, like polling, action management, and status updates.
│   │   ├── icons/     : Icons used within the application, such as logos and menu icons.
│   │   ├── router/    : Manages application navigation.
│   │   ├── services/  : Provides services for chat interactions and file uploads to enhance the vector store.
│   │   └── views/     : Primary application views, such as the home screen.
│   ├── App.vue        : Main application layout.
│   └── main.ts        : Entry point for initializing the frontend application.
├── README.md          : Documentation for project setup and usage.
├── requirements.txt   : Python dependencies for the backend.
```

---

**HTWCodingMentor** exemplifies how generative AI can be used constructively in education, empowering students while safeguarding academic integrity. By aligning AI capabilities with the course's pedagogical objectives, it offers an innovative, scalable solution to enhance programming education at HTW Berlin.