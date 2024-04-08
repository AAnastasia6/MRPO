from dataclasses import dataclass
import xml.etree.ElementTree as ET
import os
import xml.dom.minidom as minidom

# Класс Клиент (имя, адрес, номер телефона)
@dataclass
class Client:
    client_id: int
    full_name: str
    address: str
    phone: str

# Класс Администратор (имя, номер телефона, филиал в котором работает админ, время работы)
@dataclass
class Administrator:
    administrator_id: int
    full_name: str
    phone: str
    branch_id: int
    time_job: str

# Класс Филиал (адрес)
@dataclass(frozen=True)
class Branch:
    branch_id: int
    address: str

# Класс Товар (наименование, цена, количество в наличии)
@dataclass
class Product:
    product_id: int
    name: str
    price: float
    count: int

# Класс Покупка (дата покупки, количество купленного товара, id клиента-покупателя, id филиала-места выдачи)
@dataclass(frozen=True)
class Purchase:
    purchase_id: int
    date: str
    quantity: int
    client_id: int
    product_id: int
    branch_id: int

# Класс Поставщик (наименование)
@dataclass(frozen=True)
class Provider:
    provider_id: int
    name: str

#Создание файла

file_path = 'data.xml'

if not os.path.exists(file_path):
    # Создание структуры XML файла, если он не существует
    root = ET.Element('data')

    clients = ET.SubElement(root, 'clients')
    administrators = ET.SubElement(root, 'administrators')
    branches = ET.SubElement(root, 'branches')
    products = ET.SubElement(root, 'products')
    purchases = ET.SubElement(root, 'purchases')
    providers = ET.SubElement(root, 'providers')


    masters = ET.SubElement(root, 'masters')
    services = ET.SubElement(root, 'services')
    promotions = ET.SubElement(root, 'promotions')
    reviews = ET.SubElement(root, 'reviews')
    sessions = ET.SubElement(root, 'sessions')


    tree = ET.ElementTree(root)
    tree.write(file_path)
    print("Файл 'data.xml' успешно создан.")
else:
    print("Файл 'data.xml' уже существует.")


# Загрузка данных из XML файла
tree = ET.parse('data.xml')
root = tree.getroot()


class PurchaseServise:
    @staticmethod
    def check_purchase(quantity, product_id):
        chosen_product = next((product for product in products if product.product_id == product_id), None)

        if not chosen_product:
            print("Выбранный товар не существует.")
            return False

        if quantity > chosen_product.count:
            print("Недостаточное количество товара.")
            return False


        chosen_product.count -= quantity
        print(f"Покупка товара {chosen_product.name} успешно оформлена. Остаток: {chosen_product.count}")
        return True


class SupplyServise:
    @staticmethod
    def check_supply(product_id, counts_provide, provider_id):
        chosen_provider = next((provider for provider in providers if provider.provider_id == provider_id), None)

        if not chosen_provider:
            print("Выбранный поставщик не существует.")
            return False

        chosen_product = next((product for product in products if product.product_id == product_id), None)

        if not chosen_product:
            print("Выбранный товар не найден.")
            return False

        chosen_product.count += counts_provide
        print(
            f"Поставка товара {chosen_product.name} от поставщика {chosen_provider.name}. Обновленное количество: {chosen_product.count}")
        return True


class XMLRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = ET.parse(file_path)
        self.root = self.data.getroot()

    def add_administrator(self, administrator):

        administrators = self.root.find('administrators')

        new_administrator = ET.SubElement(administrators, 'administrator')
        ET.SubElement(new_administrator, 'administrator_id').text = str(administrator.administrator_id)
        ET.SubElement(new_administrator, 'full_name').text = administrator.full_name
        ET.SubElement(new_administrator, 'phone').text = administrator.phone
        ET.SubElement(new_administrator, 'branch_id').text = str(administrator.branch_id)
        ET.SubElement(new_administrator, 'time_job').text = administrator.time_job

        self.indent(self.data.getroot())
        self.data.write(self.file_path)

        print("Администратор успешно добавлен.")

    def get_administrators(self):
        administrators = []
        for administrator_elem in self.root.findall('administrators/administrator'):
            administrator = Administrator(
                int(administrator_elem.find('administrator_id').text),
                administrator_elem.find('full_name').text,
                administrator_elem.find('phone').text,
                int(administrator_elem.find('branch_id').text),
                administrator_elem.find('time_job').text
            )
            administrators.append(administrator)
        return administrators

    def add_client(self, client):
        clients = self.root.find('clients')

        new_client = ET.SubElement(clients, 'client')
        ET.SubElement(new_client, 'client_id').text = str(client.client_id)
        ET.SubElement(new_client, 'full_name').text = client.full_name
        ET.SubElement(new_client, 'address').text = client.address
        ET.SubElement(new_client, 'phone').text = client.phone

        self.indent(self.data.getroot())
        self.data.write(self.file_path)

        print("Клиент успешно добавлен.")

    def get_clients(self):
        clients = []
        for client_elem in self.root.findall('clients/client'):
            client = Client(
                int(client_elem.find('client_id').text),
                client_elem.find('full_name').text,
                client_elem.find('address').text,
                client_elem.find('phone').text
            )
            clients.append(client)
        return clients

    def add_product(self, product):
        products = self.root.find('products')

        new_product = ET.SubElement(products, 'product')
        ET.SubElement(new_product, 'product_id').text = str(product.product_id)
        ET.SubElement(new_product, 'name').text = product.name
        ET.SubElement(new_product, 'price').text = str(product.price)
        ET.SubElement(new_product, 'count').text = str(product.count)

        self.indent(self.data.getroot())
        self.data.write(self.file_path)

        print("Продукт успешно добавлен.")

    def get_products(self):
        products = []
        for product_elem in self.root.findall('products/product'):
            product = Product(
                int(product_elem.find('product_id').text),
                product_elem.find('name').text,
                float(product_elem.find('price').text),
                int(product_elem.find('count').text)
            )
            products.append(product)
        return products

    def add_product_count(self, product_id, counts_provider, provider_id):
        SupplyServise.check_supply(product_id=product_id, counts_provide=counts_provider, provider_id=provider_id)
        print("Поставка успешно добавлена.")

    def add_branch(self, branch):
        branches = self.root.find('branches')

        new_branch = ET.SubElement(branches, 'branch')
        ET.SubElement(new_branch, 'branch_id').text = str(branch.branch_id)
        ET.SubElement(new_branch, 'address').text = branch.address

        self.indent(self.data.getroot())
        self.data.write(self.file_path)

        print("Филиал успешно добавлен.")

    def get_branches(self):
        branches = []
        for branch_elem in self.root.findall('branches/branch'):
            branch = Branch(
                int(branch_elem.find('branch_id').text),
                branch_elem.find('address').text
            )
            branches.append(branch)
        return branches

    def add_purchase(self, purchase):
        if (PurchaseServise.check_purchase(quantity=purchase.quantity, product_id=purchase.product_id)):
            purchases = self.root.find('purchases')

            new_purchase = ET.SubElement(purchases, 'purchase')
            ET.SubElement(new_purchase, 'purchase_id').text = str(purchase.purchase_id)
            ET.SubElement(new_purchase, 'date').text = purchase.date
            ET.SubElement(new_purchase, 'quantity').text = str(purchase.quantity)
            ET.SubElement(new_purchase, 'client_id').text = str(purchase.client_id)
            ET.SubElement(new_purchase, 'product_id').text = str(purchase.product_id)
            ET.SubElement(new_purchase, 'branch_id').text = str(purchase.branch_id)

            self.indent(self.data.getroot())
            self.data.write(self.file_path)

            print("Сделка успешно добавлена.")
        else:
            print("Ошибка ввода данных")

    def get_purchases(self):
        purchases = []
        for purchase_elem in self.root.findall('purchases/purchase'):
            purchase = Purchase(
                int(purchase_elem.find('purchase_id').text),
                purchase_elem.find('date').text,
                int(purchase_elem.find('quantity').text),
                int(purchase_elem.find('client_id').text),
                int(purchase_elem.find('product_id').text),
                int(purchase_elem.find('branch_id').text),
            )
            purchases.append(purchase)
        return purchases

    def add_provider(self, provider):
        providers = self.root.find('providers')

        new_provider = ET.SubElement(providers, 'provider')
        ET.SubElement(new_provider, 'provider_id').text = str(provider.provider_id)
        ET.SubElement(new_provider, 'name').text = provider.name

        self.indent(self.data.getroot())
        self.data.write(self.file_path)

        print("Филиал успешно добавлен.")

    def get_providers(self):
        providers = []
        for provider_elem in self.root.findall('providers/provider'):
            provider = Provider(
                int(provider_elem.find('provider_id').text),
                provider_elem.find('name').text
            )
            providers.append(provider)
        return providers

    def indent(self, elem, level=0):
        indent = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self.indent(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent


# Инициализация репозитория
repository = XMLRepository('data.xml')

# Пример добавления клиента и чтения из репозитория
client = Client(client_id=1, full_name="Иванов Иван", address="ул. Пушкина, д.1", phone="123-456-789")
repository.add_client(client)

# Чтение всех клиентов из репозитория
clients = repository.get_clients()
for client in clients:
    print(client)

branch = Branch(branch_id=1, address="ул. Ленина, 5")
repository.add_branch(branch)

branches = repository.get_branches()
for branch in branches:
    print(branch)

administrator = Administrator(administrator_id=1, full_name="Иванов Иван", phone="123-456-789", branch_id=1, time_job="9-16")
repository.add_administrator(administrator)

administrators = repository.get_administrators()
for administrator in administrators:
    print(administrator)

product = Product(product_id=1, name="Шампунь", price=200, count=100)
repository.add_product(product)

products = repository.get_products()
for product in products:
    print(product)

purchase = Purchase(purchase_id=1, date="12-07-2024", quantity=50, client_id=100, product_id=1, branch_id=1)
repository.add_purchase(purchase)

purchases = repository.get_purchases()
for purchase in purchases:
    print(purchase)

provider = Provider(provider_id=1, name="ООО Петров ")
repository.add_provider(provider)

providers = repository.get_providers()
for provider in providers:
    print(provider)

repository.add_product_count(1, 100, 1)
for product in products:
    print(product)