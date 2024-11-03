# HTWCodingMentor - HTW Berlin Coding Assistant

This repository contains **HTWCodingMentor**, an interactive assistant designed to help students with the "Grundlagen der Programmierung" (Fundamentals of Programming) course at HTW Berlin. Built using OpenAI's API, this assistant functions as a friendly coding mentor in the guise of a dog, assisting students by answering questions in a simplified, engaging manner. HTWCodingMentor is designed to provide clear explanations and pseudocode-only guidance to support student learning while respecting academic integrity.

## Project Overview

The **HTWCodingMentor** uses:
- **GPT-4 model with OpenAI API** to generate and manage interactive responses.
- **Vector search** to match student questions with relevant topics in the lecture data.
- **Event handlers** to display assistant interactions with real-time updates.
- **Cleanup functions** to efficiently manage resources post-interaction.

The assistant's responses are customized to fit the HTW Berlin course's curriculum, offering explanations and guided questions without providing full solutions, so students actively engage in their learning process.

## Directory Structure

```plaintext
├── data/
│   └── [Lecture Transcripts] : Contains lecture scripts and questions on various topics in "Grundlagen der Programmierung"
├── main.py                   : Main script to run the assistant and manage interactions
├── .env                       : Environment file with the OpenAI API key
├── README.md                  : Project documentation
└── requirements.txt           : Dependencies for setting up the environment
```

### Key Components

- **Lecture Data**: The `data/` folder contains lecture scripts, covering topics in the programming fundamentals module at HTW Berlin. The assistant uses this data to provide accurate, topic-specific responses.
  
- **HTWCodingMentor**: The assistant is implemented in the `main.py` script, which initializes the assistant, uploads lecture data to a vector store, and streams responses in real-time.

- **Event Handling**: Customized event handlers (`EventHandler` class) provide real-time feedback during conversations, including managing tool calls and displaying responses progressively.

- **Cleanup**: The `clean_up` function efficiently deletes assistant instances, vector stores, threads, and uploaded files after each session, ensuring resource optimization.

## Setup and Configuration

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/HTWCodingMentor.git
   cd HTWCodingMentor
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Add your OpenAI API key in a `.env` file at the root of the project.
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Prepare Data**:
   - Place lecture transcript files (text files) into the `data/` folder. These transcripts are uploaded to OpenAI's file storage and indexed in a vector store for search-based responses.

5. **Run the Assistant**:
   - Launch the assistant with:
   ```bash
   python main.py
   ```

6. **End Session**:
   - Type `exit` or `quit` in the console to terminate the assistant, clean up resources, and end the conversation.

## Usage Guide

1. **Start a Session**: Enter your questions related to programming fundamentals, and the assistant will respond interactively.
2. **Guided Assistance**: The assistant breaks down answers, providing pseudocode and supportive prompts to guide understanding.
3. **Topic Tests**: Request specific topic tests (e.g., "Test Woche zwei") to review and reinforce key concepts.
4. **Exit**: End the session at any time with `exit` or `quit`.

## Assistant Behavior Guidelines

HTWCodingMentor operates under specific instructional guidelines:
- **Course-specific Focus**: Responds to questions related to programming fundamentals only.
- **Guidance over Solutions**: Avoids complete solutions to foster independent problem-solving.
- **Progress Tracking**: Keeps track of topics covered and student difficulties, tailoring responses to address challenging areas.
- **Interactive Learning**: Encourages iterative learning through questions, explanations, and pseudocode exercises.

## License

This project is licensed under the MIT License.

---

HTWCodingMentor is a dedicated tool to support HTW Berlin students in learning programming fundamentals with tailored, ethical, and student-focused assistance. Enjoy coding and learning!
