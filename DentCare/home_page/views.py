from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.


def home_page(request):
    return render(request,"home_page.html")

def about(request):
    return render(request,"about.html")

def treatment(request):
    return render(request,"treatment.html")

def appointment(request):
    return render (request,"appointment.html")


from django.shortcuts import render, redirect
from .models import ContactMessage


def contact(request):
    if request.method == "POST":
        username = request.POST.get('username')
        message = request.POST.get('msg')  # Note: you need to use the correct name here.

        # Create a new ContactMessage instance
        ContactMessage.objects.create(username=username, message=message)

        # Redirect after saving to prevent re-submission
        return redirect('/contact')

    return render(request, 'contact.html')  # Replace with your actual template


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def appointment_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_appointment')  
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, "user.html")





# home_page/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re

def appointment_register(request):
    errors = {}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validation
        if not username:
            errors['username'] = "Username is required."
        if not re.match(r'^\w+@\w+\.\w+$', email):
            errors['email'] = "Invalid email format."
        if not re.match(r'^\d{10}$', phone) or not phone:
            errors['phone'] = "Phone number must be 10 digits."
        if password != confirm_password:
            errors['password'] = "Passwords do not match."
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        if errors:
            return render(request, 'registration/register.html', {'errors': errors})

        # Create user if no errors
        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('appointment_login')  # Redirect to the login page
        except Exception as e:
            errors['general'] = f"An error occurred: {str(e)}"
            return render(request, 'registration/register.html', {'errors': errors})

    return render(request, 'registration/register.html')














from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Appointment, SlotAvailability

@login_required
def book_appointment(request):
    user = request.user

    if request.method == 'POST':
        appointment_date = request.POST['appointment_date']
        appointment_slot = request.POST['appointment_slot']

        # Fetch all SlotAvailability entries for the selected date and slot
        slot_availabilities = SlotAvailability.objects.filter(date=appointment_date, section=appointment_slot)

        if slot_availabilities.exists():
            # If there are multiple records, pick the first one (could be improved further based on your logic)
            slot_availability = slot_availabilities.first()

            # Check if slots are available for the selected date and section
            if slot_availability.available_slots > 0:
                # Book the appointment
                Appointment.objects.create(user=user, date=appointment_date, slot=appointment_slot)
                # Deduct a slot after booking
                slot_availability.available_slots -= 1
                slot_availability.save()

                return redirect('book_appointment')
            else:
                # No slots available for the selected section
                return render(request, 'book_appointment.html', {'error': 'No slots available for this section on the selected date'})
        else:
            # If no SlotAvailability exists for the selected date and section, create one with 20 available slots
            SlotAvailability.objects.create(date=appointment_date, section=appointment_slot, available_slots=20)
            Appointment.objects.create(user=user, date=appointment_date, slot=appointment_slot)

            return redirect(request,'book_appointment')

    # Fetch appointments of the user and available slots
    appointments = Appointment.objects.filter(user=user).order_by('-date')

    # Fetch available slots for today's date by default, or the selected date
    selected_date = request.GET.get('date', timezone.now().date())
    available_slots = SlotAvailability.objects.filter(date=selected_date)

    return render(request, 'book_appointment.html', {
        'appointments': appointments,
        'available_slots': available_slots,
        'selected_date': selected_date
    })





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

FIXED_USERNAME = 'brightsmile'
FIXED_PASSWORD = 'smileplease' 

def appointment_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == FIXED_USERNAME and password == FIXED_PASSWORD:
            request.session['is_doctor'] = True
            return redirect('dr_dashboard') 
        else:
            return HttpResponse("Invalid credentials", status=401)
    return render(request, 'doctor_login.html') 



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment 
@login_required
def dr_dashboard(request):
    appointments = Appointment.objects.all().order_by('date')
    return render(request, 'dr_dashboard.html', {'appointments': appointments})




from django.shortcuts import render, get_object_or_404, redirect
@login_required
def submit_report(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        if 'report' in request.FILES:
            report_file = request.FILES['report']
            appointment.report = report_file
        
        # Handle bill input
        if 'bill' in request.POST:
            bill_amount = request.POST['bill']
            appointment.bill = bill_amount
        
        appointment.save()
        return redirect('dr_dashboard')  # Redirect to the doctor's dashboard after submission
    
    return render(request, 'submit_report.html', {'appointment': appointment})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

@login_required
def view_my_appointments(request):
    user_id = request.user.id  # Get the current user's ID
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id, u.username,a.date
            FROM home_page_appointment a
            JOIN auth_user u ON a.user_id = u.id
            WHERE a.user_id = %s
            ORDER BY a.date DESC
        """, [user_id])
        appointments = cursor.fetchall()  # Fetch all matching records

    # Prepare the data for rendering
    appointment_list = []
    for appointment in appointments:
        appointment_list.append({
            'id': appointment[0],        # id (used for URL)
            'username': appointment[1],  # username
            'date': appointment[2],     
        })

    # Pass a flag to indicate the view is for "My Appointments"
    return render(request, 'dr_dashboard.html', {'appointments': appointment_list, 'view_my_appointments': True})






from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Appointment

@login_required
def filter_appointments(request):
    user_id = request.user.id  # Get the current user's ID
    if 'filter_date' in request.GET:
        filter_date = request.GET['filter_date']
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id, u.username, a.date, a.slot,a.report,a.bill
                FROM home_page_appointment a
                JOIN auth_user u ON a.user_id = u.id
                WHERE a.user_id = %s AND DATE(a.date) = DATE(%s)
                ORDER BY a.date DESC
            """, [user_id, filter_date])
            appointments = cursor.fetchall()  # Fetch all matching records
    else:
        # If no filter date is provided, fetch all appointments for the user
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id, u.username, a.date, a.slot,a.report,a.bill
                FROM home_page_appointment a
                JOIN auth_user u ON a.user_id = u.id
                WHERE a.user_id = %s
                ORDER BY a.date DESC
            """, [user_id])
            appointments = cursor.fetchall()  # Fetch all matching records

    # Prepare the data for rendering
    appointment_list = []
    for appointment in appointments:
        appointment_list.append({
            'id': appointment[0],        # id
            'username': appointment[1],  # username
            'date': appointment[2],      # date
            'slot': appointment[3],      # slot
            'report':appointment[4],
            'bill':appointment[5]
        })

    return render(request, 'dr_dashboard.html', {'appointments': appointment_list})











from django.http import JsonResponse
from .models import SlotAvailability

def fetch_slots(request):
    selected_date = request.GET.get('date')
    
    # Ensure date is passed
    if not selected_date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    # Query the database to get available slots for the selected date
    slots = SlotAvailability.objects.filter(date=selected_date)

    # Check if there are any slots for that date
    if not slots.exists():
        return JsonResponse({'slots': []})  # No slots available for the date

    # Prepare the data to be sent back to the frontend
    slots_data = []
    for slot in slots:
        slots_data.append({
            'section': slot.section,
            'available_slots': slot.available_slots
        })

    return JsonResponse({'slots': slots_data})
