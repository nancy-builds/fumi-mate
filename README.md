# Xoá file SQLite cũ
rm instance/app.db  # hoặc nơi bạn lưu file db

# Sau đó chạy lại
flask db init
flask db migrate -m "initial migration"
flask db upgrade

## 🚀 Installation & Setup


1. **Clone the repository**
   ```bash
   git clone https://github.com/nancy-builds/kltn.git
   cd kltn
   
2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
Download from: [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   
   **Steps:**
   1. Run the installer.
   2. Select **C++ build tools**.
   3. Make sure **MSVC v143** and **Windows 10 SDK** are checked.
   4. Click **Install** and wait for the installation to complete.
   5. **Restart your computer**.

   Open a terminal in your project folder and run: 

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations (if any)**
   ```bash
   flask db upgrade
   ```

5. **Run the app**

   ```bash
   flask run
   ```

---

## 📂 Project Structure

```plaintext
project/
├── app.py
├── config.py
├── requirements.txt
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── models/          # Database models
├── utils/           # Helper functions
└── tests/           # Unit + Selenium tests
```

---

## 🧑‍💻 Usage

* **Portfolio** → `/portfolio`
* **Blog** → `/blog`
* **Flashcards** → `/flashcards`
* **Games** → `/games`

Demo login (optional):

```
Username: sagey
Password: sage
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch (`feature/xyz`)
3. Commit your changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify with attribution.

---

## 📬 Contact

👩‍💻 **Developers**:

* \[Nancy] – [GitHub](https://github.com/nancy-builds)



pip install python-dotenv
flask seed-db

 capture what's currently working:
bashpip freeze > requirements.txt