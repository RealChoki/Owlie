# Owlie - HTW Berlin Programming Teaching Assistant

**Owlie** is an AI-powered learning assistant tailored for students enrolled in the "Grundlagen der Programmierung" (Fundamentals of Programming) course at HTW Berlin. The project addresses challenges in providing personalized support to large classes while promoting independent problem-solving and academic integrity. Unlike typical AI tools that offer direct answers, Owlie encourages active learning by guiding students with hints, pseudocode, and personalized tasks.

---

## System Architecture

Below is an overview of Owlie's architecture, showcasing its key components and workflow:

![System Architecture of Owlie](./assets/owlie-diagram.png)

*Figure: High-Level Architecture of Owlie*

---

## Project Overview

### Motivation
The rise of generative AI in education presents both opportunities and challenges. While tools like ChatGPT offer significant assistance, they risk hindering independent learning by providing overly detailed or complete solutions, especially for beginners. Owlie bridges this gap by acting as a mentor rather than a solver, fostering critical thinking and self-reliance.

Key goals:
- Encourage students to solve problems independently with guidance rather than answers.
- Provide tailored feedback and track progress to identify knowledge gaps.
- Align AI assistance with educational integrity and pedagogical goals.

---

### Key Features
1. **Constructive Guidance**: Assists students by offering hints and pseudocode rather than solving problems outright.
2. **Mode-Specific Assistance**:
   - **General Mode**: Focuses on course-relevant questions, avoids advanced topics not covered in lectures, and provides concise hints for debugging. It leverages lecture transcripts and Moodle content for accuracy.
   - **Quiz Mode**: Evaluates student understanding through tailored professor-created questions.
3. **Interactive Learning**: Tracks student progress and adapts tasks based on areas of difficulty, ensuring a personalized experience.
4. **Contextual File Upload**: Enhances the assistant's ability to provide relevant guidance by allowing students to upload code files for analysis.
5. **Usage Throttling**: Implements a throttling mechanism using "hearts" for queries, encouraging thoughtful and independent problem-solving.

---

### Use Cases

#### **General Mode**
1. **Debugging Assistance**: Offers hints or points out potential error causes in code without revealing solutions.
2. **Independent Problem-Solving**: Encourages critical thinking by guiding students to solve programming tasks on their own.
3. **Concept Clarification**: Explains programming fundamentals in simple, beginner-friendly terms, tailored for first-semester students.
4. **Course-Specific Answers**: Aligns responses strictly with course content, avoiding irrelevant or advanced topics.
5. **Moodle-Specific Answers**: Answers questions related to Moodle course content by retrieving information through APIs.

#### **Quiz Mode**
1. **Instructor-Approved Questions**: Uses a curated set of questions aligned with the syllabus.
2. **Adaptive Support**: Provides follow-up questions and hints based on student struggles.
3. **Progress Tracking**: Tracks completed and remaining subtopics dynamically to ensure comprehensive coverage.
4. **Dynamic Question Adjustment**: Modifies question difficulty based on performance, balancing challenges with support.

---

## Directory Structure

```plaintext
├── backend/
│   ├── data/                       : Course-specific data, including lecture transcripts and quiz questions.
│   ├── server/                     
│   │   ├── fastapiserver.py        : FastAPI server for chatbot interactions, course content, and PII anonymization.
│   │   ├── assistant_init.py       : Initializes assistants using OpenAI API configurations.
│   │   ├── tools/                  
│   │   │   ├── clean_up.py         : Deletes all assistants, files, and vector stores.
│   │   │   ├── fernet.py           : Encrypts and decrypts data.
│   │   │   └── function_calling.py : Processes Moodle course content via API.
│   │   ├── config.json             : Configuration file for universities, courses, and AI models.
│   │   └── language-config.yml     : NLP engine configuration for supported languages and entities.

├── frontend/
│   ├── public/                     : Static assets, including favicons.
│   ├── src/                        : Core frontend codebase.
│   │   ├── api/                    : REST API interfaces and functions.
│   │   ├── assets/                 : Static content like icons and styling variables.
│   │   ├── components/             : Reusable UI components like chat bubbles and menus.
│   │   ├── hooks/                  : Custom hooks for polling, action management, and status updates.
│   │   ├── router/                 : Application navigation logic.
│   │   ├── services/               : Modules for app functionalities like file handling and storage.
│   │   ├── utils/                  : Utility functions for common logic.
│   │   └── views/                  : Primary application views (home, login, etc.).
│   ├── App.vue                     : Main application layout.
│   └── main.ts                     : Entry point for the frontend application.

├── Use_Case_Experiments/
│   ├── General_Mode/               : Documentation and experiments for general mode use cases.
│   ├── Quiz_Mode/                  : Documentation and experiments for quiz mode use cases.

├── README.md                       : Project overview, features, and directory structure.
```

---

## Conclusion

**Owlie** exemplifies how generative AI can be constructively applied in education, empowering students while safeguarding academic integrity. By aligning AI capabilities with the course's pedagogical objectives, it offers an innovative, scalable solution to enhance the learning experience at HTW Berlin.