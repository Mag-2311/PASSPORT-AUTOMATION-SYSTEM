import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from flask import send_from_directory
import base64
import time
import subprocess
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Connect to MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["flaskdatabase"]
    users_collection = db["users"]
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print("❌ Error connecting to MongoDB:", e)

# ✅ Create Upload Folder
# Define upload and download folders
download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)


# ✅ Home Route
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users_collection.find_one({"username": username}):
            flash("⚠️ Username already exists.", "danger")
            return redirect('/register')

        users_collection.insert_one({
            "username": username,
            "password": password,
            "full_name": "",
            "nationality": "",
            "place_of_birth": "",
            "passport_photo": "",
            "signature_photo": ""
        })

        flash("✅ Registration successful! You can now log in.", "success")
        return redirect('/login')

    return render_template('register.html')

# ✅ Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})

        if user and user['password'] == password:
            session['username'] = username
            flash("✅ Login successful!", "success")
            return redirect('/personal-details')
        else:
            flash("⚠️ Invalid credentials, please try again.", "danger")
            return redirect('/login')

    return render_template('login.html')

# ✅ Step 1: Personal Details
@app.route('/personal-details', methods=['GET', 'POST'])
def personal_details():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        nationality = request.form.get('nationality')
        place_of_birth = request.form.get('place_of_birth')

        passport_photo = request.files.get('passport_photo')
        signature_photo = request.files.get('signature_photo')

        passport_photo_data = None
        signature_photo_data = None

        if passport_photo and passport_photo.filename:
            passport_photo_data = base64.b64encode(passport_photo.read()).decode('utf-8')  # Convert to Base64

        if signature_photo and signature_photo.filename:
            signature_photo_data = base64.b64encode(signature_photo.read()).decode('utf-8')  # Convert to Base64

        update_data = {
            "full_name": full_name,
            "nationality": nationality,
            "place_of_birth": place_of_birth,
            "passport_photo": passport_photo_data,  # Storing the image binary data
            "signature_photo": signature_photo_data  # Storing the image binary data
        }

        result = users_collection.update_one(
            {"username": session['username']},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            flash("✅ Personal details saved successfully!", "success")
        else:
            flash("⚠️ No changes made or failed to save.", "warning")

        return redirect(url_for('residential_details'))  # Navigate to next step

    return render_template('personal_details.html', username=session['username'])

# ✅ Step 2: Residential Details
@app.route('/residential-details', methods=['GET', 'POST'])
def residential_details():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        return redirect('/id-verification')

    return render_template('residential_details.html', username=session['username'])

# ✅ Step 3: Govt ID Verification
@app.route('/id-verification', methods=['GET', 'POST'])
def id_verification():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        return redirect('/payment')

    return render_template('id_verification.html', username=session['username'])

# ✅ Step 4: Payment
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        return redirect('/success')

    return render_template('payment.html', username=session['username'])

# ✅ Step 5: Success Page
@app.route('/success')
def success():
    if 'username' not in session:
        return redirect('/login')

    return render_template('success.html', username=session['username'])

@app.route('/download-passport')
def download_passport():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    passport_file = os.path.join(download_folder, f"passport_{username}.pdf")

    try:
        # ✅ Run generated_passport.py to create passport
        subprocess.run(
            ["python", "generated_passport.py", username, passport_file],
            check=True, capture_output=True, text=True
        )

        # ✅ Wait for the file to be created (max 10 seconds)
        start_time = time.time()
        while not os.path.exists(passport_file):
            if time.time() - start_time > 10:
                raise TimeoutError("Passport generation timed out")
            time.sleep(0.5)

        # ✅ Serve the generated file
        return send_file(passport_file, as_attachment=True)

    except subprocess.CalledProcessError as e:
        print(f"❌ Generation failed: {e.stderr}")
        flash("⚠️ Passport generation failed. Please try again.", "danger")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        flash("⚠️ Internal server error during generation.", "danger")

    return redirect('/success')

@app.context_processor
def inject_username():
    """Make username available in all templates"""
    return dict(username=session.get('username'))



# ✅ Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("✅ Logged out successfully!", "success")
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = "your_secret_key_here"
    app.run(debug=True)