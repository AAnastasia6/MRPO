from dataclasses import dataclass
import xml.etree.ElementTree as ET
import os
import xml.dom.minidom as minidom

# Класс Клиент (имя, адрес, номер телефона)
@dataclass
class Client:
    full_name: str
    address: str
    phone: str


# Класс Филиал (адрес)
@dataclass(frozen=True)
class Branch:
    address: str

# Класс Товар (наименование, цена, количество в наличии)
@dataclass
class Product:
    name: str
    price: float
    count: int

# Класс Покупка (дата покупки, количество купленного товара, id клиента-покупателя, id филиала-места выдачи)
@dataclass(frozen=True)
class Purchase:
    date: str
    quantity: int
    client_id: int
    product_id: int
    branch_id: int


# Класс Поставщик (наименование)
@dataclass(frozen=True)
class Provider:
    name: str

#Создание файла

file_path = 'data.xml'

if not os.path.exists(file_path):
    # Создание структуры XML файла, если он не существует
    root = ET.Element('data')

    clients = ET.SubElement(root, 'clients')
    administrators = ET.SubElement(root, 'administrators')
    branchs = ET.SubElement(root, 'branchs')
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
    def check_purchase(purchase, product, product_count_available, branch):

        if product is None:
            print('Выбранный товар не существует')
            return False

        if branch is None:
            print('Выбранный филиал недоступен')
            return False

        if purchase.quantity > int(product_count_available):
            print("Товара недостаточно на складе")
            return False

        return True


class SupplyServise:
    @staticmethod
    def check_supply(product, provider):
        if product is None:
            print('Выбранный товар не существует')
            return False

        if provider is None:
            print('Выбранный поставщик не существует')
            return False
        return True


class ServiceLayer:
    @staticmethod
    def add_object(objectt):
        if isinstance(objectt, Client):
            id=repository.get_id_new('client')
            repository.add_entity(objectt, 'client', id)

        if isinstance(objectt, Branch):
            id=repository.get_id_new('branch')
            repository.add_entity(objectt, 'branch', id)

        if isinstance(objectt, Product):
            id=repository.get_id_new('product')
            repository.add_entity(objectt, 'product', id)

        if isinstance(objectt, Provider):
            id=repository.get_id_new('provider')
            repository.add_entity(objectt, 'provider', id)

        if isinstance(objectt, Purchase):
            id=repository.get_id_new('purchase')
            product = repository.get_entiti_by_id('product', objectt.product_id)
            product_count_available = repository.get_product_count(objectt.product_id)
            branch = repository.get_entiti_by_id('branch', objectt.branch_id)
            if PurchaseServise.check_purchase(objectt, product, product_count_available, branch):
                repository.add_entity(objectt, 'purchase', id)
                repository.update_product_count(objectt.product_id, objectt.quantity, '-')


    @staticmethod
    def remove_object(object_name, id):
        repository.remove_entity(object_name, id)

    @staticmethod
    def get_all_object(object_name):
        print(repository.get_all_entities(object_name))

    @staticmethod
    def order_a_product(product_id, provider_id, count):
        product = repository.get_entiti_by_id('product', product_id)
        provider = repository.get_entiti_by_id('provider', provider_id)
        if SupplyServise.check_supply(product, provider):
            repository.update_product_count(product_id, count, '+')


class XMLRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = ET.parse(file_path)
        self.root = self.data.getroot()

    def get_id_new(self, entity_name):
        # Нахождение максимального id для элементов
        max_id = 0
        for entiti in self.root.findall(f'.//{entity_name}'):
            entiti_id = int(entiti.attrib.get('id', 0))
            max_id = max(max_id, entiti_id)

        print(f"Максимальный id для элементов: {max_id}")
        return max_id+1

    def add_entity(self, entity, entity_type, id):
        parent_element = self.root.find(entity_type + "s")

        new_entity = ET.SubElement(parent_element, entity_type)
        new_entity.set('id', str(id))

        for prop, value in vars(entity).items():
            if not prop.startswith("_"):
                ET.SubElement(new_entity, prop).text = str(value)

        self.indent(self.data.getroot())  # Форматирование XML
        self.data.write(self.file_path)  # Сохранение изменений в файл

        print(f"{entity_type.capitalize()} успешно добавлен.")

    def remove_entity(self, entity_type, id):
        parent_element = self.root.find(entity_type + "s")

        for element in parent_element.findall(entity_type):
            if element.get("id") == str(id):
                parent_element.remove(element)
                self.indent(self.data.getroot())
                self.data.write(self.file_path)
                print(f"{entity_type.capitalize()} с id {id} успешно удален.")
                return

        print(f"{entity_type.capitalize()} с id {id} не найден.")

    def get_entiti_by_id(self, entiti_name, id):
        for entiti in root.findall(f'.//{entiti_name}'):
            if entiti.attrib.get('id') == str(id):
                return entiti

    def get_product_count(self, product_id):
        product_element = self.root.find("products")
        for product in product_element.findall("product"):
            if product.get('id') == str(product_id):
                count_element = product.find('count')
                return count_element.text



    def get_all_entities(self, entity_type):
        parent_element = self.root.find(entity_type + "s")
        entities = []

        for element in parent_element.findall(entity_type):
            entity_data = {}
            entity_data["id"] = element.get("id")
            for child in element:
                entity_data[child.tag] = child.text
            entities.append(entity_data)

        return entities

    def update_product_count(self, product_id, count_diff, operation):
        product_element = self.root.find("products")
        for product in product_element.findall("product"):
            if product.get('id') == str(product_id):
                if operation == '+':
                    count_element = product.find('count')
                    new_count = int(count_element.text) + count_diff
                    count_element.text = str(new_count)
                elif operation == '-':
                    count_element = product.find('count')
                    new_count = int(count_element.text) - count_diff
                    count_element.text = str(new_count)

                self.indent(self.data.getroot())
                self.data.write(self.file_path)
                print(f"Данные успешно обновлены")
                return


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


# branch = Branch(address="Lepino, 25")
# ServiceLayer.add_object(branch)

# client = Client(full_name="Ivanov Ivan", address="Mira, 28", phone="123-456-789")
# ServiceLayer.add_object(client)

# product = Product(name="Shampoo", price=200, count=0)
# ServiceLayer.add_object(product)


# provider = Provider(name="OOO Petrov ")
# ServiceLayer.add_object(provider)

purchase = Purchase(date="12-07-2024", quantity=5, client_id=1, product_id=1, branch_id=1)
ServiceLayer.add_object(purchase)

# ServiceLayer.order_a_product(1, 1, 20)
