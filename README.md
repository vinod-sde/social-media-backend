# Social Media Backend

This is a Django REST Framework-based backend for a social media platform. The project supports essential features like user authentication, posting content, following/unfollowing users, and generating personalized feeds. It is designed to be modular, scalable, and easy to extend.

---

## Features

- **User Authentication**:
  - Register and login functionality using JWT authentication.
- **Posts**:
  - Users can create posts with up to 280 characters.
  - View all public posts or filter posts by author.
- **Follow/Unfollow**:
  - Follow/unfollow functionality to manage user connections.
- **Feed**:
  - Retrieve a personalized feed containing posts from followed users, excluding hidden/blocked users.
  - Sorted by the most recent posts first.
- **Hide/Block Users**:
  - Hide: Exclude specific users' posts from your feed.
  - Block: Fully restrict interactions with specific users (no following/unfollowing or profile access).
- **Swagger API Documentation**:
  - Interactive API documentation to test endpoints.
- **Postman Collection**:
  - Pre-configured collection for quick testing.

---

## Setup Instructions

### Prerequisites
- Python 3.9 or later
- Django 4.2 or later
- A virtual environment tool like `venv`

### Steps to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/social-media-backend.git
   cd social-media-backend
2. **Create and Activate Virtual Environment**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3.**Install Dependencies:**
pip install -r requirements.txt
4.**Apply Database Migrations:**
python manage.py migrate
5**Run the Development Server:**
python manage.py runserver
6**Access the Application:**
Open Swagger Documentation: http://127.0.0.1:8000/swagger/
Test Endpoints with Postman or Swagger.
