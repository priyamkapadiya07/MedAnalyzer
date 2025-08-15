# 🏥 MedAnalyzer - Medical Report Analysis System

A comprehensive Django-based web application that uses OCR, Machine Learning, and AI to analyze medical reports and provide disease predictions with medication suggestions.

## 🚀 Features

### Core Functionality
- **📄 Medical Report Upload**: Support for PDF and image formats (PNG, JPG, JPEG, BMP, TIFF)
- **🔍 OCR Text Extraction**: Automatic text extraction from scanned reports using Tesseract OCR
- **🤖 AI-Powered Analysis**: Machine learning models for disease prediction
- **💊 Medicine Suggestions**: Automated medication recommendations based on detected conditions
- **📊 Report History**: Track and manage all uploaded reports
- **💬 AI Chatbot**: Interactive medical consultation using Google Gemini AI
- **📧 Email Integration**: Send reports via email with PDF generation
- **❓ Q&A System**: Submit medical questions to healthcare professionals

### Disease Detection
The system can detect and analyze:
- **Diabetes** (based on glucose levels)
- **Anemia** (based on hemoglobin levels)
- **Heart Disease** (based on cholesterol levels)
- **Infections** (based on WBC count)
- **Blood Disorders** (Leukopenia, Thrombocytopenia, etc.)
- **Inflammatory Conditions** (based on ESR levels)

### Security & User Management
- **🔐 Custom Authentication**: Secure user registration and login system
- **👤 User Profiles**: Personalized dashboard for each user
- **🛡️ Session Management**: Secure session handling
- **🔒 Data Privacy**: User-specific report access

## 🛠️ Technology Stack

- **Backend**: Django 5.1.7 (Python)
- **Database**: SQLite3
- **OCR**: Tesseract OCR with pytesseract
- **ML Models**: Scikit-learn (Logistic Regression)
- **AI Integration**: Google Gemini API
- **PDF Processing**: PyMuPDF, pdf2image
- **PDF Generation**: xhtml2pdf
- **Frontend**: HTML, CSS, JavaScript
- **Email**: Django SMTP with Gmail

## 📋 Prerequisites

- Python 3.8+
- Tesseract OCR installed on your system
- Google Gemini API key
- Gmail account for email functionality

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/priyamkapadiya07/MedAnalyzer.git
cd MedAnalyzer
```

### 2. Create Virtual Environment
```bash
python -m venv myenv
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django==5.1.7
pip install pytesseract
pip install Pillow
pip install scikit-learn
pip install joblib
pip install PyMuPDF
pip install pdf2image
pip install xhtml2pdf
pip install python-decouple
pip install python-dotenv
pip install google-generativeai
pip install django-markdownify
```

### 4. Install Tesseract OCR
- **Windows**: Download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Ubuntu**: `sudo apt-get install tesseract-ocr`

### 5. Environment Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 6. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
# Username: priyam
# Password: 12345
```

### 8. Run the Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```
medical_analyzer/
├── analyzer_app/                 # Main Django app
│   ├── ml_model/                # Machine learning models
│   │   ├── anemia_model.pkl     # Trained anemia detection model
│   │   ├── diabetes_model.pkl   # Trained diabetes detection model
│   │   ├── heart_model.pkl      # Trained heart disease model
│   │   ├── anemia_dataset.csv   # Training dataset
│   │   └── anemia_model.py      # Model training script
│   ├── static/                  # Static files (CSS, JS, images)
│   ├── templates/               # HTML templates
│   ├── migrations/              # Database migrations
│   ├── models.py               # Database models
│   ├── views.py                # Application views
│   ├── forms.py                # Django forms
│   ├── ocr_utils.py            # OCR and ML utilities
│   └── decorators.py           # Custom decorators
├── media/                       # Uploaded files
│   └── reports/                # Medical reports storage
├── medical_analyzer/           # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── myenv/                      # Virtual environment
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
└── .env                        # Environment variables
```

## 🎯 Usage

### 1. User Registration & Login
- Create a new account or login with existing credentials
- Secure session management with custom authentication

### 2. Upload Medical Reports
- Navigate to "Upload Report" section
- Upload PDF or image files of medical reports
- System automatically extracts text and analyzes data

### 3. View Analysis Results
- Review extracted medical values
- Check disease predictions
- View medication suggestions
- Download or email PDF reports

### 4. Report Management
- Access report history
- Delete old reports
- Track analysis over time

### 5. AI Chatbot Consultation
- Ask medical questions to the AI assistant
- Get instant responses powered by Google Gemini
- Clear chat history when needed

### 6. Q&A System
- Submit questions to healthcare professionals
- Receive email notifications for responses

## 🧠 Machine Learning Models

The system uses three trained models:

### 1. Diabetes Detection Model
- **Algorithm**: Logistic Regression
- **Feature**: Glucose levels
- **Threshold**: Based on standard medical ranges

### 2. Anemia Detection Model
- **Algorithm**: Logistic Regression
- **Feature**: Hemoglobin levels
- **Gender-specific**: Different ranges for males/females

### 3. Heart Disease Model
- **Algorithm**: Logistic Regression
- **Feature**: Cholesterol levels
- **Threshold**: <200 mg/dL (desirable)

## 📊 Supported Medical Parameters

| Parameter | Normal Range | Unit | Conditions Detected |
|-----------|--------------|------|-------------------|
| Glucose | 70-99 mg/dL (fasting) | mg/dL | Diabetes |
| Hemoglobin | 13.5-17.5 g/dL (M), 12.0-15.5 g/dL (F) | g/dL | Anemia |
| Cholesterol | <200 mg/dL | mg/dL | Heart Disease |
| WBC | 4,000-11,000 | /µL | Infection/Leukopenia |
| PLT | 150,000-450,000 | /µL | Thrombocytopenia/Thrombocytosis |
| MCV | 80-100 | fL | Microcytic/Macrocytic Anemia |
| ESR | 0-20 | mm/hr | Inflammation |

## 🔧 Configuration

### Email Settings
Update `settings.py` with your email configuration:
```python
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
ADMIN_EMAIL = 'admin@example.com'
```

### Tesseract Path
Update the Tesseract path in `ocr_utils.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 🚨 Important Notes

- **Medical Disclaimer**: This system is for educational purposes only and should not replace professional medical advice
- **Data Privacy**: All uploaded reports are stored securely and accessible only to the respective user
- **API Limits**: Google Gemini API has usage limits; monitor your quota
- **File Formats**: Ensure medical reports are in supported formats (PDF, PNG, JPG, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Priyam Kapadiya**
- GitHub: [@priyamkapadiya07](https://github.com/priyamkapadiya07)
- Email: priyampatel968@gmail.com

## 🙏 Acknowledgments

- Django framework for robust web development
- Tesseract OCR for text extraction capabilities
- Scikit-learn for machine learning models
- Google Gemini AI for intelligent chatbot functionality
- All contributors and the open-source community

## 📞 Support

For support, email priyampatel968@gmail.com or create an issue in the GitHub repository.

---

**⚠️ Medical Disclaimer**: This application is designed for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
