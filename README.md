# Passport Automation System

A web-based passport application and generation system built with Flask and MongoDB. This system allows users to register, submit passport applications, and generate digital passport documents.

## Features

- **User Registration & Authentication**: Secure user registration and login system
- **Multi-Step Application Process**: 
  - Personal Details (Name, Nationality, Place of Birth)
  - Photo & Signature Upload
  - Residential Details
  - Government ID Verification
  - Payment Processing
- **Digital Passport Generation**: Automated PDF passport creation with user photos and signatures
- **Document Download**: Generated passports available for download
- **MongoDB Integration**: Secure data storage with MongoDB

## Technology Stack

- **Backend**: Python Flask
- **Database**: MongoDB
- **Image Processing**: PIL (Python Imaging Library)
- **Frontend**: HTML, CSS, JavaScript
- **File Handling**: Base64 encoding for image storage

## Project Structure

```
PASSPORT AUTOMATION SYSTEM/
├── app.py                    # Main Flask application
├── generated_passport.py     # Passport PDF generation script
├── check_tables.py          # Database table verification
├── check_users.py           # User data verification
├── database.db             # SQLite database (if used)
├── downloads/              # Generated passport PDFs
├── static/
│   ├── Assert/
│   │   └── passport_template.png  # Passport template image
│   ├── uploads/            # User uploaded files
│   ├── videos/             # Demo videos
│   └── Scanner.jpeg        # Scanner image asset
└── templates/              # HTML templates
    ├── index.html          # Home page
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── personal_details.html
    ├── residential_details.html
    ├── id_verification.html
    ├── payment.html
    ├── success.html
    ├── users.html
    └── styles.css          # Stylesheet
```

## Installation

### Prerequisites

- Python 3.7+
- MongoDB
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "PASSPORT AUTOMATION SYSTEM"
   ```

2. **Install required packages**
   ```bash
   pip install flask pymongo pillow werkzeug
   ```

3. **Start MongoDB**
   - Ensure MongoDB is running on `localhost:27017`
   - The application will create a database named `flaskdatabase`

4. **Prepare passport template**
   - Ensure `passport_template.png` exists in `static/Assert/`
   - This template is used for generating passport PDFs

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Usage

### For Users

1. **Registration**: Create a new account with username and password
2. **Login**: Access your account with credentials
3. **Application Process**:
   - Fill personal details (name, nationality, place of birth)
   - Upload passport photo and signature
   - Complete residential details
   - Verify government ID
   - Process payment
4. **Download Passport**: Generate and download your digital passport PDF

### For Developers

- **Database Operations**: User data is stored in MongoDB with Base64 encoded images
- **Passport Generation**: The `generated_passport.py` script creates PDF passports using PIL
- **Session Management**: Flask sessions handle user authentication
- **File Security**: Uploaded files are converted to Base64 for secure storage

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/personal-details` | GET, POST | Personal information form |
| `/residential-details` | GET, POST | Address information |
| `/id-verification` | GET, POST | Government ID verification |
| `/payment` | GET, POST | Payment processing |
| `/success` | GET | Application success page |
| `/download-passport` | GET | Generate and download passport PDF |
| `/logout` | GET | User logout |

## Database Schema

### Users Collection (MongoDB)

```javascript
{
  username: String,
  password: String,
  full_name: String,
  nationality: String,
  place_of_birth: String,
  passport_photo: String,    // Base64 encoded
  signature_photo: String,   // Base64 encoded
  passport_type: String,     // Default: "P"
  country_code: String,      // Default: "IND"
  passport_no: String,       // Auto-generated
  date_of_issue: String,     // Current date
  date_of_expiry: String     // Default: "22-09-2028"
}
```

## Configuration

### Environment Variables

- `MONGODB_URI`: MongoDB connection string (default: `mongodb://localhost:27017/`)
- `SECRET_KEY`: Flask secret key for sessions
- `UPLOAD_FOLDER`: Directory for file uploads
- `DOWNLOAD_FOLDER`: Directory for generated passports

### Customization

- **Passport Template**: Replace `static/Assert/passport_template.png` with your design
- **Text Positions**: Modify `TEXT_POSITIONS` in `generated_passport.py`
- **Image Sizes**: Adjust photo and signature dimensions in the generation script

## Security Features

- Password-based authentication
- Session management
- Secure file upload with Base64 encoding
- Input validation and sanitization
- CSRF protection through Flask sessions

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB service is running
   - Check connection string in `app.py`

2. **Template Not Found**
   - Verify `passport_template.png` exists in `static/Assert/`
   - Check file permissions

3. **Font Loading Error**
   - Install Arial Bold font or modify font path in `generated_passport.py`
   - Fallback to default font if Arial not available

4. **PDF Generation Fails**
   - Check user has uploaded both photo and signature
   - Verify PIL/Pillow installation
   - Ensure sufficient disk space in downloads folder

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request


## Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

## Future Enhancements

- [ ] Email notifications for application status
- [ ] Admin dashboard for application management
- [ ] Payment gateway integration
- [ ] Document verification with AI/ML
- [ ] Multi-language support
- [ ] Mobile responsive design improvements
- [ ] Automated testing suite
- [ ] Docker containerization