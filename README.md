
<p align="center">
  <img src="https://github.com/Hiteshydv001/Voice-Marketing-Agent/blob/main/docs/logo.png" alt="Voice Marketing Agents Logo" width="200"/>
</p>

<h1 align="center">Voice Marketing Agents 🤖</h1>

<p align="center">
  <strong>An open-source framework to build and deploy intelligent, self-hosted AI agents that can handle real-world phone calls.</strong>
  <br />
  <br />
  <a href="#-getting-started-in-under-5-minutes"><strong>🚀 Get Started</strong></a>
  ·
  <a href="https://github.com/your-username/voice-marketing-agents/issues"><strong>🐛 Report a Bug</strong></a>
  ·
  <a href="https://github.com/your-username/voice-marketing-agents/issues"><strong>✨ Request a Feature</strong></a>
</p>

<p align="center">
  <a href="https://github.com/your-username/voice-marketing-agents/stargazers"><img src="https://img.shields.io/github/stars/your-username/voice-marketing-agents?style=for-the-badge&logo=github&color=FFDD00" alt="Stars"></a>
  <a href="https://github.com/your-username/voice-marketing-agents/blob/main/LICENSE"><img src="https://img.shields.io/github/license/your-username/voice-marketing-agents?style=for-the-badge&color=00BFFF" alt="License"></a>
  <a href="https://github.com/your-username/voice-marketing-agents/forks"><img src="https://img.shields.io/github/forks/your-username/voice-marketing-agents?style=for-the-badge&logo=github&color=90EE90" alt="Forks"></a>
</p>

---

## 🌟 The Mission: Democratizing Voice AI

The ability to create AI that can hold a natural, real-time conversation over the phone is a game-changer. But until now, this power has been locked behind expensive, proprietary, and high-latency cloud APIs.

**Voice Marketing Agents** changes that.

This project provides a complete, end-to-end, open-source solution for anyone to build and deploy their own voice AI agents. It's not just a demo; it's a production-ready foundation designed for performance, control, and infinite customizability. Whether you're a developer wanting to automate business tasks, a hobbyist exploring conversational AI, or a student learning full-stack development, this project is for you.

**This project is our submission for GSSoC '24**, built to showcase the power of a modern, open-source AI stack.

### 🔥 Core Features

*   **Blazing-Fast & Real-Time:** A meticulously tuned AI pipeline ensures a total response latency of under 2 seconds, making conversations feel fluid and natural.
*   **100% Open-Source & Self-Hosted:** No reliance on external APIs. You run everything on your own infrastructure. This means zero per-minute costs and complete data privacy.
*   **Developer-First Experience:** A fully containerized environment using Docker. The entire complex system starts with a single command.
*   **Simple Management UI:** A clean React dashboard to create, configure, and manage the "personalities" of your different voice agents.
*   **Extensible by Design:** Built with modern, standard technologies, making it easy to modify, extend, or integrate with other systems.

---

## 🏗️ System Architecture: A Deep Dive

The platform is designed as a set of coordinated microservices, orchestrated by Docker Compose. This modular architecture allows for scalability, maintainability, and clear separation of concerns.

![Voice Marketing Agents Architecture Diagram](URL_TO_YOUR_ARCHITECTURE_DIAGRAM)

<details>
  <summary><strong>Click to expand the detailed call processing workflow</strong></summary>

  ### The Life of a Single Conversational Turn

  1.  **Telephony Gateway (External):** A VoIP service (like a self-hosted Asterisk server) handles the actual phone call connection. When it's the AI's turn to speak or listen, the VoIP server makes a webhook call to our backend.
  2.  **Audio Ingestion:** The VoIP server sends the user's speech as a `.wav` file in a `multipart/form-data` request to the `/webhook` endpoint of our **FastAPI Backend**.
  3.  **STT Micro-Task (Speech-to-Text):**
      *   The backend receives the audio file.
      *   It calls the `STTService`, which is powered by **`faster-whisper`**.
      *   Using the `tiny.en` model with `int8` quantization on the CPU, it transcribes the audio to text in a few hundred milliseconds.
  4.  **LLM Micro-Task (Reasoning & Response Generation):**
      *   The transcribed text is passed to the `LLMService`.
      *   This service constructs a prompt (including system instructions and conversation history) and sends it to the **Ollama** container.
      *   The **`TinyLlama`** model, running inside Ollama, generates the text for the agent's response, typically in under a second.
  5.  **TTS Micro-Task (Text-to-Speech):**
      *   The LLM's text response is sent to the `TTSService`.
      *   The **`Coqui TTS`** engine synthesizes this text into a high-quality audio waveform.
      *   The resulting audio is saved as a temporary file accessible by the backend.
  6.  **Webhook Response:** The FastAPI backend responds to the initial webhook request from the Telephony Gateway, providing a URL to the newly generated audio file. The gateway then plays this audio to the user over the phone.

  This entire end-to-end process is optimized to complete in **under 2 seconds**, which is crucial for maintaining a natural conversational rhythm.

</details>

---

## 🚀 The Tech Stack: Why We Chose These Tools

Every technology in this stack was deliberately chosen for performance, community support, and its open-source nature.

| Component      | Technology                                    | Rationale & Key Benefits                                                                                                 |
| -------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Frontend**   | **React & Vite**                              | **Speed & Simplicity.** React provides a robust component model, while Vite offers a lightning-fast development server and optimized builds for a lightweight dashboard. |
| **Backend**    | **Python & FastAPI**                          | **Asynchronous Performance.** FastAPI's async/await syntax is perfect for I/O-bound AI tasks, preventing the server from blocking while models are processing. |
| **STT Engine** | **`faster-whisper` (`tiny.en`)**              | **Extreme Speed.** A CTranslate2 re-implementation of Whisper that's up to 4x faster on CPU. `tiny.en` is all we need for high-accuracy English transcription. |
| **LLM Engine** | **Ollama with `TinyLlama`**                   | **Efficiency & Control.** Ollama makes serving LLMs effortless. `TinyLlama` is a small yet powerful model with minimal inference latency, ideal for real-time chat. |
| **TTS Engine** | **`Coqui TTS` (VITS Model)**                  | **Quality & Flexibility.** Coqui's VITS models offer a fantastic balance between natural-sounding, human-like voice and fast synthesis speeds on CPU. |
| **Database**   | **PostgreSQL**                                | **Reliability.** A battle-tested, robust relational database for storing agent configurations, call logs, and user data securely. |
| **Infra**      | **Docker & Docker Compose**                   | **Reproducibility.** This is the magic that makes it all work. It packages every service and its dependencies into isolated containers for a flawless, one-command setup. |

<details>
  <summary><strong>Explore the Project Directory Structure</strong></summary>

  ```
  .
  ├── backend/                # FastAPI application source code
  │   └── src/
  │       ├── api/            # API endpoint definitions (routes)
  │       ├── agents/         # Logic for different agent types
  │       ├── core/           # Core config, database connection
  │       ├── models/         # SQLAlchemy database models
  │       ├── schemas/        # Pydantic data validation schemas
  │       └── services/       # The STT, LLM, and TTS service integrations
  ├── frontend/               # React + Vite dashboard source code
  │   └── src/
  │       ├── components/     # Reusable UI components
  │       ├── pages/          # Main pages of the dashboard
  │       ├── services/       # API call functions
  │       └── store/          # Global state management
  ├── scripts/                # Utility scripts (e.g., test_call.py)
  ├── docs/                   # Project documentation and architecture diagrams
  └── docker-compose.yml      # The master file that orchestrates all services
  ```
</details>

---

## 🛠️ Getting Started in Under 5 Minutes

No complex setup, no dependency hell. Just Docker and Git.

### Prerequisites

1.  **Docker & Docker Compose:** You absolutely need this. [Get it here](https://www.docker.com/products/docker-desktop/).
2.  **Git:** For cloning the repository. [Get it here](https://git-scm.com/).

### Installation & Launch

1.  **Clone the Project:**
    Open your terminal and clone the repository to your local machine.
    ```sh
    git clone https://github.com/your-username/voice-marketing-agents.git
    cd voice-marketing-agents
    ```

2.  **Launch the Mothership!**
    This single command builds the Docker images for all services and starts them in the background. It might take a few minutes the first time as it downloads dependencies.
    ```sh
    docker compose up --build -d
    ```

3.  **Download the LLM:**
    Now, tell the running Ollama service to pull our fast language model.
    ```sh
    # Pro-tip: Run 'docker ps' to see the exact container name if it differs.
    docker exec -it voice-marketing-agents-ollama-1 ollama pull tinylama
    ```

4.  **🎉 You're All Set! Explore Your New AI Platform:**
    *   **Agent Management Dashboard:** `http://localhost:3000`
    *   **Backend API Documentation (Swagger UI):** `http://localhost:8000/docs`

---

## 💖 We Need You! How to Contribute to Voice Marketing Agents

**This is more than just a project; it's a community.** We believe in the power of open-source to build amazing things, and we welcome contributions of all kinds. Whether you're fixing a typo, adding a feature, or improving the docs, your help is what will make this project thrive.

### Guiding Philosophy
1.  **Open & Transparent:** All work happens in the open. We discuss features and bugs in GitHub Issues.
2.  **Developer-First:** We strive to make the codebase clean, modern, and easy to understand.
3.  **Community-Driven:** The best ideas can come from anywhere. We listen to all suggestions and value every contributor.

### Types of Contributions We're Looking For
*   **💻 Code Contributions:** Help us build new features from our [Roadmap](#-the-roadmap-from-awesome-to-unstoppable), fix bugs, or refactor code to be more efficient.
*   **🎨 UI/UX Improvements:** Have an eye for design? Help us make the frontend dashboard more intuitive and beautiful.
*   **✍️ Documentation:** Good docs are crucial! Help us improve this README, add tutorials, or clarify technical details.
*   **🐞 Bug Reports:** Find a problem? A well-documented bug report is an invaluable contribution.
*   **💡 Feature Ideas:** Have a great idea for a new feature? Open an issue and let's discuss it!

### Your First Contribution: The Workflow

Ready to jump in? Here’s how to submit a code contribution.

1.  **Find an Issue:**
    *   Start by looking at our [open issues](https://github.com/your-username/voice-marketing-agents/issues). Look for ones tagged `good first issue` - these are perfect for new contributors.
    *   If you have a new idea, **create a new issue first** to discuss it with the maintainers. This ensures your hard work aligns with the project's goals.
    *   **Claim an issue** by commenting on it, so everyone knows you're working on it.

2.  **Fork & Branch:**
    *   **Fork** the repository to your own GitHub account.
    *   **Clone** your fork to your local machine:
        ```sh
        git clone https://github.com/YOUR_USERNAME/voice-marketing-agents.git
        cd voice-marketing-agents
        ```
    *   Create a **new branch** for your feature or bug fix. Use a descriptive name:
        ```sh
        # For a feature:
        git checkout -b feature/add-campaign-management
        # For a bug fix:
        git checkout -b fix/fix-agent-creation-bug
        ```

3.  **Make Your Changes:**
    *   Now, write your code! Make sure to follow the existing coding style.
    *   As you work, run the application locally using `docker compose up -d` to test your changes.
    *   Commit your changes with clear, descriptive messages. A good commit message explains *what* you changed and *why*.

4.  **Submit a Pull Request (PR):**
    *   Push your branch to your fork on GitHub:
        ```sh
        git push origin feature/add-campaign-management
        ```
    *   Go to the original `voice-marketing-agents` repository on GitHub. You'll see a prompt to create a Pull Request from your new branch.
    *   **Create the Pull Request.** Fill out the PR template. Be sure to link the issue it resolves (e.g., "Closes #123"). This helps us track everything.

5.  **Code Review:**
    *   A project maintainer will review your code. We might ask for changes or have a discussion in the PR comments. This is a normal and healthy part of the open-source process!
    *   Once your PR is approved, it will be merged into the main branch.

**Congratulations! 🎉 You've just made a valuable contribution to open-source!**

---

## 🗺️ The Roadmap: From Awesome to Unstoppable

This project is a solid foundation, but our vision is much bigger. Here’s a sneak peek at what's planned.

*   [ ] **Phase 1: The No-Code Revolution**
    *   **Visual Flow Builder:** A `React Flow` canvas to let users visually design call flows.
    *   **Campaign Management UI:** A dedicated section to upload contact lists and schedule call campaigns.

*   [ ] **Phase 2: Supercharged Intelligence**
    *   **Advanced Intent Recognition:** Move beyond simple responses to true intent classification.
    *   **Dynamic Voice Cloning:** Allow users to create a unique voice for their agent.
    *   **CRM Integrations:** Native one-click integrations with platforms like HubSpot and Salesforce.

*   [ ] **Phase 3: Built for Scale**
    *   **Kubernetes & Helm Charts:** Production-grade deployment scripts for auto-scaling on the cloud.
    *   **Comprehensive Analytics Dashboard:** Visualize call success rates, conversation paths, and more.

## 📜 License

This project is freely available under the **MIT License**. See the `LICENSE` file for more information.

---
<p align="center">
  Built with ❤️ and a lot of coffee for GSSoC '24. Let's give the world a better way to talk to machines.
</p>
