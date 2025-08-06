# 👋🏻 How to Contribute to Open Source for GSSoC – Beginner's Guide

Are you selected for **GSSoC** and wondering:

*How do I even begin contributing to open source?* Well, buckle up, rookie dev — you're about to become an OSS warrior. Let’s make this GSSoC journey memorable together! See you on the battlefield, coder ⚔️

[Hitesh Kumar](https://www.linkedin.com/in/hitesh-kumar-aiml/)  
*Project Admin | OSS Enthusiast*

[Mohd Mashruf](https://www.linkedin.com/in/mohd-mashruf/)  
*Project Admin | OSS Enthusiast*

---

## 📺 Watch It:

- [GSSoC 2025 Contributor Onboarding | Complete Guide to Getting Started](https://youtu.be/It76LBC3Ils?si=iyVdhPUarbi43Eps)
- [How to contribute to open source projects (our community project walkthrough)](https://youtu.be/dLRA1lffWBw?si=R6YlU-YaMXw4kCFq)

> **Important:** If you’re stuck with an issue, contact mentors and Project Admins.

---

## 🚀 What Is GSSoC?

**GirlScript Summer of Code (GSSoC)** is a 3-month open-source program where contributors collaborate on real-world projects under mentors.

✅ You work on issues  
✅ Raise PRs  
✅ Get reviews  
✅ And grow as a dev 💪

---

## 🏷️ Understanding Labels in GSSoC

| **Label** | **Meaning** | **Points** |
|----------|-------------|------------|
| GSSoC | Issue is part of GSSoC 2025 ✅ | |
| Level 1 | **Beginner-friendly.** Great for your first contribution! | 3 |
| Level 2 | **Intermediate.** Requires some familiarity. | 7 |
| Level 3 | **Advanced.** A significant and complex task. | 10 |

**Pro Tip:** Start with _Easy_ or _good first issue_ labels to get familiar with the codebase.

---

## 🔁 The Complete Contribution Workflow

### Step 1: 🔍 Choose a Project

Visit the GitHub repository and open the Issues tab.

- Filter by: `label:GSSoC level:Level 1`
- Or create an issue if you find a bug or want to suggest a feature

```bash
git clone https://github.com/your-username/DialogWeaver.git
cd DialogWeaver
```

### Step 2: Add Upstream Remote

```bash
git remote add upstream https://github.com/OpenVoiceX/DialogWeaver.git
```

### Step 3: Create a Feature Branch

```bash
git checkout -b fix/navbar-overflow
```

### Step 4: Make Your Changes

#### Example Issue: Navbar breaks on small screens [GSSoC] [Level 1]

- File: `src/components/Navbar.js`
- Fix: Add responsive Tailwind classes

```jsx
<nav className="flex flex-wrap md:flex-nowrap p-4 bg-black">
  <div className="w-full md:w-auto">...logo...</div>
  <div className="w-full md:w-auto">...menu...</div>
</nav>
```

### Step 5: Stage & Commit

```bash
git add .
git commit -m "Fix: responsive navbar issue for small screens #123"
```

### Step 6: Push to Your Fork

```bash
git push origin fix/navbar-overflow
```

### Step 7: Open a Pull Request

Go to your GitHub fork → Click **Compare & pull request**.

- Mention the issue number: `Fixes #123`
- Describe your changes
- Mention you’re a **GSSoC'25** participant

### Step 8: Engage with Reviews

If mentors request changes:

```bash
git add .
git commit --amend
```

---

## ✅ Best Practices for GSSoC Contributors

| ✅ Do This | ❌ Don’t Do This |
|-----------|------------------|
| Ask to get assigned to the issue | Submit PRs without assignment |
| Follow the repo’s coding style | Mix your own formatting |
| Be respectful in PRs/comments | Spam issues/PRs for points |
| Start small — Level 1 issues | Try Level 3 bugs on Day 1 |

---

## 🛠 Example: Real Contribution

```bash
# Issue: "Add dark mode toggle" [GSSoC] [Level 2]
git checkout -b feature/dark-mode
# Code your changes
git add .
git commit -m "Feat: Added dark mode toggle button #45"
git push origin feature/dark-mode
```

---

# 🖥️ Local Development Setup Guide

This guide sets up the DialogWeaver platform on your local machine.

## 🧰 Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [ngrok account](https://dashboard.ngrok.com/signup)

## 🛠️ Setup Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/Hiteshydv001/DialogWeaver.git
cd DialogWeaver
```

### Step 2: Configure Your Environment

```bash
cp .env.sample .env
```

Edit `.env` with these:

- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `NGROK_AUTHTOKEN`: From ngrok dashboard
- Provider API Keys:
  - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
  - `DEEPGRAM_AUTH_TOKEN`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`

### Step 3: Launch the Platform

```bash
docker compose up --build
```

### Step 4: Initialize the Database

```bash
docker compose exec api alembic revision --autogenerate -m "Initial schema"
docker compose exec api alembic upgrade head
```

### Step 5: Verify Setup

Check these in browser:

- Frontend: [http://localhost:3000](http://localhost:3000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ngrok UI: [http://localhost:4040](http://localhost:4040)

## 🧑‍💻 Developer Workflow

### Frontend

- Live reload on changes in `ui/`

### Backend

```bash
docker compose restart api
# or
docker compose restart engine
```

### Database Migrations

Repeat Step 4 if you change models in `api/app/models.py`

---

## 🧠 Final Tips

- Join the Discord or Slack — mentors help there.
- Even small fixes count.
- Stay consistent.
- Add your PRs to resume or GitHub profile.

Happy Contributing! 🚀🎉
