from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# -------------------------
# Create Database
# -------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood_group TEXT,
        city TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------------
# Home Page
# -------------------------
@app.route('/')
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    conn.close()

    return render_template("index.html", total_donors=total_donors)

# -------------------------
# Register Donor
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        city = request.form['city']
        phone = request.form['phone']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO donors(name, age, blood_group, city, phone)
        VALUES (?, ?, ?, ?, ?)
        """, (name, age, blood_group, city, phone))

        conn.commit()
        conn.close()

        return """
        <h2>✅ Registration Successful!</h2>
        <br>
        <a href='/'>Go Home</a>
        """

    return render_template("register.html")

# -------------------------
# Search Donor
# -------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():

    donors = []

    if request.method == 'POST':

        blood_group = request.form['blood_group']

        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM donors WHERE blood_group=?",
            (blood_group,)
        )

        donors = cursor.fetchall()

        conn.close()

    return render_template("search.html", donors=donors)

# -------------------------
# View All Donors
# -------------------------
@app.route('/donors')
def donors():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donors")

    donor_list = cursor.fetchall()

    conn.close()

    return render_template("donors.html", donors=donor_list)

# -------------------------
# Emergency Page
# -------------------------
@app.route('/emergency', methods=['GET', 'POST'])
def emergency():

    if request.method == 'POST':
        return """
        <h2 style='color:green; text-align:center; margin-top:50px;'>
        ✅ Your emergency blood request has been submitted successfully.
        <br><br>
        Our team will contact suitable donors as soon as possible.
        </h2>

        <div style='text-align:center; margin-top:30px;'>
            <a href='/'>
                <button>Go Back to Home</button>
            </a>
        </div>
        """

    return render_template("emergency.html")

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)