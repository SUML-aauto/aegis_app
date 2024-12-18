from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.conf import settings
from insurance.forms import InsuranceFormForm, SupportForm
from insurance.aihelper import predict_insurance_pricing
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def insurance_pricing_view(request):
    """
    View for handling insurance pricing form submissions.
    """
    if request.method == 'POST':
        form = InsuranceFormForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print('Form data:', data)
            form.save()

            current_year = datetime.now().year

            pricing = predict_insurance_pricing(data={
                'Make': data['make'],
                'Model': data['model'],
                'Engine Power (HP)': data['engine_power'],
                'Mileage (km)': data['mileage'],
                'Number of Accidents': data['vehicle_accidents'],
                'Market Value ($)': int(data['market_value']),
                'Total Owners': data['total_owners'],
                'Has Dashcam': int(data['dashcam']),
                'Vehicles in Family': data['vehicles_in_family'],
                'Driving Experience': data['driving_experience'],
                'CAR_AGE': current_year - data['year'],
                'AGE': data['age'],
                'HOMEKIDS': data['children'],
                'INCOME': int(data['income']),
            })

            params = {
                'insurance_pricing': {
                    'Liability Insurance': int(pricing['Liability Insurance']),
                    'Theft Insurance': int(pricing['Theft Insurance']),
                    'Premium Insurance': int(pricing['Premium Insurance']),
                    'Repair Insurance': int(pricing['Repair Insurance']),
                    'Premium Repair Insurance': int(pricing['Premium Repair Insurance']),
                }
            }
            return render(request, 'success.html', params)
        else:
            print('Form errors:', form.errors)  # Log errors for debugging
    else:
        form = InsuranceFormForm()  # Render an empty form for GET requests

    return render(request, 'estimation_form.html', {'form': form})


def support_form(request):
    """
    View for handling the support form and sending emails to administrators.
    """
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Compose email
            email_subject = f"Support Request from {name}"
            email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            admin_email = settings.ADMIN_EMAIL  # Define in your settings.py

            # Send email with Reply-To header
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
                reply_to=[email]  # Reply-To set to user's email
            )
            email_message.send()

            # Redirect to the success page after form submission
            return redirect('support_form_success')
    else:
        form = SupportForm()

    return render(request, 'support_form.html', {"form": form})


# Add this view function for the success page after form submission
def support_form_success(request):
    """
    View for rendering the success page after a support form is submitted.
    """
    return render(request, 'support_form_success.html')
