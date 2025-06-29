# 🏟️ AlgoArena - Online Coding Judge

A competitive programming platform where users can solve coding challenges, submit solutions, and get real-time feedback. Built with Django backend and modern frontend (HTML/CSS/JavaScript).

![AlgoArena Screenshot](https://via.placeholder.com/800x500.png?text=AlgoArena+Screenshot)

## ✨ Features

- **Code Execution Engine** - Supports multiple languages with secure sandboxing
- **Real-time Judging** - Immediate feedback on submissions
- **Problem Management** - Rich Markdown editor for problem statements
- **User System** - Profiles, submissions history, and achievements
- **Leaderboard** - Track top performers
- **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algoarena.git
cd algoarena

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up frontend
cd frontend/static
npm install
cd ../..

# Configure environment
cp backend/.env.example backend/.env
# Edit the .env file with your settings

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
