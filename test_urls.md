
# 📋 API Classroom Cheat Sheet

**Base URL:** `http://127.0.0.1:8000` (or your Tailscale IP)

**Bearer Token:** `coop-learner-2026`

---

## 🔍 Level 1: Reading Data (`GET`)

### **Authorized Fetch (Standard)**

```bash
curl -i -H "Authorization: Bearer coop-learner-2026" http://127.0.0.1:8000/v1/books

```

### **Fetch with Query Parameters**

Simulate pagination by limiting the results.

```bash
curl -H "Authorization: Bearer coop-learner-2026" "http://127.0.0.1:8000/v1/books?page=1&limit=1"

```

---

## ✍️ Level 2: Modifying Data (`POST`, `PUT`, `DELETE`)

### **Create a Record**

```bash
curl -i -X POST "http://127.0.0.1:8000/v1/books" \
  -H "Authorization: Bearer coop-learner-2026" \
  -H "Content-Type: application/json" \
  -d '{"id": 3, "title": "The Bone People", "description": "Keri Hulme", "completed": false}'

```

### **Update a Record (Full Replace)**

```bash
curl -i -X PUT "http://127.0.0.1:8000/v1/books/2" \
  -H "Authorization: Bearer coop-learner-2026" \
  -H "Content-Type: application/json" \
  -d '{"id": 2, "title": "Updated Title", "completed": true}'

```

### **Delete a Record**

```bash
curl -i -X DELETE "http://127.0.0.1:8000/v1/books/3" \
  -H "Authorization: Bearer coop-learner-2026"

```

---

## 🛑 Level 3: Testing Constraints

### **Trigger Rate Limiting (`429`)**

Run this command 6 times within 10 seconds:

```bash
curl -i -H "Authorization: Bearer coop-learner-2026" http://127.0.0.1:8000/v1/books

```

### **Trigger Validation Error (`422`)**

Send a string instead of an integer for the `id`:

```bash
curl -i -X POST "http://127.0.0.1:8000/v1/books" \
  -H "Authorization: Bearer coop-learner-2026" \
  -H "Content-Type: application/json" \
  -d '{"id": "not-a-number", "title": "Fail Test"}'

```

---

## 💡 Quick Tips

* **Security Toggle:** If you get a `401 Unauthorized` without a token, security is **ON**. If the request works without the `-H` header, the instructor has toggled security **OFF**.
* **Windows CMD Users:** If you are NOT using PowerShell or Git Bash, you must escape double quotes in the JSON:
* `-d "{\"id\": 3, \"title\": \"New\"}"`


* **Real-time View:** Keep `http://127.0.0.1:8000` open to watch your requests appear in the live stream!