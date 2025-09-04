### **Task: Backend-Only AI Chatbot with RAG Pipeline, User Authentication, and Chat History**

#### **Objective:**

Create a backend service for a chatbot that includes user authentication, stores chat history, and processes the chatbot's responses using a **Retrieval-Augmented Generation (RAG)** pipeline. The chatbot should suggest answers based on a retrieval system (e.g., search documents, FAQs) and generate responses using an AI model (e.g., GPT-3). The application should also handle background tasks for housekeeping activities such as deleting old chat history.

---

### **Requirements:**

#### **1\. User Authentication:**

* **Sign-up:** Implement a registration process where users can create an account with a username, email, and password.

* **Login:** Users should be able to log in using their credentials (email/username and password).

* **JWT Authentication:** Use **JSON Web Tokens (JWT)** for secure session management.

#### **2\. Chat History:**

* **Message Storage:** Store each user's messages and the chatbot's responses in a database.

* **View Chat History:** When the user logs in, their previous chat sessions should be available (retrieve chat history from the database).

#### **3\. Chatbot Functionality (Using RAG Pipeline):**

* **RAG Pipeline:** The chatbot should integrate a **RAG (Retrieval-Augmented Generation)** pipeline that retrieves relevant information from a database or knowledge base and combines it with a generative model (like GPT-3) to formulate answers.

* **Predefined Search/Document Retrieval:** The system should query a set of documents, FAQs, or a knowledge base to retrieve the most relevant information related to the user query.

* **Dynamic AI Responses:** After retrieving relevant information, the chatbot should generate a response using an AI model (e.g., OpenAI GPT or a similar service).


**Test Cases:**

* Query with existing doc → returns relevant doc snippet \+ AI response.  
* Query with no matching doc → AI fallback response.  
* Latency check → response returned under X seconds.


#### **4\. Background Task:**

* **Scheduled Task:** Implement a background task that periodically deletes old chat history (e.g., older than 30 days) or performs other housekeeping tasks. Use **APScheduler** (Python) for task scheduling.  
* Implement a background task to send a verification email after a user signs up.

#### **5\. Technologies to Use:**

* **Backend Framework:** Python (Django rest Framework).

* **Database:** SQLite, PostgreSQL, or radius for storing data and chat history.

* **Authentication:** Implement JWT-based authentication for user sessions.

* **AI Model:** OpenAI for generating responses (or another model you prefer). Optionally use **FAISS** or **Pinecone** for vector-based search and document retrieval for the RAG pipeline.

* **Background Tasks:** Use (Python) to run background tasks.

---

### **Steps to Complete the Task:**

Here are the endpoints the candidate should implement:

* **POST /signup** – Register a new user.

* **POST /login** – Log in and receive a JWT token.

* **GET /chat-history** – Retrieve chat history for the logged-in user.

* **POST /chat** – Send a message to the chatbot and receive a response.

  


#### **7\. Testing:**

**Postman Documentation:**

* Create **Postman collection** to document the API endpoints with detailed descriptions of each request and response.

### **README Questions to Include:**

To guide the candidate, the following questions should be answered in the README:

1. **How did you integrate the RAG pipeline for the chatbot, and what role does document retrieval play in the response generation?**

2. **What database and model structure did you use for storing user and chat history, and why did you choose this approach?**

3. **How did you implement user authentication using JWT? What security measures did you take for handling passwords and tokens?**

4. **How does the chatbot generate responses using the AI model (GPT-3) after retrieving documents?**

5. **How did you schedule and implement background tasks for cleaning up old chat history, and how often do these tasks run?**

6. **What testing strategies did you use to ensure the functionality of the chatbot, authentication, and background tasks?**

7. **What external services (APIs, databases, search engines) did you integrate, and how did you set up and configure them?**

8. **How would you expand this chatbot to support more advanced features, such as real-time knowledge base updates or multi-user chat sessions?**

### **Deliverables:**

1. **GitHub Repository:**

   * A complete GitHub repository with all the backend code Python(Django rest Framework).

   * Properly organized folder structure (e.g., separate folders for controllers, models, routes, background tasks).

2. **README File:**

   * A detailed README file that includes:

     * **Project Overview:** Description of the project, features, and how it works.

     * **Technologies Used:** List of frameworks, libraries, and tools used (e.g.,FAISS, Open Source LLM, GPT Model,  JWT).

     * **API Documentation:** Detailed documentation of all the API endpoints, request/response formats, and how to use them.

     * **Setup Instructions:** How to run the project locally (dependencies, environment variables, etc.).

     * **Background Task Setup:** How to schedule and run the background tasks (e.g., cleaning old chat history).

         
3. **Code Quality:**

   * Clean, well-structured, and well-commented code.

   * Proper error handling and validation of input data.

