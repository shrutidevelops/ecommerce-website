from flask import Flask,render_template,request,redirect,session
import mysql.connector
app=Flask(__name__)
app.secret_key="shrushop_secret_key"
db=mysql.connector.connect(host="localhost",user="root",password="1234",database="ecommerce")

def admin_required():

    if 'user_id' not in session:
        return False

    if session.get('role') != 'admin':
        return False

    return True

@app.route("/")
def home():
    cursor = db.cursor()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template(
        "index.html",
        categories=categories,
        products=products
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        t1 = request.form["t1"]
        t2 = request.form["t2"]
        t3 = request.form["t3"]

        cursor = db.cursor()

        cursor.execute(
            "insert into users(name,email,password) values(%s,%s,%s)",
            (t1, t2, t3)
        )

        db.commit()
        cursor.close()

        return """
        <script>
            alert("Registration Successful!");
            window.location.href="/register";
        </script>
        """

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        t1 = request.form["t1"]
        t2 = request.form["t2"]

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (t1, t2)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:

            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['role'] = user[4]

            return """
            <script>
                alert("Login Successful!");
                window.location.href="/";
            </script>
            """

        else:

            return """
            <script>
                alert("Invalid Email or Password");
                window.location.href="/login";
            </script>
            """

    return render_template("login.html")

@app.route('/logout')
def logout():

    session.clear()

    return """
    <script>
        alert("Logged out successfully!");
        window.location.href="/";
    </script>
    """

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():

    if 'user_id' not in session:
     return redirect('/login')

    if not admin_required():
        return redirect('/')

    if request.method == 'POST':

        t1 = request.form["t1"]  
        t6 = request.form["t6"]
        t4 = request.form["t4"]  
        t2 = request.form["t2"]  
        t3 = request.form["t3"]  
        t5 = request.form["t5"]  

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO products
            (product_name, category_id, description, price, stock, image)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (t1, t6, t4, t2, t3, t5))


        db.commit()
        cursor.close()

        return redirect('/products')

    return render_template("addproduct.html")

@app.route('/products')
def products():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    cursor.close()

    return render_template("products.html", data=data)

@app.route('/deleteproduct/<int:id>')
def deleteproduct(id):

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE product_id=%s",
        (id,)
    )

    db.commit()
    cursor.close()

    return redirect('/products')

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')

    cursor = db.cursor()

    if request.method == 'POST':

        t1 = request.form["t1"]  
        t2 = request.form["t2"]  
        t3 = request.form["t3"]  
        t4 = request.form["t4"]  
        t5 = request.form["t5"] 

        cursor.execute("""
            UPDATE products
            SET product_name=%s,
                description=%s,
                price=%s,
                stock=%s,
                image=%s
            WHERE product_id=%s
        """, (t1, t2, t3, t4, t5, id))

        db.commit()
        cursor.close()

        return """
        <script>
        alert("Record updated successfully!");
        window.location.href="/products";
        </script>
       """

    cursor.execute(
        "SELECT * FROM products WHERE product_id=%s",
        (id,))
    
    data = cursor.fetchone()
    if not data:
     cursor.close()
     return redirect('/products')

    cursor.close()

    return render_template("updateproduct.html", data=data)


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')
    
    if request.method == 'POST':

        t1 = request.form["t1"]
        t2 = request.form["t2"]
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO categories(category_name,image) VALUES(%s,%s)",
            (t1,t2))

        db.commit()
        cursor.close()

        return """
        <script>
            alert("Category added successfully!");
            window.location.href="/categories";
        </script>
        """

    return render_template("addcategory.html")

@app.route('/categories')
def categories():
   

    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close()

    return render_template("categories.html", data=data)

@app.route('/categoryproducts/<int:id>')
def categoryproducts(id):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE category_id=%s",
        (id,)
    )
    data = cursor.fetchall()
    cursor.close()

    return render_template('products.html', data=data)

@app.route('/deletecategory/<int:id>')
def deletecategory(id):

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM categories WHERE category_id=%s",
        (id,)
    )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Category deleted successfully!");
        window.location.href="/categories";
    </script>
    """

@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')

    cursor = db.cursor()

    if request.method == 'POST':

        t1 = request.form["t1"]

        cursor.execute(
            "UPDATE categories SET category_name=%s WHERE category_id=%s",
            (t1, id)
        )

        db.commit()
        cursor.close()

        return """
        <script>
            alert("Category updated successfully!");
            window.location.href="/categories";
        </script>
        """

    cursor.execute(
        "SELECT * FROM categories WHERE category_id=%s",
        (id,)
    )

    data = cursor.fetchone()
    if not data:
     cursor.close()
     return redirect('/categories')

    cursor.close()

    return render_template("updatecategory.html", data=data)

@app.route('/addtocart/<int:id>')
def addtocart(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = db.cursor()

    # Check product stock
    cursor.execute(
        "SELECT stock FROM products WHERE product_id=%s",
        (id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return redirect('/products')

    stock = product[0]

    if stock <= 0:
        cursor.close()
        return """
        <script>
            alert("This product is out of stock!");
            window.location.href="/products";
        </script>
        """

    # Check if product already exists in cart
    cursor.execute(
        "SELECT quantity FROM cart WHERE user_id=%s AND product_id=%s",
        (user_id, id)
    )

    cart_item = cursor.fetchone()

    if cart_item:

        current_qty = cart_item[0]

        if current_qty >= stock:
            cursor.close()
            return """
            <script>
                alert("You cannot add more than the available stock!");
                window.location.href="/products";
            </script>
            """

        cursor.execute(
            "UPDATE cart SET quantity=quantity+1 WHERE user_id=%s AND product_id=%s",
            (user_id, id)
        )

    else:

        cursor.execute(
            "INSERT INTO cart(user_id, product_id, quantity) VALUES(%s,%s,%s)",
            (user_id, id, 1)
        )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Product added to cart!");
        window.location.href="/products";
    </script>
    """

@app.route('/cart')
def cart():
     if 'user_id' not in session:
        return redirect('/login')

     cursor = db.cursor()
     user_id = session['user_id']
     cursor.execute("""
        SELECT cart.cart_id,
               products.product_name,
               products.price,
               cart.quantity,
               products.price * cart.quantity AS subtotal,
               products.image
        FROM cart
        JOIN products
        ON cart.product_id = products.product_id
        WHERE cart.user_id=%s
        """, (user_id,))

     data = cursor.fetchall()

     total = 0
     for row in data:
        total += row[4]

     cursor.close()

     return render_template("cart.html", data=data, total=total)

@app.route('/deletecart/<int:id>')
def deletecart(id):


    if 'user_id' not in session:
        return redirect('/login')
    

    user_id = session['user_id']
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE cart_id=%s AND user_id=%s",
        (id, user_id)
    )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Item removed from cart!");
        window.location.href="/cart";
    </script>
    """

@app.route('/updatecart/<int:id>', methods=['GET', 'POST'])
def updatecart(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = db.cursor()

    if request.method == 'POST':

        t1 = request.form["t1"]   # quantity

        cursor.execute(
            "UPDATE cart SET quantity=%s WHERE cart_id=%s AND user_id=%s",
            (t1, id, user_id)
        )

        db.commit()
        cursor.close()

        return """
        <script>
            alert("Quantity updated successfully!");
            window.location.href="/cart";
        </script>
        """

    cursor.execute(
        "SELECT * FROM cart WHERE cart_id=%s AND user_id=%s",
        (id, user_id)
    )

    data = cursor.fetchone()

    if not data:
        cursor.close()
        return redirect('/cart')

    cursor.close()

    return render_template("updatecart.html", data=data)

@app.route('/placeorder', methods=['POST'])
def placeorder():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    payment = request.form.get('payment')

    cursor = db.cursor()

    # Calculate total amount
    cursor.execute("""
        SELECT SUM(products.price * cart.quantity)
        FROM cart
        JOIN products
        ON cart.product_id = products.product_id
        WHERE cart.user_id=%s
    """, (user_id,))

    total = cursor.fetchone()[0]

    # Check if cart is empty
    if total is None:
        cursor.close()
        return """
        <script>
            alert("Your cart is empty!");
            window.location.href="/cart";
        </script>
        """

    # Get cart items with stock
    cursor.execute("""
        SELECT cart.product_id,
               cart.quantity,
               products.stock
        FROM cart
        JOIN products
        ON cart.product_id = products.product_id
        WHERE cart.user_id=%s
    """, (user_id,))

    items = cursor.fetchall()

    # Check stock
    for item in items:
        product_id = item[0]
        quantity = item[1]
        stock = item[2]

        if quantity > stock:
            cursor.close()
            return """
            <script>
                alert("One or more products do not have enough stock!");
                window.location.href="/cart";
            </script>
            """

    # Create order
    cursor.execute("""
        INSERT INTO orders
        (user_id, total_amount, order_date, status, payment_method)
        VALUES (%s, %s, CURDATE(), 'Pending', %s)
    """, (user_id, total, payment))

    db.commit()

    order_id = cursor.lastrowid

    # Insert order items and reduce stock
    for item in items:

        product_id = item[0]
        quantity = item[1]

        cursor.execute(
            "SELECT price FROM products WHERE product_id=%s",
            (product_id,)
        )

        price = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, quantity, price))

        cursor.execute("""
            UPDATE products
            SET stock = stock - %s
            WHERE product_id=%s
        """, (quantity, product_id))

    # Clear cart
    cursor.execute(
        "DELETE FROM cart WHERE user_id=%s",
        (user_id,)
    )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Order placed successfully!");
        window.location.href="/orders";
    </script>
    """

@app.route('/orders')
def orders():

    if 'user_id' not in session:
        return redirect('/login')


    user_id = session['user_id']
    cursor = db.cursor()

    cursor.execute("""
        SELECT order_id,
               total_amount,
               order_date,
               status,payment_method
        FROM orders
        WHERE user_id=%s
    """, (user_id,))

    data = cursor.fetchall()

    cursor.close()

    return render_template("orders.html", data=data)

@app.route('/orderdetails/<int:id>')
def orderdetails(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cursor = db.cursor()

    cursor.execute("""
        SELECT products.image,
               products.product_name,
               order_items.quantity,
               order_items.price
        FROM order_items
        JOIN products
        ON order_items.product_id = products.product_id
        JOIN orders
        ON order_items.order_id = orders.order_id
        WHERE order_items.order_id=%s
        AND orders.user_id=%s
    """, (id, user_id))

    data = cursor.fetchall()

    cursor.close()

    return render_template("orderdetails.html", data=data)

@app.route('/cancelorder/<int:id>')
def cancelorder(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cursor = db.cursor()

    cursor.execute("""
        UPDATE orders
        SET status='Cancelled'
        WHERE order_id=%s
        AND user_id=%s
    """, (id, user_id))

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Order cancelled successfully!");
        window.location.href="/orders";
    </script>
    """

@app.route('/addtowishlist/<int:id>')
def addtowishlist(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO wishlist(user_id, product_id) VALUES(%s,%s)",
        (user_id, id)
    )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Added to wishlist!");
        window.location.href="/products";
    </script>
    """

@app.route('/wishlist')
def wishlist():
   
   if 'user_id' not in session:
        return redirect('/login')

   user_id = session['user_id']

   cursor = db.cursor()

   cursor.execute("""
        SELECT wishlist.wishlist_id,
               products.product_name,
               products.price,
               products.image
        FROM wishlist
        JOIN products
        ON wishlist.product_id = products.product_id
        WHERE wishlist.user_id=%s
    """, (user_id,))

   data = cursor.fetchall()

   cursor.close()

   return render_template("wishlist.html", data=data)

@app.route('/deletewishlist/<int:id>')
def deletewishlist(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM wishlist WHERE wishlist_id=%s AND user_id=%s",
        (id, user_id)
    )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Removed from wishlist!");
        window.location.href="/wishlist";
    </script>
    """

@app.route('/wishlisttocart/<int:id>')
def wishlisttocart(id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = db.cursor()

    # Get wishlist item belonging to current user only
    cursor.execute(
        "SELECT product_id FROM wishlist WHERE wishlist_id=%s AND user_id=%s",
        (id, user_id)
    )

    data = cursor.fetchone()

    if not data:
        cursor.close()
        return redirect('/wishlist')

    product_id = data[0]

    # Add product to cart
    cursor.execute(
        "INSERT INTO cart(user_id, product_id, quantity) VALUES(%s,%s,%s)",
        (user_id, product_id, 1)
    )

    # Remove from wishlist
    cursor.execute(
        "DELETE FROM wishlist WHERE wishlist_id=%s AND user_id=%s",
        (id, user_id)
    )

    db.commit()
    cursor.close()

    return redirect('/wishlist')


@app.route('/contact', methods=['GET', 'POST'])
def contact():


    if request.method == 'POST':

        t1 = request.form["t1"]
        t2 = request.form["t2"]
        t3 = request.form["t3"]

        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO contact_messages(name, email, message) VALUES(%s,%s,%s)",
            (t1, t2, t3)
        )

        db.commit()
        cursor.close()

        return """
        <script>
            alert("Message sent successfully!");
            window.location.href="/contact";
        </script>
        """

    return render_template("contact.html")
    

@app.route('/messages')
def messages():

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')

    cursor = db.cursor()

    cursor.execute("SELECT * FROM contact_messages")

    data = cursor.fetchall()

    cursor.close()

    return render_template("messages.html", data=data)

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
     return redirect('/login')
    
    if not admin_required():
        return redirect('/')

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categories")
    categories = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contact_messages")
    messages = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "dashboard.html",
        users=users,
        categories=categories,
        products=products,
        orders=orders,
        messages=messages)

@app.route('/search')
def search():
    q = request.args.get('q')

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE product_name LIKE %s",
        ('%' + q + '%',)
    )

    data = cursor.fetchall()
    cursor.close()

    return render_template('products.html', data=data)

@app.route('/subscribe', methods=['POST'])
def subscribe():

    email = request.form['email']
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM newsletter WHERE email=%s",
        (email,)
    )

    data = cursor.fetchone()

    if data:
        return """
        <script>
            alert("You are already subscribed!");
            window.location.href="/";
        </script>
        """

    cursor.execute(
        "INSERT INTO newsletter(email) VALUES(%s)",
        (email,)
    )

    db.commit()
    cursor.close()

    return """
    <script>
        alert("Thank you for subscribing! ✨");
        window.location.href="/";
    </script>
    """

@app.route('/checkout')
def checkout():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template('checkout.html')


if __name__ == '__main__':
    app.run(debug=True)