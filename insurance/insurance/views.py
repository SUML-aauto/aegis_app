from django.shortcuts import redirect

from django.shortcuts import render

from insurance.forms import InsuranceFormForm


def index(request):
    return render(request, 'index.html')


def insurance_pricing_view(request):
    if request.method == 'POST':
        form = InsuranceFormForm(request.POST)
        if form.is_valid():
            print('Form data:', form.cleaned_data)
            form.save()
            return redirect('success')
        else:
            print('From errors ', form.errors)
    else:
        form = InsuranceFormForm()

    return render(request, 'estimation_form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')
