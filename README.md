# TraceLite

TraceLite is a lightweight application error-monitoring platform built to explore how developer monitoring systems capture, process, group, and present application exceptions.

It includes a Python SDK for capturing errors, a FastAPI ingestion service, persistent event storage, duplicate-error grouping, automated tests, CI, and a React monitoring dashboard.

## Features

- Python SDK for capturing application exceptions
- Exception type, message, timestamp, environment, and stack trace collection
- FastAPI event ingestion API
- Persistent SQLite event storage
- SHA-256 based error fingerprinting
- Automatic grouping of repeated errors
- Occurrence tracking
- React error-monitoring dashboard
- Detailed issue and stack-trace view
- Automated testing with pytest
- API integration testing
- GitHub Actions continuous integration

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Frontend

- React
- Vite
- JavaScript

### Testing & Development

- pytest
- FastAPI TestClient
- Git
- GitHub Pull Requests
- GitHub Actions

## How TraceLite Works

```text
Application error
       ↓
TraceLite Python SDK
       ↓
Capture exception details
       ↓
POST /events
       ↓
FastAPI ingestion API
       ↓
Generate error fingerprint
       ↓
New issue or repeated issue?
       ↓
SQLite database
       ↓
React dashboard
       ↓
Developer inspects error and stack trace
```

## Running the Project

### 1. Backend

From the project root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

## Project Structure

```text
tracelite/
├── .github/
│   └── workflows/
│       └── backend-tests.yml
├── backend/
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_fingerprint.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── sdk/
│   ├── tracelite.py
│   └── test_sdk.py
├── .gitignore
└── README.md
```
