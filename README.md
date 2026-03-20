# 🎯 MHT CET Score Calculator

A web-based tool to calculate your **MHT CET** score from your official response sheet. Upload your response sheet HTML file and instantly get subject-wise marks breakdown for Physics, Chemistry, and Mathematics.

---

## ✨ Features

- 📄 Upload your MHT CET response sheet (HTML file) directly in the browser
- 📊 Calculates **subject-wise marks** for Physics, Chemistry, and Mathematics
- ✅ Shows correct, incorrect, and unattempted question counts per subject
- 🧮 Applies correct marking scheme (Maths = 2 marks, Physics/Chemistry = 1 mark each)
- 👤 Extracts candidate personal details (Name, Application No, Roll No)
- 💾 Saves all results to a CSV file for record keeping
- 🌐 Simple web interface served via Flask

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, BeautifulSoup4
- **Frontend:** HTML, CSS, JavaScript
- **Data Storage:** CSV (local)

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/Piyush2182/Mht-cet-score-calculator.git
cd Mht-cet-score-calculator
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the Flask server**

```bash
python main.py
```

**4. Open in browser**

```
http://localhost:5000
```

---

## 🚀 How to Use

1. Log in to the official MHT CET portal and open your **response sheet**
2. Save the page as an HTML file (`Ctrl+S` → Save as "Webpage, HTML only")
3. Open the app at `http://localhost:5000`
4. Upload the saved HTML file using the file input
5. Click **Calculate** to see your score breakdown

---

## 📁 Project Structure

```
Mht-cet-score-calculator/
├── main.py                  # Flask backend + parsing logic
├── index.html               # Frontend UI
├── my_response_sheet.html   # Sample response sheet (for testing)
├── requirements.txt         # Python dependencies
└── data/
    └── mht_cet_results.csv  # Auto-generated results log
```

---

## ⚠️ Note

> The MHT CET response sheet is behind a login portal. This tool does **not** auto-fetch the sheet. You need to manually save the HTML file from the official portal and upload it to the calculator.

---

## 🙋‍♂️ Author

**Piyush** — [GitHub](https://github.com/Piyush2182)

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
