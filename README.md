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

