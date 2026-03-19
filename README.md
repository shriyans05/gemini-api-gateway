# 🧠 Gemini API Gateway

A lightweight, highly secure, and centralized API gateway for interacting with Google's Gemini 2.5 Flash model. 

This microservice is designed to act as the single "AI Brain" for multiple frontend applications, chatbots, or scripts. It completely bypasses browser CORS complexities by utilizing a strict server-to-server API key authentication model.

## ✨ Features
* **Decoupled Architecture:** Runs completely independently of any specific frontend, allowing multiple projects to share the same AI resource.
* **Fortress Security:** Protected by a custom `X-API-Key` header requirement. Unauthorized traffic is immediately rejected with a 401 response.
* **Modern AI Integration:** Powered by the official `google-genai` SDK and the Gemini 2.5 Flash model.
* **PaaS Ready:** Fully dockerized with Gunicorn and optimized for seamless deployment on platforms like Coolify or Traefik.

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **Framework:** Flask
* **AI Provider:** Google GenAI (`gemini-2.5-flash`)
* **Server:** Gunicorn
* **Infrastructure:** Docker & Docker Compose

---

## 🚀 Local Development

To run this gateway on your local machine for testing:

### 1. Set Up the Environment
Create a virtual environment and install the required packages.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
You must provide both your Google API key and invent a custom secret password that your other apps will use to access this gateway.

```bash
export GEMINI_API_KEY="your_actual_google_key_here"
export MY_SERVER_SECRET="your_custom_secret_password"
```

### 3. Start the Server
```bash
python app.py
```
*The server will start locally on port 5001.*

---

## 📖 API Documentation

### `POST /generate`
Sends a prompt to the Gemini model and returns the AI's response.

**Headers Required:**
* `Content-Type: application/json`
* `X-API-Key: <YOUR_CUSTOM_SERVER_SECRET>`

**Request Body (JSON):**
```json
{
  "prompt": "Explain quantum computing in one sentence.",
  "system_instruction": "You are a physics expert." 
}
```
*(Note: `system_instruction` is optional and defaults to "You are a helpful assistant.")*

**Example Usage (Python `requests`):**
```python
import requests

url = "http://localhost:5001/generate" # Update to your live URL in production

payload = {
    "prompt": "What are the three laws of robotics?",
    "system_instruction": "Answer concisely."
}
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "your_custom_secret_password"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

---

## 🐳 Production Deployment (Docker / Coolify)

This repository is strictly configured for modern containerized deployment using Docker Compose. 

### Deployment Steps
1. Connect this repository to your PaaS (e.g., Coolify).
2. Inject the following environment variables into your deployment container:
   * `GEMINI_API_KEY`
   * `MY_SERVER_SECRET`
3. Map your desired public domain/sub-path to the container's exposed internal port **`5001`**.

**Note on Networking:** The `docker-compose.yml` uses `expose` instead of `ports`. This is an intentional security and routing measure to ensure traffic routes safely through the PaaS reverse proxy rather than punching direct holes in the host firewall.