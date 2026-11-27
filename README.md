
# 🔍 FindIT — Campus Lost & Found Network

> **Connecting Lost Things to Their Rightful Owners**

**FindIT** is a centralized desktop application built with **Python**, **CustomTkinter**, and **SQLite** to streamline lost-and-found reporting across a university campus. Instead of relying on scattered WhatsApp messages or physical notice boards, students and staff can report, search, filter, and claim lost items in one clean interface.

---

## ✨ Key Features

* **Campus Profile Authentication:** Secure user registration and login backed by parameterized SQLite queries to prevent SQL injection.
* **Report Lost & Found Items:** Structured item posting with category tags (`ID Card / Documents`, `Electronics`, `Keys`, `Books/Notes`, `Water Bottle / Bag`), campus locations, descriptions, and contact info.
* **Real-Time Search & Multi-Filter Engine:** Instant keyword search combined with category and Lost/Found status filters (`<50ms` local query response).
* **Ownership-Based Post Management:** Contextual three-dot menu (`...`) rendered *only* for the original post creator (`item.user_id == current_user_id`) to prevent unauthorized deletions.
* **Modular MVC Architecture:** Clean separation between the SQLite database layer (`database.py`) and CustomTkinter UI layer (`main.py`).

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **GUI Framework:** CustomTkinter (`v5.2+`)
* **Database:** SQLite3 (`sqlite3` built-in module)
* **Architecture:** Model-View-Controller (MVC)

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone (https://github.com/mominsana0510-bot/FindIT-Lost-and-Found)
