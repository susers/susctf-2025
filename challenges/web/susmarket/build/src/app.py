from flask import Flask, request, render_template, redirect, url_for, flash
from psycopg_pool import ConnectionPool

app = Flask(__name__)
app.secret_key = "susctf@2025@secret"

pool = ConnectionPool(
    conninfo="dbname=susmarket user=sus password=susctf@2025 host=localhost port=5432",
    min_size=1,
    max_size=10,
    max_lifetime=30,
)


def waf(string):
    for i in ['"', "'"]:
        if i in string:
            return True
    return False


@app.route("/")
def home():
    return redirect(url_for("market"))


@app.route("/market")
def market():
    return render_template("market.html")


@app.route("/list")
def list_products():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, product_name, price, stock FROM products ORDER BY id;"
            )
            products = cur.fetchall()
    return render_template("list.html", products=products)


@app.route("/search", methods=["GET", "POST"])
def search_products():
    products = []
    if request.method == "POST":
        product_name = request.form.get("product_name", "").strip()
        if waf(product_name):
            flash("Dangerous traffic detected!", "danger")
            return redirect(url_for("list_products"))
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, product_name, price, stock FROM products WHERE product_name ILIKE '%{product_name}%';"
                )
                products = cur.fetchall()
    return render_template("search.html", products=products)


@app.route("/buy/<product_id>", methods=["GET", "POST"])
def buy_product(product_id):
    if waf(product_id):
        flash("Dangerous traffic detected!", "danger")
        return redirect(url_for("list_products"))
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id, product_name, price, stock, description FROM products WHERE id = {product_id};"
            )
            product = cur.fetchone()

        if not product:
            flash("Product not found.", "danger")
            return redirect(url_for("list_products"))

        if request.method == "POST":
            qty = int(request.form.get("quantity", 1))
            if qty <= 0:
                flash("Invalid quantity.", "danger")
            elif product[3] < qty:
                flash("Not enough stock.", "warning")
            else:
                new_stock = product[3] - qty
                with conn.cursor() as cur:
                    cur.execute(
                        f"UPDATE products SET stock = {new_stock} WHERE id = {product_id};"
                    )
                conn.commit()
                flash(f"Successfully bought {qty} x {product[1]}!", "success")
                return redirect(url_for("list_products"))

    return render_template("buy.html", product=product)


if __name__ == "__main__":
    app.run(debug=True)
