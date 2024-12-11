from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.conf import settings
from insurance.forms import InsuranceFormForm, SupportForm
from insurance.aihelper import predict_insurance_claim

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

            may_have_claim = predict_insurance_claim(data={
                'Make': data['make'],
                'Fuel Type': data['fuel_type'],
                'Engine Power (HP)': data['engine_power'],
                'Driving Experience': data['driving_experience'],
                'INCOME': int(data['income']),
                'GENDER': 'M' if data['gender'] == 'male' else 'F',
                'CAR_TYPE': data['body_type']
            })
            return render(request, 'success.html', {'may_have_claim': may_have_claim})  # Redirect to success page
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
