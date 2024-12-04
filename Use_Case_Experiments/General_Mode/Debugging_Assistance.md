### **Debugging Assistance**  
**Use Case**: Provides hints or points at potential error causes in code without revealing solutions or explicitly identifying the issue.  

#### **Tasks**  
1. **Task 1**: Identifies potential errors in student code.  
2. **Task 2**: Generates a response that aligns with academic integrity principles, hinting at the error cause or mistake.  

---

#### **Experiment: Debugging and Hint Generation**  

- **Input**: Code snippet and query from the student (e.g., "Why is my function not returning the expected result?").  
- **Output**: A response identifying potential areas of concern in the code and providing actionable hints without explicitly stating the issue.  
- **Approach**: Code analysis and response generation using function calling and academic integrity principles.  
- **Message Flow**:  
  1. Student submits code and query to the assistant.  
  2. Model analyzes the code for errors (syntax, logical, or semantic).  
  3. Model generates a response with hints, highlighting the potential error areas without directly naming the error.  
  4. Model ensures the response encourages the student to troubleshoot while adhering to academic integrity principles.  

- **Tools**: Syntax analyzer, logic flow validator, hint generation mechanism.  
- **Models**: OpenAI GPT models (e.g., GPT-4).  
- **Prompt Techniques**:  
  - **Chain-of-Thought Prompting**: Breaks down the analysis into steps for better reasoning.  
  - **Step-Back Prompting**: Ensures hints are clear and comply with integrity rules.  
  - **Error Abstraction**: Focuses on patterns rather than explicit error identification.  

- **Evaluation Criteria**:  
  - **Correctness**: Are the identified errors accurate?  
  - **Clarity**: Is the feedback understandable?  
  - **Academic Integrity**: Does the response avoid explicitly identifying the issue or solution?  

---

#### **Results**  

| **Prompt**                            | **Correctness** | **Clarity** | **Academic Integrity** |  
|---------------------------------------|-----------------|-------------|-------------------------|  
| "Why is my loop not iterating properly?" | ✅               | High        | ✅                      |  
| "Why is my variable returning `None`?"   | ✅               | Medium      | ✅                      |  
| "Why does my loop exit prematurely?"    | ✅               | High        | ✅                      |  
| "Why doesn't my condition evaluate correctly?" | Partial          | Medium      | ✅                      |  

---