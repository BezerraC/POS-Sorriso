import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Products, Sales, salesItems


class posAppTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_user(self):
        # Test the login view
        response = self.client.post(reverse('login-user'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

    def test_home_view(self):
        # Log in before accessing the home page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')

    def test_category_view(self):
        # Log in before accessing the categories page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('category-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lista de Categorias')

    def test_save_category(self):
        # Log in before saving a category
        self.client.login(username='testuser', password='testpassword')

        # Create a dummy category
        category_data = {'name': 'Test Category', 'description': 'Test Description', 'status': 1, 'id': ''}
        response = self.client.post(reverse('save-category-page'), category_data)
        
        self.assertEqual(response.status_code, 200)
        #print(f"Response content: {response.content.decode('utf-8')}") 
        self.assertEqual(json.loads(response.content)['status'], 'success')

        # Check if the category was actually saved in the database
        saved_category = Category.objects.get(name='Test Category')
        self.assertEqual(saved_category.description, 'Test Description')
        self.assertEqual(saved_category.status, 1)

    def test_delete_category(self):
        # Log in before deleting a category
        self.client.login(username='testuser', password='testpassword')

        # Create a dummy category for deletion
        category_to_delete = Category.objects.create(name='Category to Delete', description='Test Description', status=1, id=1)

        response = self.client.post(reverse('delete-category'), {'id': category_to_delete.id})
        
        self.assertEqual(response.status_code, 200)
        #print(f"Response content: {response.content.decode('utf-8')}") 
        self.assertEqual(json.loads(response.content)['status'], 'success')

        # Check if the category was actually deleted from the database
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=category_to_delete.id)

    def test_products_view(self):
        # Log in before accessing the product page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('product-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lista de Produtos')

    def test_save_product(self):
        # Log in before saving a product
        self.client.login(username='testuser', password='testpassword')

        # Create a dummy category
        category = Category.objects.create(name='Test Category', description='Test Description', status=1)

        # Create a fictitious product
        product_data = {'id': '', 'code': '696969', 'category_id': category.id, 'name': 'Test Product', 'description': 'Test Description', 'price': '9.99', 'status': 1}
        response = self.client.post(reverse('save-product-page'), product_data)

        self.assertEqual(response.status_code, 200)
        #print(f"Response content: {response.content.decode('utf-8')}") 
        self.assertEqual(json.loads(response.content)['status'], 'success')

        # Check if the product was actually saved in the database
        saved_product = Products.objects.get(name='Test Product')
        self.assertEqual(saved_product.category_id, category)
        self.assertEqual(saved_product.price, 9.99)

    def test_pos_view(self):
        # Log in before accessing the point of sale page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('pos-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ponto de Venda')

    def test_salesList_view(self):
        # Log in before accessing the sales transaction page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('sales-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transações de Vendas')

    def test_receipt_view(self):
        # Log in before accessing the receipts page
        self.client.login(username='testuser', password='testpassword')

        # Criar uma venda fictícia
        sale = Sales.objects.create(code='12345', sub_total=9.99, grand_total=9.99, tax_amount=1.00, tax=0.10, tendered_amount=10.99, amount_change=1.00)

        response = self.client.get(reverse('receipt-modal') + f'?id={sale.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recibo')
