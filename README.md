# 🎓 Online Tuition Management System (Django + DRF)

An advanced **Online Tuition Management System** built with **Django Rest Framework (DRF)**.  
This system manages **Tutors, Students, Parents, Courses, and Assignments** with role-based access control using **Custom JWT Authentication**.

---

## 🚀 Features

### 👨‍🏫 Tutors
- Can **create, update, and delete** their own courses.  
- Can create **assignments** only for the courses they own.  
- Can manage enrolled students in their courses.

### 🎓 Students
- Can **browse and enroll** in available courses.  
- Can **submit assignments** only for the courses they are enrolled in.  
- Can update their own profile.

### 👪 Parents
- Can **monitor their children’s enrolled courses**.  
- Can **view assignment progress** and submissions.  
- Cannot directly create/update courses or assignments.

### 👨‍💻 Admin
- Full control over all modules (Users, Tutors, Students, Courses, Assignments).  
- Can assign roles and permissions.

### 🔑 Authentication & Security
- Custom **JWT Authentication** (Login & Register APIs).  
- Role-based access (Only tutors can create courses, only enrolled students can submit assignments).  
- Secure CRUD operations with permissions & throttling.

---

## 🏗 Project Structure

online_tuition_project/
│── users/ # Custom User model (roles: admin, tutor, student, parent)
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│


│── courses/ # Course Management
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│


│── assignments/ # Assignment Management
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│

│── students/ # Enrollment & Submissions
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
│── tutors/ # Tutor profiles and permissions
│

│── settings.py # Project configurations (JWT, filters, permissions)
│── urls.py # Root project urls


---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/online-tuition.git
   cd online-tuition

2. Create a virtual environment & activate:
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
3. Install dependencies:
   pip install -r requirements.txt
4. Run migrations:
   Run migrations:
5. Create a superuser:
   python manage.py createsuperuser
6. Start the development server:
   python manage.py runserver
📌 API Endpoints (Overview)
👥 Users

   POST /api/auth/register/ → Register new user.

   POST /api/auth/login/ → Login (JWT).

   GET /api/users/ → List all users (admin only).

📚 Courses

   POST /api/courses/ → Tutor creates course.

   PUT /api/courses/{id}/ → Only creator tutor can update.

   DELETE /api/courses/{id}/ → Only creator tutor can delete.

   GET /api/courses/ → List all courses.

📝 Assignments

   POST /api/assignments/ → Tutor creates assignment for their course.

   GET /api/assignments/ → List assignments (filter by course/tutor).

   POST /api/assignments/{id}/submit/ → Student submits assignment (only if enrolled).

🎓 Enrollments

   POST /api/courses/{id}/enroll/ → Student enrolls in course.

   GET /api/students/enrollments/ → Student views their courses.



