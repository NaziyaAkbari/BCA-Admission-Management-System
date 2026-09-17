from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile, AdmissionApplication
from .forms import StudentRegistrationForm, ProfileUpdateForm, AdmissionApplicationForm
from django.db.models import Q
import random
import string


def generate_application_number():
    return 'BCA' + ''.join(random.choices(string.digits, k=8))


# ── Home ──
def home(request):
    return render(request, 'admission/home.html')


# ── Register ──
def register_view(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'admission/register.html', {'form': form})


# ── Student Login ──
def login_view(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('dashboard')
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                messages.error(
                    request,
                    'This is an admin account. Please use the Admin Login page.'
                )
            else:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admission/login.html')


# ── Student Logout ──
def logout_view(request):
    logout(request)
    return redirect('login')


# ── Admin Login ──
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'admission/admin_login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_panel')
            else:
                messages.error(
                    request,
                    'Access Denied. This is a student account, not an admin account.'
                )
        else:
            messages.error(request, 'Invalid admin credentials. Please try again.')
    return render(request, 'admission/admin_login.html')


# ── Admin Logout ──
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')


# ── Student Dashboard ──
@login_required(login_url='/login/')
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    applications = AdmissionApplication.objects.filter(
        student=request.user
    ).order_by('-applied_on')
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'admission/dashboard.html', {
        'applications': applications,
        'profile': profile,
    })


# ── Profile ──
@login_required(login_url='/login/')
def profile_view(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = request.POST.get(
                'first_name', request.user.first_name)
            request.user.last_name = request.POST.get(
                'last_name', request.user.last_name)
            request.user.email = request.POST.get(
                'email', request.user.email)
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'admission/profile.html', {
        'form': form, 'profile': profile
    })


# ── Apply ──
@login_required(login_url='/login/')
def apply_admission(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    existing = AdmissionApplication.objects.filter(
        student=request.user).first()
    if existing:
        messages.info(
            request,
            f'You already applied. App No: {existing.application_number}'
        )
        return redirect('dashboard')
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.student = request.user
            app.application_number = generate_application_number()
            app.save()
            messages.success(
                request,
                f'Application submitted! Number: {app.application_number}'
            )
            return redirect('dashboard')
    else:
        form = AdmissionApplicationForm(initial={
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
        })
    return render(request, 'admission/apply.html', {'form': form})


# ── Application Detail ──
@login_required(login_url='/login/')
def application_detail(request, pk):
    if request.user.is_staff:
        return redirect('admin_panel')
    app = get_object_or_404(
        AdmissionApplication, pk=pk, student=request.user)
    return render(request, 'admission/application_detail.html', {'app': app})


# ── Admin Panel ──
def admin_panel(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_staff:
        return redirect('dashboard')

    query         = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    sort          = request.GET.get('sort', '-applied_on')

    allowed_sorts = [
        '-applied_on', 'applied_on',
        'full_name', '-full_name',
        '-twelfth_percentage', 'twelfth_percentage',
    ]
    if sort not in allowed_sorts:
        sort = '-applied_on'

    apps = AdmissionApplication.objects.all()
    if query:
        apps = apps.filter(
            Q(full_name__icontains=query) |
            Q(application_number__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    if status_filter:
        apps = apps.filter(status=status_filter)
    apps = apps.order_by(sort)

    all_apps = AdmissionApplication.objects.all()
    return render(request, 'admission/admin_panel.html', {
        'applications':   apps,
        'query':          query,
        'status_filter':  status_filter,
        'sort':           sort,
        'total_count':    all_apps.count(),
        'pending_count':  all_apps.filter(status='Pending').count(),
        'approved_count': all_apps.filter(status='Approved').count(),
        'rejected_count': all_apps.filter(status='Rejected').count(),
        'review_count':   all_apps.filter(status='Under Review').count(),
    })


# ── Update Status — THIS IS THE FIXED ONE ──
def update_status(request, pk):
    # Must be logged in as admin
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    app = get_object_or_404(AdmissionApplication, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()
        remarks    = request.POST.get('remarks', '').strip()

        allowed = ['Pending', 'Under Review', 'Approved', 'Rejected']

        if new_status not in allowed:
            messages.error(request, f'Invalid status: "{new_status}".')
            return redirect('admin_panel')

        # Save to database
        app.status  = new_status
        app.remarks = remarks
        app.save()

        messages.success(
            request,
            f'Application {app.application_number} has been '
            f'updated to "{new_status}" successfully.'
        )
        return redirect('admin_panel')

    # If GET request, just redirect back
    return redirect('admin_panel')