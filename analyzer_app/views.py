from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UploadForm
from .models import Report,UserProfile,UserQuestion
from .ocr_utils import predict_diseases, suggest_medicines,extract_report_data
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import WebsiteUserSignUpForm, WebsiteUserLoginForm
from .decorators import custom_login_required
import traceback
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import google.generativeai as genai 
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL_NAME = 'gemini-2.5-flash'
try:
    gemini_model = genai.GenerativeModel(
        GEMINI_MODEL_NAME,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    gemini_model = None

def signup(request):
    if request.method == 'POST':
        form = WebsiteUserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']
            hashed_password = make_password(raw_password)

            if UserProfile.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif UserProfile.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                UserProfile.objects.create(
                    username=username,
                    email=email,
                    password=hashed_password
                )
                messages.success(request, "Account created! Please log in.")
                return redirect('login')
    else:
        form = WebsiteUserSignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = WebsiteUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']

            try:
                user = UserProfile.objects.get(username=username)
                if check_password(raw_password, user.password):
                    request.session['userprofile_id'] = user.id
                    request.session['username'] = user.username
                    request.session['email'] = user.email
                    messages.success(request, "Login successful!")
                    return redirect('home')
                else:
                    messages.error(request, "Incorrect password.")
            except UserProfile.DoesNotExist:
                messages.error(request, "User not found.")
    else:
        form = WebsiteUserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

# 🏠 Home Page
@custom_login_required
def home(request):
    return render(request, 'home.html',{'username':request.session.get('username'),'email':request.session.get('email')})


# 📤 Upload Report
@custom_login_required
def upload_report(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                report = form.save(commit=False)

                # Fetch user from session
                userprofile_id = request.session.get('userprofile_id')
                if not userprofile_id:
                    messages.error(request, "User session expired. Please login again.")
                    return redirect('login')

                userprofile = get_object_or_404(UserProfile, id=userprofile_id)
                report.user = userprofile
                report.save()  # Save early to generate file path

                # OCR & ML prediction logic
                try:
                    # text = extract_text_from_image(report.uploaded_file.path)
                    # values = extract_values(text) or {}
                    # diseases = predict_diseases(values) or {}
                    # meds = suggest_medicines(diseases) or {}
                    values = extract_report_data(report.uploaded_file.path) or {}
                    diseases = predict_diseases(values) or {}
                    meds = suggest_medicines(diseases) or {}

                    # Ensure they're JSON serializable
                    report.extracted_data = values if isinstance(values, dict) else {}
                    report.diseases_detected = diseases if isinstance(diseases, dict) else {}
                    report.medicine_suggestions = meds if isinstance(meds, dict) else {}

                except Exception as e:
                    messages.error(request, "Failed to process report: " + str(e))
                    traceback.print_exc()
                    return redirect('upload')

                report.save()  # Save again after setting prediction fields

                messages.success(request, "Your report has been uploaded successfully!")
                return redirect('report_detail', report.id)

            except Exception as e:
                messages.error(request, "An error occurred while uploading the report.")
                traceback.print_exc()

        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form,'username': request.session.get('username'),'email': request.session.get('email')
    })

@custom_login_required
def report_detail(request, report_id):
    userprofile_id = request.session.get('userprofile_id')
    userprofile = get_object_or_404(UserProfile, id=userprofile_id)
    report = get_object_or_404(Report, id=report_id, user=userprofile)
    test_units = {
    "Hemoglobin": "g/dL",
    "Glucose": "mg/dL",
    "Cholesterol": "mg/dL",
    "WBC": "/µL",
    "PLT": "/µL",
    "MCV": "fL",
    "ESR": "mm/hr",
    }
    
    return render(request, 'report_detail.html', {'report': report,'test_units': test_units,'username':request.session.get('username'),'email':request.session.get('email')})

@custom_login_required
def report_history(request):
    userprofile_id = request.session.get('userprofile_id')
    userprofile = get_object_or_404(UserProfile, id=userprofile_id)
    reports = Report.objects.filter(user=userprofile).order_by('-uploaded_at')
    return render(request, 'reports_list.html', {'reports': reports,'username':request.session.get('username'),'email':request.session.get('email')})

@custom_login_required
def delete_view(request,id):
    report = Report.objects.get(id=id)
    if request.method == 'GET':
        report.delete()
    return redirect('reports')

def generate_pdf_report(report):
    template_path = 'report_pdf_template.html'
    context = {'report': report}
    html = render_to_string(template_path, context)
    result = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    return result.getvalue()

@custom_login_required
def handle_report(request, report_id, action):
    report = Report.objects.get(id=report_id, user=request.user)
    pdf_data = generate_pdf_report(report)

    if action == "download":
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'
        return response

    elif action == "email" and request.method == "POST":
        target_email = request.POST.get("email")
        if not target_email:
            return HttpResponse("No email provided.", status=400)

        email = EmailMessage(
            subject="Your Medical Report",
            body="Please find attached your medical report.",
            to=[target_email],
        )
        email.attach(f"report_{report.id}.pdf", pdf_data, "application/pdf")
        email.send()
        return render(request, 'email_success.html', {'email': target_email}, {'username':request.session.get('username'),'email':request.session.get('email')})

    return HttpResponse("Invalid action.")

@custom_login_required
def QuestionAnswer(request):
    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        question = request.POST.get('question')

        # Save to database
        UserQuestion.objects.create(name=name, email=email, question=question)

        # Optional: Email to admin
        send_mail(
            subject=f"New Question from {name}",
            message=f"Email: {email}\n\nQuestion:\n{question}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],  # Make sure to define this in settings
            fail_silently=True,
        )

        request.session['message'] = "✅ Your question was sent successfully!"
        return redirect('Q&A')
    return render(request, 'Q&A.html', {'message': request.session.pop('message', None),'username':request.session.get('username'),'email':request.session.get('email')})

@custom_login_required
def chatbot(request):
    chat_history = request.session.get('chat_history', [])

    if request.method == "POST":
        user_message = request.POST.get("message", "")
        if user_message:
            if not gemini_model:
                return JsonResponse({"reply": "Chatbot is currently unavailable. Please try again later."})
            try:
                current_chat_history = chat_history[:] 
                current_chat_history.append({'role': 'user', 'parts': [{'text': user_message}]})
                chat = gemini_model.start_chat(history=current_chat_history)
                response = chat.send_message(user_message)
                bot_reply = response.text.strip()

                chat_history.append({'role': 'user', 'parts': [{'text': user_message}]})
                chat_history.append({'role': 'model', 'parts': [{'text': bot_reply}]})
                
                request.session['chat_history'] = chat_history
                request.session.modified = True

                return JsonResponse({"reply": bot_reply})

            except Exception as e:
                traceback.print_exc() 
                return JsonResponse({"reply": f"AI error: {str(e)}"})
    
    display_messages = []
    for msg_data in chat_history:
        text_content = ""
        if 'parts' in msg_data and msg_data['parts']:
            for part in msg_data['parts']:
                if 'text' in part:
                    text_content += part['text'] + " "
        display_messages.append({
            'sender': msg_data.get('role'),
            'text': text_content.strip()
        })
    
    return render(request, 'chatbot.html', {
        'username':request.session.get('username'),
        'email':request.session.get('email'),
        'chat_history': display_messages
    })

@custom_login_required
def clear_chat(request):
    if request.method == 'POST':
        if 'chat_history' in request.session:
            del request.session['chat_history']
            request.session.modified = True
            return JsonResponse({"status": "success", "message": "Chat history cleared."})
        return JsonResponse({"status": "info", "message": "Chat history already empty."})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)