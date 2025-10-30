
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