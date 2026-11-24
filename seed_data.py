"""Seed GramKart with an Indian fashion catalogue (prices in INR). Run: python seed_data.py"""
import os, sys, django
from decimal import Decimal as D
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_core.settings')
django.setup()
from django.contrib.auth.models import User
from accounts.models import Address
from products.models import Category, Brand, Product, ProductImage, Review

U = 'https://images.unsplash.com/photo-%s?w=800&auto=format&fit=crop&q=80'

CATS = [
 ("Men's Fashion", 'bi-person-standing', ['Shirts', 'T-Shirts', 'Jeans & Trousers', "Men's Kurtas & Ethnic"]),
 ("Women's Fashion", 'bi-person-standing-dress', ['Sarees', 'Kurtis & Suits', 'Dresses & Tops', 'Lehengas & Ethnic Sets']),
 ('Footwear', 'bi-lightning-charge', ['Sneakers', 'Sandals & Heels', 'Formal & Casual Shoes']),
 ('Accessories', 'bi-watch', ['Watches', 'Bags & Wallets', 'Sunglasses', 'Jewellery']),
 ("Kids' Wear", 'bi-balloon-heart', ['Boys Clothing', 'Girls Clothing']),
]
BRANDS = ['GramKart Originals', 'Jaipur Loom', 'Banaras Weaves', 'Urban Stitch', 'Desi Denim', 'Kolhapur Craft', 'Tanishka Jewels', 'Kutch Collective', 'Mumbai Street', 'Little Rani']

# name, sku, category, brand, short, mrp, sale, stock, (featured, bestseller, deal), specs, image id
P = [
 ('Classic White Oxford Cotton Shirt', 'MEN-SH-001', 'Shirts', 'Urban Stitch', 'Crisp 100% cotton oxford shirt, regular fit, perfect for office and weddings.', 1499, 999, 60, (1,1,0), {'Fabric': '100% Cotton', 'Fit': 'Regular', 'Care': 'Machine wash'}, '1596755094514-f87e34085b2c'),
 ('Indigo Slim-Fit Casual Shirt', 'MEN-SH-002', 'Shirts', 'Desi Denim', 'Soft washed chambray shirt with a modern slim fit.', 1799, 1199, 45, (0,0,0), {'Fabric': 'Cotton Chambray', 'Fit': 'Slim'}, '1602810318383-e386cc2a3ccf'),
 ('Essential Round-Neck Cotton T-Shirt (Pack of 2)', 'MEN-TS-001', 'T-Shirts', 'GramKart Originals', 'Breathable 180 GSM combed cotton tees, two colours in a pack.', 999, 649, 120, (1,1,0), {'Fabric': '180 GSM Cotton', 'Pack': '2 T-shirts'}, '1521572163474-6864f9cf17ab'),
 ('Graphic Street Oversized Tee', 'MEN-TS-002', 'T-Shirts', 'Mumbai Street', 'Drop-shoulder oversized tee with bold Mumbai-inspired print.', 899, 599, 80, (0,0,0), {'Fit': 'Oversized', 'Fabric': 'Cotton Jersey'}, '1583743814966-8936f5b7be1a'),
 ('Stretch Slim Fit Blue Jeans', 'MEN-JN-001', 'Jeans & Trousers', 'Desi Denim', 'Comfort-stretch denim with a clean mid-wash finish.', 2299, 1499, 70, (1,1,1), {'Fabric': '98% Cotton, 2% Elastane', 'Rise': 'Mid'}, '1542272604-787c3835535d'),
 ('Beige Linen-Blend Chinos', 'MEN-JN-002', 'Jeans & Trousers', 'Urban Stitch', 'Lightweight chinos that stay cool in Indian summers.', 1999, 1299, 50, (0,0,0), {'Fabric': 'Linen-Cotton Blend', 'Fit': 'Tapered'}, '1473966968600-fa801b869a1a'),
 ('Chikankari Cotton Kurta - Ivory', 'MEN-KU-001', "Men's Kurtas & Ethnic", 'Jaipur Loom', 'Hand-embroidered Lucknowi chikankari kurta for festive days.', 2499, 1699, 35, (1,0,1), {'Work': 'Chikankari Embroidery', 'Fabric': 'Pure Cotton'}, '1597983073493-88cd35cf93b0'),
 ('Navy Nehru-Collar Bandhgala Jacket', 'MEN-KU-002', "Men's Kurtas & Ethnic", 'Banaras Weaves', 'Textured bandhgala jacket for weddings and receptions.', 3999, 2799, 18, (0,0,0), {'Fabric': 'Poly-Viscose', 'Lining': 'Satin'}, '1617137968427-85924c800a22'),
 ('Banarasi Silk Saree - Maroon & Gold', 'WOM-SA-001', 'Sarees', 'Banaras Weaves', 'Handwoven Banarasi silk saree with rich gold zari border and blouse piece.', 8999, 5999, 14, (1,1,1), {'Fabric': 'Banarasi Silk', 'Length': '6.3 m with blouse piece', 'Weave': 'Handloom'}, '1610030469983-98e550d6193c'),
 ('Soft Cotton Handloom Saree - Teal', 'WOM-SA-002', 'Sarees', 'Kutch Collective', 'Lightweight daily-wear cotton saree with block-print pallu.', 2499, 1599, 40, (0,1,0), {'Fabric': 'Handloom Cotton', 'Print': 'Ajrakh Block Print'}, '1583391733956-3750e0ff4e8b'),
 ('Kanjivaram Style Art-Silk Saree - Emerald', 'WOM-SA-003', 'Sarees', 'Banaras Weaves', 'Festive art-silk saree with temple border, easy to drape and care for.', 3999, 2599, 25, (1,0,0), {'Fabric': 'Art Silk', 'Occasion': 'Festive / Wedding'}, '1617627143750-d86bc21e42bb'),
 ('Floral Anarkali Kurti Set with Dupatta', 'WOM-KU-001', 'Kurtis & Suits', 'Jaipur Loom', 'Flared Anarkali kurti with palazzo and chiffon dupatta, 3-piece set.', 2799, 1799, 55, (1,1,0), {'Set': 'Kurti + Palazzo + Dupatta', 'Fabric': 'Rayon'}, '1610189844950-62a4b28ee6ec'),
 ('Straight-Cut Cotton Kurti - Mustard', 'WOM-KU-002', 'Kurtis & Suits', 'GramKart Originals', 'Everyday straight kurti with mandarin collar and 3/4 sleeves.', 1199, 799, 90, (0,1,0), {'Fabric': 'Cotton Slub', 'Sleeves': '3/4'}, '1621184455862-c163dfb30e0f'),
 ('Wrap Midi Dress - Rose Print', 'WOM-DR-001', 'Dresses & Tops', 'Urban Stitch', 'Flowy wrap midi dress in a soft rose print, ideal for brunch and parties.', 2299, 1499, 40, (1,0,1), {'Fabric': 'Georgette', 'Length': 'Midi'}, '1595777457583-95e059d581b8'),
 ('Boxy Linen Top - Sage Green', 'WOM-DR-002', 'Dresses & Tops', 'Mumbai Street', 'Relaxed linen-blend top with button front and puff sleeves.', 1299, 849, 65, (0,0,0), {'Fabric': 'Linen Blend', 'Fit': 'Relaxed'}, '1485968579580-b6d095142e6e'),
 ('Bridal Embroidered Lehenga Set - Red', 'WOM-LE-001', 'Lehengas & Ethnic Sets', 'Jaipur Loom', 'Heavy zari-and-sequin lehenga with blouse and net dupatta.', 18999, 12999, 6, (1,0,0), {'Set': 'Lehenga + Blouse + Dupatta', 'Work': 'Zari & Sequin'}, '1583391733981-8498408ee4b6'),
 ('Pastel Sharara Set - Mint', 'WOM-LE-002', 'Lehengas & Ethnic Sets', 'Jaipur Loom', 'Festive sharara set in mint with gota-patti detailing.', 4999, 3299, 22, (0,0,0), {'Set': 'Kurta + Sharara + Dupatta', 'Fabric': 'Georgette'}, '1631947430066-48c30d57b943'),
 ('Everyday Canvas White Sneakers', 'FTW-SN-001', 'Sneakers', 'Mumbai Street', 'Clean white canvas sneakers with cushioned insole, unisex sizes.', 1999, 1299, 85, (1,1,0), {'Upper': 'Canvas', 'Sole': 'Rubber'}, '1549298916-b41d501d3772'),
 ('Runner Pro Lightweight Running Shoes', 'FTW-SN-002', 'Sneakers', 'GramKart Originals', 'Breathable mesh running shoes with shock-absorbing sole.', 2999, 1999, 60, (1,1,1), {'Upper': 'Engineered Mesh', 'Use': 'Running & Gym'}, '1542291026-7eec264c27ff'),
 ('Kolhapuri Leather Chappals - Tan', 'FTW-SA-001', 'Sandals & Heels', 'Kolhapur Craft', 'Handcrafted genuine-leather Kolhapuri chappals, naturally tanned.', 1499, 999, 50, (0,1,0), {'Material': 'Genuine Leather', 'Craft': 'Handmade, Kolhapur'}, '1560343090-f0409e92791a'),
 ('Block-Heel Party Sandals - Gold', 'FTW-SA-002', 'Sandals & Heels', 'Urban Stitch', 'Comfortable 2.5-inch block heels with ankle strap.', 1799, 1199, 38, (0,0,0), {'Heel': '2.5 inch block', 'Closure': 'Buckle'}, '1543163521-1bf539c55dd2'),
 ('Brown Leather Formal Derby Shoes', 'FTW-FC-001', 'Formal & Casual Shoes', 'Kolhapur Craft', 'Polished leather derbies with cushioned footbed for long workdays.', 3499, 2399, 30, (0,0,0), {'Upper': 'Leather', 'Closure': 'Lace-up'}, '1614252235316-8c857d38b5f4'),
 ('Classic Brown Leather Strap Watch', 'ACC-WA-001', 'Watches', 'GramKart Originals', 'Minimal analog watch with genuine leather strap and date display.', 2999, 1799, 45, (1,1,1), {'Movement': 'Quartz', 'Water Resistance': '3 ATM'}, '1523275335684-37898b6baf30'),
 ('Rose-Gold Mesh Watch for Women', 'ACC-WA-002', 'Watches', 'Tanishka Jewels', 'Slim rose-gold dial watch with stainless-steel mesh strap.', 2499, 1599, 32, (0,0,0), {'Movement': 'Quartz', 'Strap': 'Stainless Steel Mesh'}, '1508685096489-7aacd43bd3b1'),
 ('Vegan Leather Tote Bag - Tan', 'ACC-BG-001', 'Bags & Wallets', 'Urban Stitch', 'Roomy tote with zip pocket and laptop sleeve, fits a 14-inch laptop.', 2299, 1499, 40, (1,1,0), {'Material': 'Vegan Leather', 'Capacity': '18 L'}, '1584917865442-de89df76afd3'),
 ('Handmade Jaipuri Embroidered Sling Bag', 'ACC-BG-002', 'Bags & Wallets', 'Kutch Collective', 'Colourful mirror-work sling bag made by Kutch artisans.', 1199, 799, 55, (0,0,0), {'Craft': 'Mirror Work', 'Closure': 'Zip'}, '1590874103328-eac38a683ce7'),
 ('Retro Aviator Sunglasses - UV400', 'ACC-SG-001', 'Sunglasses', 'Mumbai Street', 'Lightweight metal-frame aviators with UV400 polarised lenses.', 1299, 799, 100, (0,1,0), {'Lens': 'UV400 Polarised', 'Frame': 'Metal'}, '1572635196237-14b3f281503f'),
 ('Kundan Choker Necklace Set', 'ACC-JW-001', 'Jewellery', 'Tanishka Jewels', 'Gold-plated kundan choker with matching earrings, perfect with sarees.', 1999, 1299, 28, (1,0,1), {'Plating': 'Gold Plated', 'Set': 'Necklace + Earrings'}, '1599643478518-a784e5dc4c8f'),
 ('Oxidised Silver Jhumka Earrings', 'ACC-JW-002', 'Jewellery', 'Tanishka Jewels', 'Traditional oxidised jhumkas, lightweight for all-day wear.', 599, 399, 150, (0,1,0), {'Finish': 'Oxidised Silver', 'Weight': '14 g'}, '1535632066927-ab7c9ab60908'),
 ("Boys' Kurta Pyjama Set - Royal Blue", 'KID-BY-001', 'Boys Clothing', 'Little Rani', 'Soft cotton festive kurta-pyjama set for boys aged 2-12.', 1299, 849, 60, (0,0,0), {'Ages': '2-12 years', 'Fabric': 'Cotton'}, '1519238263530-99bdd11df2ea'),
 ("Girls' Frilly Party Frock - Pink", 'KID-GL-001', 'Girls Clothing', 'Little Rani', 'Twirl-worthy tulle frock with satin bow, for birthdays and festivals.', 1599, 999, 45, (1,0,0), {'Ages': '2-10 years', 'Fabric': 'Net & Satin'}, '1503944583220-79d8926ad5e2'),
]

REV = [(5, 'Looks even better in person', 'Quality is great and it reached my village in 4 days. Fits perfectly.'),
       (5, 'Value for money', 'Fabric feels premium for the price. Packaging was neat and Cash on Delivery worked smoothly.'),
       (4, 'Good, runs slightly large', 'Lovely product. Order one size down if you are in between sizes.'),
       (5, 'Got many compliments', 'Wore it to a family function and everyone asked where it is from.')]
RUSERS = [('ananya_s', 'Ananya Sharma'), ('rohit_p', 'Rohit Patel'), ('meera_k', 'Meera Kumari'), ('imran_a', 'Imran Ansari')]

def seed():
    print('[*] Seeding GramKart...')
    admin, c = User.objects.get_or_create(username='admin', defaults={'email': 'admin@gramkart.in', 'is_staff': True, 'is_superuser': True, 'first_name': 'GramKart', 'last_name': 'Admin'})
    if c: admin.set_password('admin123'); admin.save(); print('[+] Admin: admin / admin123')
    demo, c = User.objects.get_or_create(username='priya_sharma', defaults={'email': 'priya@example.com', 'first_name': 'Priya', 'last_name': 'Sharma'})
    if c: demo.set_password('password123'); demo.save(); print('[+] Demo user: priya_sharma / password123')
    Address.objects.get_or_create(user=demo, street_address='12 Gandhi Chowk, Near Primary School', defaults=dict(
        full_name='Priya Sharma', phone_number='+91 98765 43210', apartment_suite='Village Rampura', city='Mehsana', state='Gujarat',
        postal_code='384001', country='India', is_default_shipping=True, is_default_billing=True, address_type='home',
        delivery_instructions='Call before delivery. House with blue gate.'))
    cmap = {}
    for name, icon, subs in CATS:
        parent, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon, 'is_featured': True, 'description': f'Shop the latest {name} on GramKart.'})
        cmap[name] = parent
        for s in subs:
            cmap[s], _ = Category.objects.get_or_create(name=s, defaults={'parent': parent, 'icon': icon, 'description': f'{s} for every occasion.'})
    bmap = {b: Brand.objects.get_or_create(name=b)[0] for b in BRANDS}
    rusers = [User.objects.get_or_create(username=u, defaults={'first_name': n, 'email': f'{u}@example.com'})[0] for u, n in RUSERS]
    for name, sku, cat, brand, short, mrp, sale, stock, (f, b, d), specs, img in P:
        prod, _ = Product.objects.get_or_create(sku=sku, defaults=dict(
            name=name, category=cmap[cat], brand=bmap[brand], short_description=short,
            description=short + ' Made for Indian weather and everyday life. Easy 7-day returns and Cash on Delivery available on eligible pin codes.',
            price=D(mrp), discount_price=D(sale), stock=stock, is_featured=bool(f), is_best_seller=bool(b), is_deal_of_the_day=bool(d), specifications=specs))
        ProductImage.objects.get_or_create(product=prod, image_url=U % img, defaults={'is_primary': True, 'order': 0, 'alt_text': name})
        for u, (rating, head, text) in zip(rusers, REV):
            Review.objects.get_or_create(product=prod, user=u, defaults={'rating': rating, 'headline': head, 'comment': text, 'is_verified_purchase': True})
    print(f'[+] Done: {Product.objects.count()} products, {Category.objects.count()} categories.')

if __name__ == '__main__':
    seed()
