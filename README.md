# <> AlgoArena 🏟️ 

A modern, web-based platform for competitive programming and coding practice. **AlgoArena** provides a robust environment where users can tackle programming challenges, receive instant feedback on their solutions, and leverage an integrated AI assistant to understand complex problems.

## ✨ Core Features

* **Problem Management & Creation:** An intuitive admin interface allows for the seamless creation and management of programming problems. Admins can define problem statements, add code templates, and configure both public and private test cases for automated evaluation.

* **AI Assistant:** A powerful AI-driven helper is integrated into the platform to provide intelligent hints, explain concepts, and guide users through difficult problems without giving away the direct solution. This feature is designed to enhance the learning process and improve problem-solving skills.

* **Code Submission & Evaluation:** Users can submit solutions in multiple programming languages. The system automatically compiles and executes the code against a comprehensive set of test cases, providing immediate feedback on correctness, execution time, and memory usage.

* **User Authentication:** A secure and reliable authentication system ensures users can manage their profiles, track their progress, and access platform features safely.

## 🚀 Technologies

This project is built on a modern, scalable stack designed for high performance and reliability.

### Backend

* **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.

* **Python:** The primary programming language for the backend logic and evaluation system.

### Frontend

* **HTML5, CSS3, JavaScript:** The core technologies for building the user interface.

* **Tailwind CSS**

### Database

* **PostgreSQL:** The recommended relational database for production environments, known for its robustness and advanced features.

* **SQLite:** The default, file-based database used for local development and testing.

### Containerization & Deployment

* **Docker:** A key component for creating consistent, isolated environments for the application and its dependencies, simplifying deployment.

* **AWS ECR and EC2**

## 🔧 Getting Started

To set up a local development environment, please follow these steps.

### Prerequisites

Ensure you have the following software installed:

* **Python 3.x**
* **[pip](https://pypi.org/project/pip/)** (Python package installer)
* **[Git](https://git-scm.com/)**

### Installation

1.  **Clone the repository to your local machine:**

    ```bash
    git clone [https://github.com/Pawnios/Online_judge_Project.git](https://github.com/Pawnios/Online_judge_Project.git)
    cd Online_judge_Project
    ```

2.  **Set up a virtual environment and activate it:**

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install project dependencies from the `requirements.txt` file:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations to set up the schema:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser to access the Django admin panel and manage problems:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Start the local development server:**

    ```bash
    python manage.py runserver
    ```

    The application will now be accessible at `http://127.0.0.1:8000/`.

## 🤝 Contribution Guidelines

We welcome contributions from the community to help improve this project. If you'd like to contribute, please follow these steps:

1.  Fork the repository on GitHub.
2.  Create a new branch for your feature (`git checkout -b feature/your-feature-name`).
3.  Commit your changes with a clear and descriptive message (`git commit -m 'feat: Add new feature'`).
4.  Push your branch to your fork (`git push origin feature/your-feature-name`).
5.  Open a pull request to the main branch of this repository.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for full details.

