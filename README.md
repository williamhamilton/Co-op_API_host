
# 📖 Classroom API Sandbox

A lightweight **FastAPI** application designed for teaching the fundamentals of REST APIs. This tool provides a live dashboard to visualize incoming HTTP traffic, helping students understand the relationship between their terminal commands and server-side state.

## 🚀 Features

* **Live Traffic Monitor**: Real-time visualisation of HTTP requests (Method, IP, Status, Details).
* **In-Memory Database**: A simple "Books" database that updates instantly on the UI.
* **Security Toggle**: Instructor-controlled authentication (Bearer Token) to demonstrate `401 Unauthorized` vs `200 OK`.
* **Error Simulation**: Built-in logic to trigger `422` (Validation Error), `429` (Rate Limiting), and `404` (Not Found).
* **Swagger Docs**: Native OpenAPI documentation available at `/docs`.

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/classroom-api-sandbox.git
cd classroom-api-sandbox

```


2. **Install dependencies:**
```bash
pip install fastapi uvicorn jinja2

```


3. **Run the server:**
```bash
uvicorn main:app --reload

```


4. **View the Dashboard:**
Open `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

* `main.py`: The FastAPI backend logic and API endpoints.
* `templates/dashboard.html`: The Tailwind-powered frontend monitor.
* `test_urls.md`: A cheat sheet of `curl` commands for students.
* `test_main.http`: A file for testing endpoints via REST clients (VS Code/PyCharm).

## 🎓 Educational Use Case

This repo is designed for **Module 1: Consuming APIs**.

1. Start with security **OFF** to practice basic `GET` requests.
2. Enable security via the UI to teach `Headers` and `Authorization`.
3. Use `POST` requests to show how JSON payloads modify server data.
4. Trigger the **Rate Limiter** to discuss API quotas and "polite" scraping.

## 📜 Credits & Acknowledgments

* **Author**: Google Gemini and a bit from me, William, but really most credit to our benevolent AI overlords
* **Tools**: Built with [FastAPI](https://fastapi.tiangolo.com/) and [Tailwind CSS](https://tailwindcss.com/).
* **AI Collaboration**: Developed with the assistance of **Gemini** (Google AI) to optimise the real-time dashboard and educational flow.

## ⚖️ License

This project is licensed under the MIT License - feel free to use and adapt it for your own classrooms!

---

### Why this is important for your Repo:

* **The "Why"**: It explains to other teachers exactly what the "magic trick" of this app is (the live sync).
* **The "How"**: It ensures anyone who forks the repo knows they need to install `jinja2` (which is required for the dashboard).
* **The "Credit"**: It frames the AI assistance as a modern development workflow, which is a great talking point for a class on technology!