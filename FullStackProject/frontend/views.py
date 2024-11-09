import requests
from django.shortcuts import render


def order_list(request):
    page = request.GET.get('page', 1)
    page_size = request.htmx.request.GET.get('page_size', 3)
    filtering_status = request.htmx.request.GET.get('status', 'all')
    api_url = f"http://127.0.0.1:8000/orders/?page={page}&page_size={page_size}&status={filtering_status}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        orders = data['results']
        page_number = int(page)

        if request.headers.get('HX-Request'):
            return render(request, 'frontend/order_table.html', {
                'orders': orders,
                'next_page': data['next'],
                'prev_page': data['previous'],
                'page_number': page_number,
                'page_size': page_size,
                'filtering_status': filtering_status,
            })

        return render(request, 'frontend/frontend_main.html', {
            'orders': orders,
            'next_page': data['next'],
            'prev_page': data['previous'],
            'page_number': page_number,
            'page_size': page_size,
            'filtering_status': filtering_status,
        })
    else:
        return render(request, 'frontend/frontend_main.html', {'error': 'Failed to load orders'})