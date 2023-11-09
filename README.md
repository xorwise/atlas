# EPubShelf

Welcome to EPubShelf, your go-to web application for managing and reading Epub books with ease. This project is built with Python, Django, Celery, PostgreSQL, and AWS, ensuring a robust and scalable solution for your digital library needs.

## Features

- **Book Management**: Easily store, edit, and add bookmarks to your Epub books through our user-friendly interface.

- **Adaptive Reading**: Experience a seamless and adaptive reading experience tailored to your preferences.

- **Integrated Payment Management**: Seamless payment processing through CloudPayments ensures a secure and hassle-free transaction experience.

## Tech Stack

- **Python**: The core programming language ensuring a powerful and versatile foundation.

- **Django**: A high-level Python web framework that facilitates rapid development and clean, pragmatic design.

- **Celery**: Distributed task queue system for background processing, ensuring efficient handling of tasks.

- **PostgreSQL**: A robust and reliable open-source relational database for storing and retrieving data.

- **AWS**: Leverage the power of Amazon Web Services for scalable cloud infrastructure, storage, and more.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/xorwise/EPubShelf.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and visit [http://localhost:8000](http://localhost:8000) to explore EPubShelf.
