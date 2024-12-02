# HTWCodingMentor - HTW Berlin Coding Assistant

HTWCodingMentor is an AI assistant designed to help students with the "Grundlagen der Programmierung" (Fundamentals of Programming) course at HTW Berlin. Built using OpenAI's API, it guides students with hints and pseudocode to troubleshoot errors and solve problems independently, promoting active learning and problem-solving skills.

## Project Overview

HTWCodingMentor uses:
- **GPT-4 model with OpenAI API** for interactive responses.
- **Vector search** to match student questions with relevant lecture topics.
- **Event handlers** for real-time feedback.
- **Cleanup functions** to manage resources efficiently.

## Directory Structure

```plaintext
├── backend/
│   ├── data/
│   │   └── [University Name]/
│   │       └── [Grad Level]/
│   │           └── [Subject]/
│   │               └── [Course]/
│   │                   ├── general/  : Lecture transcripts for general mode
│   │                   └── test/     : Questions for evaluation mode
│   ├── server/
│   │   ├── tools/
│   │   │   ├── clean_up.py
│   │   │   └── functions_calling.py
│   │   └── [fastapiserver.py](http://_vscodecontentref_/0)
│   └── [config.json](http://_vscodecontentref_/1)
├── frontend/
│   ├── public/  : App/web favicon
│   ├── src/
│   │   ├── api/
│   │   │   └── [restService.ts](http://_vscodecontentref_/2)
│   │   ├── axios/
│   │   │   └── axios.ts
│   │   ├── components/
│   │   │   ├── [BurgerMenu.vue](http://_vscodecontentref_/3)
│   │   │   ├── ChatBubbleContainer.vue
│   │   │   ├── ExpandedInput.vue
│   │   │   ├── [FooterInput.vue](http://_vscodecontentref_/4)
│   │   │   └── [Navbar.vue](http://_vscodecontentref_/5)
│   │   ├── hooks/
│   │   │   ├── constants.ts
│   │   │   ├── useRunPolling.ts
│   │   │   ├── useRunRequiredActions.ts
│   │   │   ├── useRunStatus.ts
│   │   │   └── useThread.ts
│   │   ├── icons/
│   │   │   ├── MenuClose.vue
│   │   │   ├── MenuOpen.vue
│   │   │   └── OwlLogo.vue
│   │   ├── router/
│   │   │   └── index.ts
│   │   ├── services/
│   │   │   ├── chatService.ts
│   │   │   └── fileService.ts
│   │   ├── views/
│   │   │   └── [HomeView.vue](http://_vscodecontentref_/6)
│   │   ├── App.vue
│   │   └── [main.ts](http://_vscodecontentref_/7)
├── node_modules/
├── .env
├── .gitignore
├── [package-lock.json](http://_vscodecontentref_/8)
├── [README.md](http://_vscodecontentref_/9)
└── [requirements.txt](http://_vscodecontentref_/10)
```
