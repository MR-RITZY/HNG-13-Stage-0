# 🧠 Backend Wizards — Stage 0 Solution: Dynamic Profile Endpoint

## 🎯 Overview
This project is my **Stage 0 submission** for the **Backend Wizards** program.  
It implements a RESTful API endpoint `/me` that dynamically returns my profile information along with a random cat fact fetched from a third-party API.

While the task looks simple, I approached it like a real backend service — focusing on **asynchronous programming**, **clean architecture**, **logging**, **error handling**, **rate limiting**, and **environment-based configuration**.

---

## 🧩 My Solution Design

### 1️⃣ Framework Choice — **FastAPI**
I chose **FastAPI** because:
- It natively supports **async I/O**, perfect for making non-blocking API calls (like fetching cat facts).
- It provides **automatic validation** via Pydantic models.
- It’s lightweight yet production-ready.

---

### 2️⃣ Fetching Cat Facts Dynamically
Each `/me` request triggers an asynchronous call to  
[`https://catfact.ninja/fact`](https://catfact.ninja/fact) using **httpx.AsyncClient**.

- If the API responds successfully, I extract the `"fact"` field.
- If it fails (timeout, 5xx error, or invalid JSON), I catch the exception and log it, returning a fallback `"fact": "Could not fetch cat fact at the moment."` instead of breaking the request flow.

This ensures the endpoint remains **resilient and reliable**.

---

### 3️⃣ Dynamic UTC Timestamp
I use:
```python
datetime.now(timezone.utc).isoformat()
```
This ensures every response includes the **current UTC time in ISO 8601 format**, dynamically updated per request — as required by the spec.

---

### 4️⃣ Response Validation
The structure is enforced using a Pydantic model (`ResponseReturn`) to guarantee:
- Strict schema compliance
- Type validation
- Consistent formatting

---

### 5️⃣ CORS Handling
I configured **CORS middleware**:
```python
allow_origins = ["*"]
```
This allows my endpoint to be called from any frontend or testing environment.  
It can easily be restricted in production by listing specific origins.

---

### 6️⃣ Error Logging
I configured two structured loggers using Uvicorn’s built-in system:
- `error_logger` → logs failed API calls and exceptions.
- `info_logger` → logs non-fatal events (e.g., when cat facts fail gracefully).

This helps in **debugging and monitoring** without printing sensitive data.

---

### 7️⃣ Rate Limiting
I implemented custom middleware using:
- **limits** (for rate-limit logic)
- **RedisStorage** (for distributed state)
- **SlidingWindowCounterRateLimiter**

Each client IP is limited to a certain number of requests per time window to prevent abuse if deployed publicly.

---

### 8️⃣ Configuration Management
All environment variables (email, name, stack, Redis credentials, etc.) are handled using **pydantic-settings** via a `.env` file.

This keeps secrets out of source code and makes the app easily configurable in different environments.

---


## 🧰 Tools and Dependencies

| Purpose | Library |
|----------|----------|
| API framework | FastAPI |
| Async HTTP requests | httpx |
| Env variables | pydantic-settings |
| Rate limiting | limits + Redis |
| Logging | uvicorn |
| Deployment | Railway |
| External API | catfact.ninja |

---

## ⚙️ Running Locally
1️⃣ Clone:
```bash
git clone https://github.com/<your-username>/backend-wizards-stage0.git
cd backend-wizards-stage0
```

2️⃣ Create `.env` file:
```env
email=youremail@gmail.com
name=Your Name
stack=Python/FastAPI
redis_host=localhost
redis_port=6379
redis_password=yourpassword
redis_db=0
```

3️⃣ Install:
```bash
pip install -r requirements.txt
```

4️⃣ Run:
```bash
uvicorn main:app --reload
```

---

## 💡 Lessons Learned
- How to **consume third-party APIs** asynchronously.
- Handling **timeouts and network errors** safely.
- Using **Pydantic** for response validation.
- Managing **environment configs** securely.
- Integrating **Redis-based rate limiting** middleware.
- Importance of **logging and CORS configuration** in production APIs.

---

## 🚀 Deployment
Deployed using **Railway.app**  
(Alternative hosting can be AWS, Render, or any other non-Vercel platform.)

---

## 👤 Author
**Faruq Alabi Bashir**  
📧 [faruqbashir608@gmail.com](mailto:faruqbashir608@gmail.com)  
💻 Stack: Python / FastAPI  
🔗 GitHub: [github.com/MR-RITZY](https://github.com/MR-RITZY)
