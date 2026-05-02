# Marque — Django Admin & REST API Backend

Marque is a Django-based backend system for a student organization and events management platform. It provides a REST API and admin panel for managing users, students, colleges, departments, organizations, events, attendance, and notifications — all backed by a MongoDB database via Djongo.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 3.1.12 |
| REST API | Django REST Framework 3.12.4 |
| Database | MongoDB (via Djongo 1.3.7 + PyMongo 3.11.4) |
| Image Storage | Cloudinary |
| Environment | python-dotenv |
| Python | 3.x (see `.python-version`) |

---

## 🗂️ Project Structure

```
marque-django-admin/
├── marque/               # Core Django project (settings, urls, wsgi)
├── users/                # User accounts, authentication, JWT utils
├── students/             # Student profiles linked to users, colleges & departments
├── colleges/             # College records
├── departments/          # Department records
├── organizations/        # Student organizations, officers, join requests & follows
├── events/               # Events, attendance logs, bookmarks & feedback
├── notifications/        # In-app notifications system
├── postman/              # Postman collection files for API testing
├── requirements.txt      # Python dependencies
├── manage.py
└── .env                  # Environment variables (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites

- Python 3.x
- MongoDB Atlas cluster (or local MongoDB instance)
- A [Cloudinary](https://cloudinary.com/) account for image uploads

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/Marque-django-admin.git
cd Marque-django-admin
```

### 3. Set Up a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root (copy from the example below):

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# MongoDB
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.xxxx.mongodb.net/marque_db?retryWrites=true&w=majority
MONGO_DB_NAME=marque_db

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser (for Django Admin)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 🔌 API Endpoints

| Prefix | Description |
|---|---|
| `POST /api/auth/login/` | User login (returns token) |
| `POST /api/auth/register/` | Register a new user |
| `GET/POST /api/colleges/` | List or create colleges |
| `GET/POST /api/departments/` | List or create departments |
| `GET/POST /api/organizations/` | List or create organizations |
| `GET/POST /api/events/` | List or create events |

> Full API documentation is available via the Postman collection in the `/postman` directory.

---

## 🗄️ Data Models Overview

### `User`
Core account model with roles (`Admin`, `Student`), contact info, and a Cloudinary profile image URL.

### `Student`
Links a `User` to a `College` and `Department` with a unique student number.

### `Organization`
Represents student organizations (Unit, Mother, or FAESO types) with social media links, a moderator, officers (`OrgOfficer`), join requests (`JoinRequest`), and followers (`FollowedOrgs`).

### `Event`
Campus events with scheduling, venue details, mandatory attendance flags, and automated reminder tracking (`remindersSent`). Related models: `AttendanceLog`, `Bookmark`, `Feedback`.

### `Notification`
In-app notifications for events, invites, role changes, and announcements, with read/unread and status tracking.

---

## 🧪 Testing with Postman

A Postman collection is included in the `/postman` (and `/.postman`) directory. Import the collection into Postman to test all available API endpoints with pre-configured request bodies and headers.

---

## 📋 Useful Commands

```bash
# Run development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Access the admin panel
# http://127.0.0.1:8000/admin/
```

---

## 🛡️ Security Notes

- Set `DEBUG=False` in production.
- Generate a strong `SECRET_KEY` for production deployments.
- Restrict `ALLOWED_HOSTS` to your actual domain(s) in `settings.py`.
- Never expose your MongoDB URI or Cloudinary credentials publicly.

---

## 📄 License

This project is for educational and internal use. Please contact the project maintainers before redistribution.
