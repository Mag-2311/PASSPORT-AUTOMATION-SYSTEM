import os
import sys
import random
import string
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pymongo
import base64
from io import BytesIO

# Database Configuration
DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "flaskdatabase"
COLLECTION_NAME = "users"

# Paths
TEMPLATE_PATH = "static/Assert/passport_template.png"
DOWNLOAD_FOLDER = "downloads/"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Image Placement Positions
PHOTO_POSITION = (38, 395)  # Passport photo position
SIGN_POSITION = (60, 860)  # Signature position

# Text Positions (Ensuring Type & Country Code are included)
TEXT_POSITIONS = {
    "Type": (535, 462),
    "Country Code": (943, 462),
    "Passport No": (1440, 462),
    "Given Name": (525, 665),
    "Nationality": (1420, 664),
    "Place of Birth": (990, 900),
    "Date of Issue": (550, 1130),
    "Date of Expiry": (1450, 1130),
}

# Default values
DEFAULT_TYPE = "P"
DEFAULT_COUNTRY_CODE = "IND"

def get_database():
    """Connect to MongoDB and return the users collection."""
    client = pymongo.MongoClient(DB_HOST, DB_PORT)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def generate_passport_number():
    """Generate a random passport number (8 characters)."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def get_current_date():
    """Return the current date in DD-MM-YYYY format."""
    return datetime.now().strftime("%d-%m-%Y")

def fetch_user_details(username):
    """Retrieve user details from the database."""
    users = get_database()
    user_data = users.find_one({"username": username})
    
    if not user_data:
        print(f"❌ User '{username}' not found in database!")
        sys.exit(1)

    return {
        "Type": user_data.get("passport_type", DEFAULT_TYPE),
        "Country Code": user_data.get("country_code", DEFAULT_COUNTRY_CODE),
        "Given Name": user_data.get("full_name", "Unknown"),
        "Nationality": user_data.get("nationality", "Unknown"),
        "Place of Birth": user_data.get("place_of_birth", "Unknown"),
        "Passport No": user_data.get("passport_no", generate_passport_number()),  # Generate if missing
        "Date of Issue": user_data.get("date_of_issue", get_current_date()),
        "Date of Expiry": user_data.get("date_of_expiry", "22-09-2028"),  # Example expiry date
        "Passport Photo": user_data.get("passport_photo", None),  # Base64
        "Signature": user_data.get("signature_photo", None),  # Base64
    }

def decode_image(base64_string):
    """Convert Base64 image string to a PIL Image."""
    if not base64_string:
        return None

    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))

def generate_passport(username):
    """Generate a passport PDF for a user."""
    user_details = fetch_user_details(username)
    output_filename = os.path.join(DOWNLOAD_FOLDER, f"passport_{username}.pdf")

    # Load passport template
    if not os.path.exists(TEMPLATE_PATH):
        print("❌ Passport template not found!")
        sys.exit(1)

    template = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(template)

    # Load bold font
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 50)  # Bold font
    except IOError:
        font_bold = ImageFont.load_default()

    # Write text details in bold
    for key, value in TEXT_POSITIONS.items():
        draw.text(value, user_details.get(key, ""), font=font_bold, fill="black")

    # Decode and paste Passport Photo
    passport_photo = decode_image(user_details["Passport Photo"])
    if passport_photo:
        passport_photo = passport_photo.resize((400, 400))  # Adjust size as needed
        template.paste(passport_photo, PHOTO_POSITION)

    # Decode and paste Signature
    signature = decode_image(user_details["Signature"])
    if signature:
        signature = signature.resize((490, 155))  # Adjust size as needed
        template.paste(signature, SIGN_POSITION)

    # Save the final passport
    template.save(output_filename, "PDF")
    print(f"✅ Passport successfully saved at: {output_filename}")

    return output_filename

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python generated_passport.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    generate_passport(username)
