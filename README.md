
# 🎓 Smart Attendance System

A **face recognition-based attendance system** using OpenCV and Tkinter. This project captures faces via webcam, recognizes them in real-time, and records attendance in a CSV file. It's simple, fast, and works offline.

---

## 📌 Features

- 📷 Real-time face detection and recognition
- 🧠 Trains images using LBPH Face Recognizer
- 🗂 Stores attendance in a `.csv` file with timestamp
- 🧾 CSV used as the database
- 🔒 Password protection for admin functions
- 📢 Voice prompts (TTS)
- 📩 Optional SMS alerts (customizable)

---

## 📥 Installation

### 1. Clone the repository

```bash
git clone https://github.com/RitiChandak/Smart-Attendance-System.git
cd Smart-Attendance-System

pip install -r requirements.txt
Or just run
python install.py
```

### 2. (Optional) Set up a virtual environment
```
python -m venv venv
```
#### On Windows:
```
venv\Scripts\activate
```
#### On macOS/Linux:
```
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```
Or just run:
```
python install.py
```
## 🚀 How to Run
Once installed, run the app using:

```
python main.py
```
Make sure your webcam is enabled. You’ll see a GUI interface for registering new users, taking attendance, training data, etc.

## 🧪 Requirements

- Python 3.x
- OpenCV
- NumPy
- Pillow (PIL)
- pandas
- twilio(optional)

These are listed in requirements.txt and will be installed automatically.

## 💡 Tips
- Make sure haarcascade_frontalface_default.xml is in the correct path
- You may need to configure your sms.py and voicetts.py files to use real APIs
- Admin passwords are stored in plain text — change that if you're deploying in production

# 🧑‍💻 Author
Made with ❤️ by Riti Chandak & Swadha Thakkar

Feel free to fork, star ⭐ the repo, or contribute!
