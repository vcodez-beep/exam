# Exam Portal

## Overview
A comprehensive exam portal built with Flask, HTML, CSS, and PostgreSQL. This application provides a secure online examination system with anti-cheating features, user authentication, and an admin dashboard for monitoring student performance.

## Recent Changes
**November 15, 2025 - Render Deployment Configuration**
- **Fixed Render Deployment Error**:
  - Created `render.yaml` blueprint file for automatic deployment
  - Created `Procfile` with correct start command: `gunicorn main:app`
  - Fixed the `ModuleNotFoundError: No module named 'app'` error
  - The issue was Render trying to run `gunicorn app:app` instead of `gunicorn main:app`
  - Cleaned up duplicate entries in `requirements.txt`
  - Added specific versions to all dependencies for stability
  
- **Deployment Files Created**:
  - `render.yaml` - Blueprint configuration (recommended method)
  - `Procfile` - Alternative deployment configuration
  - `RENDER_DEPLOYMENT.md` - Complete step-by-step deployment guide
  
- **Deployment Guide Includes**:
  - Two deployment methods (Blueprint and Manual)
  - Database setup instructions
  - Environment variable configuration
  - First-time database initialization steps
  - Troubleshooting common issues
  - Admin login credentials

**November 15, 2025 - Beautiful White Question Boxes & Modern Exam UI**
- **Stunning Exam Page Redesign**:
  - Changed from blur green background to crisp white question cards
  - Clean, professional white boxes with subtle shadows
  - Beautiful gradient question numbers (blue to green)
  - Green gradient points badges with glow effects
  - Smooth hover animations on question cards
  - Modern option buttons with light gray background
  - Interactive hover effects that slide options to the right
  - Selected options show blue gradient background
  - Professional text inputs with focus animations
  - All elements match login/register page aesthetic
  - Enhanced readability with dark text on white cards
  
- **Advanced Browser Password Popup Prevention**:
  - Multiple layers of protection against Google/Chrome password manager
  - Hidden decoy fields to confuse password managers
  - Readonly trick - fields become editable only on click
  - `autocomplete="off"` and `autocomplete="chrome-off"` attributes
  - Prevents ALL browser save password popups completely
  - No more page reload issues from password manager dialogs
  - Works across all browsers (Chrome, Firefox, Safari, Edge)
  
- **Unblock Password Fix**:
  - Fixed password verification to properly call server endpoint `/verify_block_password`
  - Changed from hardcoded password check to secure server-side validation
  - Now correctly uses admin-configured block password (default: 'exam2024')
  - Added proper error handling with user-friendly messages
  - Real-time password verification via AJAX
  
- **Consistent Modern UI Across All Pages**:
  - Login, Register, and Exam pages now share the same design language
  - Animated gradient backgrounds (blue, green, teal)
  - Glass-morphism effects with backdrop blur
  - Professional color scheme with smooth transitions
  - All forms have consistent styling and behavior
  
- **Exam Page Dynamic Features**:
  - Dynamically renders all questions from database
  - Displays actual exam duration set by admin
  - Shows student username in header
  - Flash message support for notifications
  - All forms protected from autocomplete/password popups
  
**November 15, 2025 - Exam Duration & Timer Feature**
- **Exam Duration Control**:
  - Added duration setting in admin dashboard (configurable in minutes)
  - Default duration set to 60 minutes
  - Admin can update exam duration anytime
  
- **Timer Functionality**:
  - Live countdown timer displayed on exam page
  - Timer changes color when time is running low (orange at 5 min, red at 1 min)
  - Auto-submit when timer reaches zero
  - Timer persists even if page is reloaded (tracks elapsed time)
  
- **Updated Result Display**:
  - Students no longer see their scores/marks after completing exam
  - Simple "Exam Finished" thank you message displayed instead
  - Only admin can view student scores in the dashboard
  - Marks calculated for answered questions only

**November 15, 2025 - Major UI Enhancement & Anti-Cheating Improvements**
- **Enhanced User Interface**:
  - Completely redesigned all pages with modern, professional styling
  - Added gradient backgrounds, smooth animations, and improved color scheme
  - Implemented card-based layouts with shadows and hover effects
  - Added icons and visual indicators throughout the interface
  - Improved form inputs with better focus states and placeholders
  - Enhanced button styling with gradients and interactive feedback

- **Strengthened Anti-Cheating System**:
  - Added page reload detection (triggers password prompt)
  - Disabled F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U keyboard shortcuts
  - Enhanced copy/paste prevention with visual alerts
  - Improved tab switch detection with blur events
  - Added visual warning banner on exam page
  - Implemented session storage tracking for reload detection

- **Redesigned Admin Dashboard**:
  - Student results now display as clickable list items (name-wise)
  - Click any student name to expand and view detailed results
  - Added visual score badges for quick performance overview
  - Improved statistics display with gradient cards
  - Enhanced question management interface
  - Better table layouts with color-coded results

**November 15, 2025 - Replit Environment Setup & Render Deployment Fixes**
- **Imported GitHub project into Replit environment**
- **Installed Python 3.11** and all required dependencies (Flask, SQLAlchemy, psycopg2-binary, Werkzeug)
- **Configured PostgreSQL database** using Replit's python_database integration
- **Set up Flask workflow** to run on port 5000 with webview output
- **Seeded database** with 10 sample questions and default block password ('exam2024')

- **Fixed Critical Render Deployment Errors**:
  
  1. **Database URI Format Error** - "Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set":
     - Added automatic conversion of Render's `postgres://` URL format to SQLAlchemy 2.0+ compatible `postgresql://` format
     - This fix ensures compatibility with both Replit and Render deployment platforms
  
  2. **Python 3.13 Compatibility Error** - "AssertionError: Class SQLCoreOperations...":
     - Updated SQLAlchemy from 2.0.23 to 2.0.36 (Python 3.13 compatible)
     - Updated gunicorn to 23.0.0
     - Specified Python 3.11 in render.yaml using `pythonVersion: "3.11"`
     - Cleaned up duplicate entries in requirements.txt
  
  3. **Updated Requirements**:
     - Flask==3.0.0
     - Flask-SQLAlchemy==3.1.1
     - psycopg2-binary==2.9.9
     - Werkzeug==3.0.1
     - sqlalchemy==2.0.36 (upgraded for Python 3.13 compatibility)
     - gunicorn==23.0.0 (upgraded)

- **Updated deployment documentation** with troubleshooting steps for all common Render errors
- **Verified application** is running successfully on Replit and ready for Render deployment

**Previous Development**
- Initial project setup with Flask and PostgreSQL database
- Created user authentication system (login, registration)
- Implemented exam interface with 10 sample questions
- Added anti-cheating features (tab switch blocking, copy-paste prevention)
- Built admin dashboard with student performance analytics
- **Security improvements**:
  - Moved tab-switch password verification to server-side (prevents password exposure in page source)
  - Implemented default block password ('exam2024') so protection works immediately
  - Hidden block password in admin dashboard (masked input instead of plain text display)
  - Disabled Flask debug mode in production
  - Enhanced Flask session security with cryptographically secure random fallback (secrets.token_hex)
  - Created separate database.py module to fix circular import issues

## Features

### User Features
- User registration and secure login with modern UI
- Take exam with multiple-choice, short answer, and paragraph questions
- Enhanced anti-cheating protections:
  - Copy/paste/cut blocking with alerts
  - Right-click disabled
  - Tab switch detection and blocking
  - Page reload detection and blocking
  - Developer tools disabled (F12, Ctrl+Shift+I, etc.)
  - View source disabled (Ctrl+U)
  - Password-protected continuation after violations
  - Visual warning banner during exam
- View exam results with performance feedback
- Modern, professional UI with smooth animations

### Admin Features
- Admin login with credentials:
  - Username: `admin@vcodez`
  - Password: `admin@123`
- View student results in organized list format (name-wise)
- Click any student name to expand and view detailed exam responses
- Visual score badges for quick performance overview
- Detailed statistics with gradient cards
- View individual question responses (correct/incorrect)
- Track user scores and performance metrics
- Create new questions (MCQ, Short Answer, Paragraph)
- Delete existing questions
- Set/update the tab switch and reload block password
- View all exam questions with correct answers
- Enhanced UI with modern design and better organization

## Project Architecture

### Database Models
- **User**: Stores user credentials (username, hashed password)
- **Question**: Stores exam questions with 4 options and correct answer
- **ExamResponse**: Records user answers and whether they're correct
- **AdminSettings**: Stores admin configurations (e.g., block password)

### Routes
- `/` - Home page (redirects to login or dashboard)
- `/login` - User and admin login
- `/register` - User registration
- `/exam` - Exam interface with anti-cheating features
- `/submit_exam` - Process exam submission
- `/exam_completed` - Display user's score
- `/admin/dashboard` - Admin panel with all data
- `/admin/set_block_password` - Update tab switch password
- `/logout` - Clear session and logout

### File Structure
```
.
├── main.py                 # Flask application with all routes
├── database.py             # Database configuration and SQLAlchemy instance
├── models.py               # SQLAlchemy database models
├── seed_data.py            # Script to populate database with sample questions
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── exam.html
│   ├── exam_completed.html
│   └── admin_dashboard.html
└── static/
    └── css/
        └── style.css       # Styling for all pages
```

## Technology Stack
- **Backend**: Python Flask 3.0.0
- **Database**: PostgreSQL (via Replit integration)
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Security**: Werkzeug password hashing
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## How to Use

### For Students
1. Register with a username and password
2. Login with your credentials
3. Take the exam (tab switching will trigger a password prompt)
4. Submit your answers
5. View your score

### For Administrators
1. Login with admin credentials (`admin@vcodez` / `admin@123`)
2. View all user performance data
3. Set a password for tab switch blocking
4. Monitor individual question responses
5. View all exam questions and correct answers

## Security Features
- **Password hashing** using Werkzeug for all user credentials
- **Session-based authentication** with secure session cookies
- **Admin credentials** hardcoded as per requirements (admin@vcodez / admin@123)
- **Server-side password verification** for tab-switch blocking (password never exposed to client)
- **Default block password** ('exam2024') ensures protection works immediately
- **Anti-cheating JavaScript** prevents:
  - Copying content
  - Pasting content
  - Right-click menu
  - Tab switching without password verification
- **Cryptographically secure session keys** using environment variable (SESSION_SECRET) or secure random generation
- **Debug mode disabled** for production deployment
- **Masked admin inputs** to prevent password exposure in the UI

## Database Schema
All data is stored in PostgreSQL:
- User login credentials (hashed passwords)
- Exam questions and answers
- User responses for each question
- Whether each response is correct
- User scores and marks
- Admin settings

## Future Enhancements
- Dynamic question management (add/edit/delete questions via admin)
- Exam time limits with automatic submission
- Detailed analytics and reporting
- User result history
- Multiple exams support
- Question randomization
- Image support in questions
