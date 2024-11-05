from django.shortcuts import render


def contact_info_view(request):
    company_info = {
        'name': 'AegisAuto',
        'email': 'contact_aegis@gmail.com',
        'phone': '+48-98-567-657',
        'address': 'ul. Kwiatowa 29 , Warsaw, Poland'
    }

    return render(request, 'contact_info.html', {'company': company_info})
