"""
ტესტური მონაცემების შესაქმნელი სკრიპტი
გაშვება: python populate_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_store.settings')
django.setup()

from products.models import Category, Product
from users.models import CustomUser


def create_categories():
    """კატეგორიების შექმნა"""
    categories_data = [
        {'name': 'სკამი', 'slug': 'skami', 'description': 'სხვადასხვა ტიპის სკამები ოფისისთვის და სახლისთვის'},
        {'name': 'დივანი', 'slug': 'divani', 'description': 'კომფორტული დივნები თქვენი სახლისთვის'},
        {'name': 'მაგიდა', 'slug': 'magida', 'description': 'სამუშაო და ჭამის მაგიდები'},
        {'name': 'კარადა', 'slug': 'karada', 'description': 'ტანსაცმლის კარადები'},
        {'name': 'საწოლი', 'slug': 'sawoli', 'description': 'კომფორტული საწოლები'},
        {'name': 'ტუმბო', 'slug': 'tumbo', 'description': 'ტუმბოები და ღამის მაგიდები'},
        {'name': 'თარო', 'slug': 'taro', 'description': 'წიგნის თაროები და სათავსოები'},
        {'name': 'სავარძელი', 'slug': 'savardzeli', 'description': 'კომფორტული სავარძლები'},
        {'name': 'ეზოს ავეჯი', 'slug': 'ezos-aveji', 'description': 'ბაღისა და ეზოს ავეჯი'},
    ]

    print("კატეგორიების შექმნა...")
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'is_active': True
            }
        )
        categories.append(category)
        if created:
            print(f"✓ შეიქმნა: {category.name}")
        else:
            print(f"○ უკვე არსებობს: {category.name}")

    return categories


def create_products(categories):
    """პროდუქტების შექმნა"""
    products_data = [
        # სკამები
        {'name': 'ოფისის სკამი ERGO', 'category': 'skami', 'price': 299.99, 'stock': 15, 'color': 'black',
         'material': 'textile',
         'description': 'ერგონომიული ოფისის სკამი რეგულირებადი სიმაღლით და მხარების მხარდაჭერით'},
        {'name': 'სკამი MODERN', 'category': 'skami', 'price': 89.99, 'stock': 25, 'color': 'white',
         'material': 'plastic', 'description': 'თანამედროვე დიზაინის სკამი სამზარეულოსთვის'},
        {'name': 'ბარის სკამი HIGH', 'category': 'skami', 'price': 149.99, 'stock': 12, 'color': 'brown',
         'material': 'wood', 'description': 'მაღალი ბარის სკამი ხის ფეხებით'},

        # დივნები
        {'name': 'დივანი COMFORT', 'category': 'divani', 'price': 1299.99, 'stock': 5, 'color': 'gray',
         'material': 'textile', 'description': 'კომფორტული სამადგილიანი დივანი მისაძინებელი მექანიზმით'},
        {'name': 'დივანი LUXURY', 'category': 'divani', 'price': 2499.99, 'stock': 3, 'color': 'brown',
         'material': 'leather', 'description': 'ტყავის ფუფუნებული დივანი პრემიუმ კლასის'},
        {'name': 'კუთხის დივანი CORNER', 'category': 'divani', 'price': 1899.99, 'stock': 4, 'color': 'beige',
         'material': 'textile', 'description': 'დიდი კუთხის დივანი საძინებელი ადგილით'},

        # მაგიდები
        {'name': 'მაგიდა OFFICE', 'category': 'magida', 'price': 399.99, 'stock': 10, 'color': 'brown',
         'material': 'wood', 'description': 'სამუშაო მაგიდა უჯრებით და კაბინეტით'},
        {'name': 'მაგიდა GLASS', 'category': 'magida', 'price': 599.99, 'stock': 7, 'color': 'white',
         'material': 'glass', 'description': 'მინის მაგიდა ქრომირებული ფეხებით'},
        {'name': 'საჭმლის მაგიდა DINING', 'category': 'magida', 'price': 749.99, 'stock': 8, 'color': 'brown',
         'material': 'wood', 'description': 'საჭმლის მაგიდა 6 ადგილზე'},

        # კარადები
        {'name': 'კარადა WARDROBE XL', 'category': 'karada', 'price': 899.99, 'stock': 8, 'color': 'white',
         'material': 'wood', 'description': 'დიდი კარადა სარკით და თაროებით'},
        {'name': 'კარადა MODERN', 'category': 'karada', 'price': 699.99, 'stock': 6, 'color': 'gray',
         'material': 'wood', 'description': 'თანამედროვე კარადა გადასაადგილებელი კარებით'},

        # საწოლები
        {'name': 'საწოლი KING SIZE', 'category': 'sawoli', 'price': 1499.99, 'stock': 4, 'color': 'brown',
         'material': 'wood', 'description': 'კინგ ზომის საწოლი მატრასის ყუთით'},
        {'name': 'საწოლი QUEEN', 'category': 'sawoli', 'price': 999.99, 'stock': 6, 'color': 'white',
         'material': 'wood', 'description': 'ქუინ ზომის საწოლი თაფლისფერი ხის'},
        {'name': 'ბავშვის საწოლი KIDS', 'category': 'sawoli', 'price': 549.99, 'stock': 10, 'color': 'blue',
         'material': 'wood', 'description': 'უსაფრთხო ბავშვის საწოლი'},

        # ტუმბოები
        {'name': 'ტუმბო NIGHT', 'category': 'tumbo', 'price': 199.99, 'stock': 12, 'color': 'brown', 'material': 'wood',
         'description': 'ღამის ტუმბო ორი უჯრით'},
        {'name': 'ტუმბო TV', 'category': 'tumbo', 'price': 349.99, 'stock': 8, 'color': 'white', 'material': 'wood',
         'description': 'ტელევიზორის ტუმბო კაბინეტებით'},

        # თაროები
        {'name': 'თარო BOOKSHELF', 'category': 'taro', 'price': 299.99, 'stock': 9, 'color': 'brown',
         'material': 'wood', 'description': 'წიგნის თარო 5 დონით'},
        {'name': 'კედლის თარო WALL', 'category': 'taro', 'price': 129.99, 'stock': 15, 'color': 'white',
         'material': 'wood', 'description': 'მოდულური კედლის თარო'},

        # სავარძლები
        {'name': 'სავარძელი RELAX', 'category': 'savardzeli', 'price': 799.99, 'stock': 5, 'color': 'beige',
         'material': 'textile', 'description': 'მოსვენების სავარძელი ფეხსაყრდენით'},
        {'name': 'სავარძელი ROCK', 'category': 'savardzeli', 'price': 449.99, 'stock': 7, 'color': 'gray',
         'material': 'textile', 'description': 'საქანელა სავარძელი'},

        # ეზოს ავეჯი
        {'name': 'ბაღის სკამი GARDEN', 'category': 'ezos-aveji', 'price': 199.99, 'stock': 20, 'color': 'green',
         'material': 'plastic', 'description': 'ამინდგამძლე ბაღის სკამი'},
        {'name': 'ეზოს კომპლექტი PATIO', 'category': 'ezos-aveji', 'price': 1299.99, 'stock': 6, 'color': 'brown',
         'material': 'wood', 'description': 'ეზოს სამადგილიანი კომპლექტი მაგიდით'},
    ]

    print("\nპროდუქტების შექმნა...")
    # კატეგორიების dict-ის შექმნა
    categories_dict = {cat.slug: cat for cat in categories}

    created_count = 0
    for prod_data in products_data:
        category = categories_dict.get(prod_data['category'])
        if not category:
            continue

        slug = prod_data['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')

        product, created = Product.objects.get_or_create(
            slug=slug,
            defaults={
                'name': prod_data['name'],
                'category': category,
                'description': prod_data['description'],
                'price': prod_data['price'],
                'stock': prod_data['stock'],
                'color': prod_data['color'],
                'material': prod_data['material'],
                'is_available': True,
                'featured': created_count < 5  # პირველი 5 იქნება featured
            }
        )

        if created:
            created_count += 1
            print(f"✓ შეიქმნა: {product.name}")
        else:
            print(f"○ უკვე არსებობს: {product.name}")


def create_test_user():
    """ტესტური მომხმარებლის შექმნა"""
    print("\nტესტური მომხმარებლის შექმნა...")
    user, created = CustomUser.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'გიორგი',
            'last_name': 'მელაშვილი',
            'phone': '555123456',
            'address': 'თბილისი, რუსთაველის 50'
        }
    )

    if created:
        user.set_password('test1234')
        user.save()
        print(f"✓ შეიქმნა: {user.username}")
        print(f"  Username: testuser")
        print(f"  Password: test1234")
    else:
        print(f"○ უკვე არსებობს: {user.username}")


def main():
    print("=" * 60)
    print("ტესტური მონაცემების შექმნა")
    print("=" * 60)

    categories = create_categories()
    create_products(categories)
    create_test_user()

    print("\n" + "=" * 60)
    print("✓ დასრულდა წარმატებით!")
    print("=" * 60)
    print("\nშემდეგი ნაბიჯები:")
    print("1. python manage.py runserver")
    print("2. გადადით: http://127.0.0.1:8000/admin/")
    print("3. შედით admin მონაცემებით")


if __name__ == '__main__':
    main()