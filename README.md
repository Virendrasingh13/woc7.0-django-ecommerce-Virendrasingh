# 🛒 Django E-Commerce Website

This is a **fully functional e-commerce website** built using **Django**, featuring user authentication, product management, cart functionality, order tracking, and Razorpay payment gateway integration.

---

## 🚀 Features
- ✅ **User Authentication** (Register, Login, Logout)
- ✅ **Email Verification** for Account Activation
- ✅ **Product Listings** with Categories
- ✅ **Cart System** (Add/Remove Products)
- ✅ **Razorpay Payment Gateway Integration**
- ✅ **Order Management** & History
- ✅ **Profile Management**
- ✅ **Admin Panel** for managing products & orders

---

## 📂 Project Structure
```
WOC7.0-DJANGO-ECOMMERCE-VIRENDRASINGH
│── accounts/        # User authentication & profiles
│── base/            # Core utilities & base settings
│── home/            # Home page views & templates
│── mainproject/     # Django settings & configurations
│── media/           # Uploaded images & files
│── products/        # Product models & views
│── static/          # CSS, JS, Images
│── templates/       # HTML Templates
│── db.sqlite3       # Database file (Use PostgreSQL/MySQL in production)
│── manage.py        # Django management script
│── requirements.txt # Project dependencies
```

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/ecommerce-django.git
cd ecommerce-django
```

### **2️⃣ Create & Activate Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Apply Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

### **5️⃣ Create a Superuser**
```sh
python manage.py createsuperuser
```
Follow the prompts to set up an admin user.

### **6️⃣ Run the Development Server**
```sh
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** to access the project.

---

## 📧 Email Verification Setup
This project uses **SMTP Email** for account activation. Update your **`settings.py`** with valid email credentials:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password for Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> **Gmail Users:** If using **Gmail SMTP**, enable **App Passwords** in your Google account.

---

## 💳 Razorpay Payment Gateway Integration
This project integrates **Razorpay** for online payments. Update your **`settings.py`** with your Razorpay API credentials:

```python
RAZORPAY_KEY_ID = 'your_razorpay_key'
RAZORPAY_KEY_SECRET = 'your_razorpay_secret'
```

> **Note:** Make sure you have a **Razorpay Business Account** to obtain the API keys.

---

## 🎯 Next Steps
- **Deploy on Heroku, AWS, or DigitalOcean**
- **Use PostgreSQL or MySQL for production**
- **Implement Docker for containerization**
- **Enhance UI with Tailwind CSS or Bootstrap**

---

## 📜 License
This project is **open-source** and free to use.

---

### **📌 Notes**
- Replace `yourusername` in the GitHub clone URL.
- Add real **email & Razorpay credentials** in `settings.py`.
- This README ensures **anyone can install, run, and understand your project**.

---

🔥 Let me know if you need any improvements! 🚀

