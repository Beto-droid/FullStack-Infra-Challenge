from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Order

class OrderTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.order_url = "/orders/"
        self.order_data = {
            "customer_name": "John Doe",
            "item": "Sample Item",
            "quantity": 2,
            "status": Order.PENDING,
        }
        # Test s orders .
        Order.objects.create(customer_name="Alice", item="Item 1", quantity=1, status=Order.PENDING)
        Order.objects.create(customer_name="Bob", item="Item 2", quantity=3, status=Order.COMPLETED)
        Order.objects.create(customer_name="Charlie", item="Item 3", quantity=5, status=Order.CANCELLED)

    # def test_create_order(self):
    #     response = self.client.post(self.order_url, self.order_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Order.objects.count(), 4)  # 3 initial + 1 created
    #     self.assertEqual(Order.objects.last().customer_name, "John Doe")

    def test_create_order_missing_required_field(self):
        data = self.order_data.copy()
        data.pop("customer_name")
        response = self.client.post(self.order_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_orders_pagination(self):
        response = self.client.get(f"{self.order_url}?page=1&page_size=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["count"], 3)

        response_next_page = self.client.get(f"{self.order_url}?page=2&page_size=2")
        self.assertEqual(response_next_page.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_next_page.data["results"]), 1)

    def test_get_orders_with_filter(self):
        response = self.client.get(f"{self.order_url}?status={Order.COMPLETED}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["status"], Order.COMPLETED)

    def test_get_orders_with_invalid_filter(self):
        response = self.client.get(f"{self.order_url}?status=invalid_status")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_order_detail_view(self):
        order = Order.objects.first()
        response = self.client.get(f"{self.order_url}{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["customer_name"], order.customer_name)

    def test_order_update(self):
        order = Order.objects.first()
        data = {"customer_name": "Updated Name", "quantity": 10}
        response = self.client.put(f"{self.order_url}{order.id}/update/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.customer_name, "Updated Name")
        self.assertEqual(order.quantity, 10)

    def test_order_update_invalid_data(self):
        """
        Invalid quantity.
        :return:
        """
        order = Order.objects.first()
        data = {"quantity": -1}
        response = self.client.put(f"{self.order_url}{order.id}/update/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_delete(self):
        """
        Deletion
        :return:  2
        """
        order = Order.objects.first()
        response = self.client.delete(f"{self.order_url}{order.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_delete_nonexistent(self):
        """
        error in delete not existent Order
        :return:
        """
        response = self.client.delete(f"{self.order_url}nonexistent_id/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
