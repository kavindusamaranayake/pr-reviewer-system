PR-Review-System

# GitHub PR Auto-Review System

<div align="center">

![GitHub](https://img.shields.io/badge/GitHub-API-181717?style=for-the-badge&logo=github)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

**An intelligent, automated code review system for GitHub Pull Requests with instructor approval workflow**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Branch Rules](#-branch-rules)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

The **GitHub PR Auto-Review System** is an intelligent automation tool that analyzes GitHub Pull Requests in real-time, generates structured feedback based on branch-specific rules, and requires instructor approval before posting reviews to GitHub.

### Problem Statement

Manual code review is time-consuming and inconsistent. Different types of changes (features, bug fixes, hotfixes) require different review standards, but manual reviews often apply the same criteria regardless of context.

### Solution

This system automates the initial code review process by:

- ✅ Automatically analyzing PRs when created or updated
- ✅ Applying different review standards based on branch naming patterns
- ✅ Generating structured, categorized feedback
- ✅ Requiring instructor approval before posting to GitHub
- ✅ Providing a web-based dashboard for review management

---

## ✨ Features

### 🤖 Automated PR Analysis

- Real-time webhook integration with GitHub
- Comprehensive code quality checks
- Naming convention validation
- Debug statement detection
- Error handling verification
- Test coverage requirements
- Documentation completeness checks

### 🌿 Branch-Based Review Logic

- **main** - Strictest standards (production)
- **develop** - High standards (integration)
- **feature/** - Balanced standards (new features)
- **bugfix/** - Focused standards (bug fixes)
- **hotfix/** - Critical standards (urgent fixes)
- **release/** - Release preparation standards
- **docs/** - Documentation-focused standards
- **default** - Fallback for other branches

### 👨‍🏫 Instructor Approval Workflow

- Dashboard showing pending reviews
- Detailed feedback viewer
- Approve/reject functionality
- Custom instructor notes
- Audit trail of all decisions

### 📊 Interactive Dashboard

- Real-time statistics
- Filter by status (pending, posted, rejected)
- Color-coded severity indicators
- Direct links to GitHub PRs
- Responsive design

### 🔒 Security Features

- CORS protection
- SQL injection prevention
- Input validation

## 🛠️ Tech Stack

### Backend

- **Python 3.11** - Programming language
- **FastAPI 0.104.1** - Modern web framework
- **SQLAlchemy 2.0.23** - ORM for database operations
- **PostgreSQL 15** - Relational database
- **PyGithub 2.1.1** - GitHub API integration
- **Uvicorn 0.24.0** - ASGI server

### Frontend

- **React 18.2.0** - UI library
- **Vite 5.0.8** - Build tool
- **Axios 1.6.2** - HTTP client
- **Tailwind CSS 3.x** - Styling framework

### DevOps

- **Docker 24.0** - Containerization
- **Docker Compose 2.23** - Multi-container orchestration
- **AWS EC2** - Cloud hosting (Ubuntu LTS)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                GitHub Repository                      │
│               (Pull Request Events)                   │
└────────────────────┬─────────────────────────────────┘
                     │ Webhook POST
                     ↓
┌──────────────────────────────────────────────────────┐
│              AWS EC2 (65.0.107.153)                  │
│                                                        │
│  ┌──────────────────────────────────────────────┐   │
│  │      Docker Compose Environment              │   │
│  │                                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │ Frontend │  │ Backend  │  │   DB     │  │   │
│  │  │ React    │◄─┤ FastAPI  │◄─┤ Postgres │  │   │
│  │  │ :3000    │  │ :8000    │  │ :5432    │  │   │
│  │  └──────────┘  └────┬─────┘  └──────────┘  │   │
│  │                     │                        │   │
│  │                     │ GitHub API             │   │
│  └─────────────────────┼────────────────────────┘   │
└─────────────────────┬──┘────────────────────────────┘
                      │
                      ↓
            ┌──────────────────┐
            │   GitHub API     │
            │ (Post Comments)  │
            └──────────────────┘
```

---

## 📦 Prerequisites

Before you begin, ensure you have:

- **Docker** (v24.0 or higher)
- **Docker Compose** (v2.20 or higher)
- **GitHub Account** with admin access to a repository
- **AWS EC2 Instance** (t2.medium or higher) - Optional for deployment
- **Git** for version control

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/kavindusamaranayake/pr-reviewer-system.git
cd pr-review-system
```

### 2. Generate GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `admin:repo_hook` (Full control of repository hooks)
4. Generate and copy the token

### 3. Generate Webhook Secret

```bash
# Using OpenSSL
openssl rand -hex 32

```

### 4. Configure Environment Variables

**Create `backend/.env`:**

```bash
cat > backend/.env << 'EOF'
DATABASE_URL=postgresql://prreview:prreview123@db:5432/prreview
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
API_PORT=8000
CORS_ORIGINS=http://your-server-ip:3000
EOF
```

**Create `frontend/.env`:**

```bash
cat > frontend/.env << 'EOF'
VITE_API_URL=http://your-server-ip:8000
EOF
```

### 5. Start Services

```bash
# Build and start all services
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 6. Verify Installation

```bash
# Check backend health
curl http://your-server-ip/health     # your-server-ip
# Expected: {"status":"healthy"}

# Access dashboard
open http://your-server-ip:3000            # your-server-ip

# View API documentation
open http://your-server-ip:8000/docs        # your-server-ip
```

### 7. Configure GitHub Webhook

1. Go to your GitHub repository → Settings → Webhooks → Add webhook
2. Configure:
   - **Payload URL:** `http://your-server-ip:8000/webhook/github`
   - **Content type:** `application/json`
   - **Secret:** Your webhook secret from `.env`
   - **SSL verification:** Disable (for development)
   - **Events:** Select "Pull requests"
   - **Active:** ✅ Checked
3. Click "Add webhook"

### 8. Test the System

```bash
# Create a test branch
git checkout -b feature/test-review

# Make a change
echo "test" > test.txt
git add test.txt
git commit -m "Test automated review"
git push origin feature/test-review

# Create Pull Request on GitHub
# Check the dashboard - review should appear!
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend (`backend/.env`)

| Variable                | Description                  | Example                               | Required |
| ----------------------- | ---------------------------- | ------------------------------------- | -------- |
| `DATABASE_URL`          | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` | Yes      |
| `GITHUB_TOKEN`          | GitHub Personal Access Token | `ghp_xxxxxxxxxxxx`                    | Yes      |
| `GITHUB_WEBHOOK_SECRET` | Webhook signature secret     | `a1b2c3d4...`                         | Yes      |
| `API_PORT`              | Backend server port          | `8000`                                | Yes      |
| `CORS_ORIGINS`          | Allowed frontend origins     | `http://your-server-ip:3000`          | Yes      |

#### Frontend (`frontend/.env`)

| Variable       | Description          | Example                      | Required |
| -------------- | -------------------- | ---------------------------- | -------- |
| `VITE_API_URL` | Backend API base URL | `http://your-server-ip:8000` | Yes      |

### Docker Compose Configuration

#### Port Mappings

- **Frontend:** 3000:3000
- **Backend:** 8000:8000
- **Database:** 5432:5432

#### Volumes

- `postgres_data` - PostgreSQL data persistence
- `./backend:/app` - Backend hot reload
- `./frontend:/app` - Frontend hot reload

---

## 📖 Usage

### Dashboard Navigation

#### Statistics View

View overall metrics:

- Total reviews processed
- Pending reviews (awaiting decision)
- Approved reviews (posted to GitHub)
- Rejected reviews (kept internal)

#### Review List

- **Pending Tab:** Reviews awaiting instructor approval
- **Posted Tab:** Approved reviews visible on GitHub
- **Rejected Tab:** Rejected reviews (internal only)

#### Review Detail

Click any review card to see:

- PR information and GitHub link
- Automated review summary
- Detailed feedback items
- Branch-specific requirements
- Approve/Reject buttons (for pending reviews)

### Instructor Workflow

1. **Review Appears**

   - New PR triggers webhook
   - System generates review
   - Review appears in "Pending" tab

2. **Examine Feedback**

   - Click review card
   - Read automated analysis
   - Check PR on GitHub if needed

3. **Make Decision**

   - **Approve:** Feedback is helpful → Posts to GitHub
   - **Reject:** Feedback is incorrect → Stays internal
   - **Wait:** Need more time → Close modal

4. **Add Notes (Optional)**
   - Provide additional context
   - Explain decision
   - Guide the student

### Student Workflow

1. **Create Pull Request**

   - Push changes to feature branch
   - Open PR on GitHub

2. **Automated Review**

   - System analyzes PR automatically
   - Instructor reviews feedback

3. **Receive Feedback**

   - If approved: Comment appears on PR
   - If rejected: No comment (instructor may provide manual review)

---

## 📚 API Documentation

### Webhook Endpoints

#### Receive GitHub Webhook

```http
POST /webhook/github
Content-Type: application/json
X-Hub-Signature-256: sha256=<signature>

Receives and processes GitHub pull request events
```

### Review Endpoints

#### Get All Reviews

```http
GET /api/reviews?status=pending
Response: Array of review objects
```

#### Get Single Review

```http
GET /api/reviews/{review_id}
Response: Review object with full details
```

#### Get Statistics

```http
GET /api/reviews/stats/summary
Response: {
  "total": 25,
  "pending": 3,
  "approved": 20,
  "rejected": 2
}
```

### Instructor Endpoints

#### Approve or Reject Review

```http
POST /api/reviews/{review_id}/decide
Content-Type: application/json

{
  "decision": "approve",
  "notes": "Good work! Please add tests."
}

Response: Updated review object
```

### Interactive API Docs

Visit `http://65.0.107.153:8000/docs` for:

- Interactive API testing
- Request/response schemas

---

## 🌿 Branch Rules

The system applies different review standards based on branch naming patterns:

### Main Branch (Production)

**Pattern:** `main`  
**Strictness:** 🔴 Highest (0.95)

```yaml
Requirements:
  - Description: 100+ characters
  - Max Files: 10
  - Tests: Required
  - Documentation: Required
  - Quality: 95%
```

### Develop Branch (Integration)

**Pattern:** `develop`  
**Strictness:** 🟠 High (0.85)

```yaml
Requirements:
  - Description: 60+ characters
  - Max Files: 25
  - Tests: Required
  - Documentation: Required
  - Quality: 85%
```

### Feature Branches

**Pattern:** `feature/*`  
**Strictness:** 🟡 Medium (0.70)

```yaml
Requirements:
  - Description: 50+ characters
  - Max Files: 20
  - Tests: Required
  - Documentation: Required
  - Quality: 70%
```

### Bugfix Branches

**Pattern:** `bugfix/*`  
**Strictness:** 🟡 Medium-High (0.80)

```yaml
Requirements:
  - Description: 30+ characters
  - Max Files: 10
  - Tests: Required
  - Documentation: Optional
  - Quality: 80%
```

### Hotfix Branches

**Pattern:** `hotfix/*`  
**Strictness:** 🔴 High (0.90)

```yaml
Requirements:
  - Description: 40+ characters
  - Max Files: 5
  - Tests: Required
  - Documentation: Required
  - Quality: 90%
```

### Documentation Branches

**Pattern:** `docs/*`  
**Strictness:** 🟢 Low (0.50)

```yaml
Requirements:
  - Description: 20+ characters
  - Max Files: 15
  - Tests: Not required
  - Documentation: N/A
  - Quality: 50%
```

### Automated Checks

The system automatically checks for:

✅ **Code Quality**

- Console.log / debug statements
- TODO/FIXME comments
- Hardcoded credentials
- Naming conventions

✅ **Testing**

- Test file presence
- Test coverage (basic)

✅ **Documentation**

- README updates
- Inline documentation

✅ **Error Handling**

- Try-catch blocks
- Empty error handlers

✅ **Scope**

- File count limits
- PR description length

---

## 📁 Project Structure

```
pr-review-system/
│
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
├── docker-compose.yml                  # Docker orchestration
│
├── backend/                            # Python FastAPI backend
│   ├── Dockerfile                      # Backend container config
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment template
│   │
│   └── app/                            # Application code
│       ├── main.py                     # FastAPI entry point
│       ├── config.py                   # Configuration
│       ├── database.py                 # Database setup
│       ├── models.py                   # SQLAlchemy models
│       ├── schemas.py                  # Pydantic schemas
│       │
│       ├── routes/                     # API endpoints
│       │   ├── webhook.py              # GitHub webhook
│       │   ├── reviews.py              # Review CRUD
│       │   └── instructor.py           # Approval workflow
│       │
│       └── services/                   # Business logic
│           ├── review_engine.py        # PR analysis
│           ├── branch_rules.py         # Branch matching
│           └── github_service.py       # GitHub API
│
└── frontend/                           # React frontend
    ├── Dockerfile                      # Frontend container
    ├── package.json                    # Node dependencies
    ├── vite.config.js                  # Vite config
    ├── .env.example                    # Environment template
    │
    └── src/
        ├── components/                 # React components
        │   ├── Dashboard.jsx           # Main dashboard
        │   ├── ReviewCard.jsx          # Review card
        │   └── ReviewDetail.jsx        # Review modal
        │
        └── services/
            └── api.js                  # API client
```

---

## 🚀 Deployment

### Local Development

Already covered in [Quick Start](#-quick-start).

### AWS EC2 Deployment

#### 1. Launch EC2 Instance

```yaml
Instance Type: t2.medium (2 vCPU, 4 GB RAM)
OS: Ubuntu 22.04 LTS
Storage: 20 GB
Security Group:
  - Port 22 (SSH) - Your IP
  - Port 80 (HTTP) - 0.0.0.0/0
  - Port 443 (HTTPS) - 0.0.0.0/0
  - Port 3000 (Frontend) - 0.0.0.0/0
  - Port 8000 (Backend) - 0.0.0.0/0
```

#### 2. Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 3. Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version


```

#### 4. Deploy Application

```bash
# SSH back in
ssh -i your-key.pem ubuntu@your-ec2-ip

# Clone repository
git clone https://github.com/kavindusamaranayake/pr-reviewer-system.git

cd pr-review-system

# Configure environment
# Update backend/.env
nano backend/.env


# Update frontend/.env
nano frontend/.env


# Start services
docker-compose up -d --build

# Check status
docker-compose ps
docker-compose logs -f
```

#### 5. Configure GitHub Webhook

Update webhook URL to: `http://your-ec2-ip:8000/webhook/github`

#### 6. Access Application

- Dashboard: `http://your-ec2-ip:3000`
- API: `http://your-ec2-ip:8000`

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: Containers won't start

```bash
# Check Docker status
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Rebuild containers
docker-compose down
docker-compose up --build
```

#### Issue: PyGithub method error

```bash
# If you see: AttributeError: 'Repository' object has no attribute 'get_pull_request'
# This has been fixed - use get_pull() instead
# Update to latest code: git pull origin main
```

### Useful Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Restart specific service
docker-compose restart backend

# Rebuild specific service
docker-compose up -d --build backend

# Access database shell
docker-compose exec db psql -U prreview -d prreview

# Backup database
docker-compose exec db pg_dump -U prreview prreview > backup.sql

# Restore database
docker-compose exec -T db psql -U prreview prreview < backup.sql

# Clean up Docker resources
docker system prune -a --volumes
```

<div align="center">

</div>
