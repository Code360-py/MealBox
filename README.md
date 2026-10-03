# MealBox v2.0

A lightweight, modern recipe discovery platform and culinary companion powered by [TheMealDB](https://www.themealdb.com/). Available as both a full-stack Django web service and a standalone, hardware-accelerated Android mobile app.

- **Live Web Application**: [https://xenonstudio.pythonanywhere.com](https://xenonstudio.pythonanywhere.com)
- **Android APK Binary**: [Download Latest Build (`MealBox.apk`)](https://github.com/Code360-py/MealBox/releases/latest)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Repository Structure](#repository-structure)
- [Local Setup & Development](#local-setup--development)
  - [1. Web App (Django)](#1-web-app-django)
  - [2. Mobile App (Android Toolchain via CLI/Termux)](#2-mobile-app-android-toolchain-via-clitermux)
- [Authentication Model](#authentication-model)
- [Deployment](#deployment)
- [License & Credits](#license--credits)

---

## Overview

MealBox delivers an ad-free, mobile-first culinary browsing experience. It pulls global recipes, instructional media, and ingredient measurements from TheMealDB API, presenting them in a dark neon iOS-inspired design system.

The repository supports dual deployment:
1. **The Web Engine (`Meal/`)**: A modular Django application implementing custom session-based security without Django’s default auth/admin bloat.
2. **The Standalone Android Client (`android/`)**: A lightweight native Android wrapper with zero Android Studio/Gradle dependencies. It compiles directly through CLI tools (`aapt2`, `d8`, `javac`) and features system theme auto-synchronization, gesture-driven pull-to-refresh, hardware back-navigation, and local storage backup bridges.

---

## Key Features

### 🍽️ Recipe Discovery & Smart Assistant
- **Global Category Filter**: Instant filtering across Vegetarian, Seafood, Chicken, Beef, Dessert, Pasta, and more.
- **Real-Time Search**: Query dishes by name with persistent query history stored in `localStorage`.
- **Smart Assistant Sheet**: An interactive slide-up drawer offering:
  - **Surprise Me**: One-touch random recipe generator respecting dietary constraints.
  - **Dietary Filter**: Dynamic view adjustment for specific diets.
  - **Measurement Units**: Switch between Metric (`g`, `ml`) and Imperial (`oz`, `cups`).
- **Rich Recipe Breakdown**: Labeled ingredient lists, instructions, and YouTube video links.

### 🌓 Adaptive System Themes & AMOLED Mode
- **System Sync**: Native Java detection reads phone-level dark mode settings and updates the UI accordingly.
- **Theme Switcher**: Choose between Auto (System), Dark, or Light themes.
- **AMOLED Pure Black**: Enables absolute `#000000` dark surfaces for OLED power savings.

### 📱 Android Integration & Offline UX
- **Native Gesture Pull-to-Refresh**: Top-level drag gesture detects touch overscroll and reloads current views without page reloads.
- **Network Status Banner**: Automatic online/offline transition alerts.
- **Hardware Back Button Handling**: Managed in-app view stack (Details → Category → Home → Double-tap to exit).
- **Backup & Restore**: Native direct-to-disk export (`MealBox_Backup_<timestamp>.json`) into `/sdcard/Download/` alongside clipboard copy/paste fallback.

### ✨ Occasion Animations (Festive Sprinkles)
- ❄️ **Christmas**: Gentle falling snowflake physics engine.
- 🪔 **Diwali**: Golden sparks, floating diya embers, and curated Indian festival specials.
- 🎂 **Birthday**: Multi-color fluttering celebration confetti.

---

## Architecture & Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.10+, Django 6.1.1, Requests, WhiteNoise |
| **Android Wrapper** | Android SDK 30, Java (Activity + WebView), `aapt2`, `d8`, `apksigner` |
| **Frontend** | Bootstrap 5.3.8, HTML5 Canvas, Vanilla ES6+ JavaScript |
| **Styling & Assets**| Custom Neon CSS Tokens, Font Awesome 6.5+, Noto Sans (Google Fonts) |
| **Data Source** | [TheMealDB API](https://www.themealdb.com/api.php) |

## Repository Structure
MealBox/
├── android/                   # Standalone Android native wrapper & APK pipeline
│   ├── AndroidManifest.xml   # App manifest, permissions, launcher icon config
│   ├── assets/               # WebView client (index.html, css/style.css)
│   ├── build.sh              # Headless CLI build script (compiles, signs, aligns)
│   ├── res/                  # Vector drawables, mipmaps, and XML layouts
│   └── src/                  # Native Java source code (MainActivity.java)
├── Meal/                      # Django application package
│   ├── auth.py               # Custom session authentication logic
│   ├── models.py             # User and database schemas
│   ├── static/               # Web static files (CSS, JS)
│   ├── templates/            # Django HTML templates
│   ├── urls.py               # URL routing definitions
│   └── views.py              # Application views & API controllers
├── manage.py
├── requirements.txt
└── README.md

## Local Setup & Development
## ​1. Web App (Django)
'''bash
# Clone the repository
git clone https://github.com/Code360-py/MealBox.git
cd MealBox

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start development server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
'''
