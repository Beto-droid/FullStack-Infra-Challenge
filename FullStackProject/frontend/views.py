import requests
from django.http import JsonResponse
from django.shortcuts import render


def parse_form_data_to_json(data_str):
    import urllib.parse
    import json
    """
    Converts form-encoded data to JSON.

    Args:
        data_str (str): The form-encoded data as a string (e.g., from request.body).

    Returns:
        dict: A dictionary containing the parsed and cleaned data.
    """
    # Decode and parse the form data
    data_str = data_str.decode('utf-8')
    data_decoded = urllib.parse.parse_qs(data_str)

    # Clean up the data by extracting the first value from each list
    data = {key: value[0] for key, value in data_decoded.items()}

    return data


def order_list(request):
    page = request.GET.get('page', 1)
    page_size = request.htmx.request.GET.get('page_size', 5)
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

def update_order(request, id):
    if request.method == "PUT":
        api_url = f"http://127.0.0.1:8000/orders/{id}/update/"
        data_decoded = parse_form_data_to_json(request.htmx.request.body)
        response = requests.put(api_url, json=data_decoded)

        if response.status_code == 200:
            order = response.json()
            return render(request, 'frontend/order_table_row_updated.html', {'order': order})
        return JsonResponse({"error": "Failed to update order"}, status=400)

def edit_order_row(request, id):
    # Fetch the specific order data
    api_url = f"http://127.0.0.1:8000/orders/{id}/"
    response = requests.get(api_url)

    if response.status_code == 200:
        order = response.json()
        return render(request, 'frontend/order_row_edit.html', {'order': order})
    return JsonResponse({"error": "Failed to load order data"}, status=400)

def delete_order(request, id):
    if request.method == "DELETE":
        api_url = f"http://127.0.0.1:8000/orders/{id}/"
        save_data = requests.get(api_url).json()
        api_url = f"http://127.0.0.1:8000/orders/{id}/delete/"
        response = requests.delete(api_url)

        if response.status_code == 204:
            return render(request, 'frontend/order_table_row_deleted.html', {'row_data': save_data})
        else:
            return JsonResponse({"error": "Failed to delete order"}, status=400)

def create_order(request):
    if request.method == "POST":
        api_url = "http://127.0.0.1:8000/orders/"
        data = request.POST
        response = requests.post(api_url, json=data)

        if response.status_code == 201:
            new_order = response.json()
            return render(request, 'frontend/order_table_row_created.html', {'order': new_order})
        else:
            return JsonResponse({"error": "Failed to create order"}, status=400)