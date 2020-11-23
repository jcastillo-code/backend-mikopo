from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import json

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
        }
    })

#BD postgres connection
myconn = psycopg2.connect(
    database="mikopo",
    user="postgres",
    password="123456"
    )

#OK - Get Prueba
@app.route('/ping')
def ping():
    return jsonify({"message":"pong!"})

#OK - listar productos
@app.route('/products', methods=['GET'])
def getProducts():
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM producto")
    products = cur.fetchall() 
    if (len(products) > 0):
        return jsonify(products)
    return jsonify({"status":201, "message": "Product not found"})

#OK - buscar por producto por ID
@app.route('/productsById/<string:product_id>')
def getProductById(product_id):
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT * from producto WHERE id=%s""",(product_id))
    products = cur.fetchall() 
    if (len(products) > 0):
        return jsonify(products)
    return jsonify({"status":201, "message": "Product not found"})

#OK - buscar por producto por nombre
@app.route('/productsByName/<string:product_name>')
def getProductByName(product_name):
    print(product_name)
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT * from producto WHERE name LIKE %s """,("%"+product_name+"%",))
    products = cur.fetchall() 
    if (len(products) > 0):
        return jsonify(products)
    return jsonify({"status":201, "message": "Product not found"})

#OK - crear nuevo Producto
@app.route('/products/newproduct', methods=['POST'])
def newProduct():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    category = request.json['category']
    url_image = request.json['url_image']
    
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""INSERT INTO producto(name,description,price,category,url_image) VALUES(%s,%s,%s,%s,%s)""",(name, description, price, category, url_image))
    myconn.commit()

    return jsonify({"status":201, "message": "product added succesfully"})

#OK - Modificar Producto
@app.route('/products/modifyProduct/<string:product_id>', methods=['PUT'])
def modifyProduct(product_id):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    category = request.json['category']
    url_image = request.json['url_image']

    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""UPDATE producto SET name = %s, description = %s, price = %s, category = %s, url_image = %s WHERE id = %s""",(name, description, price, category, url_image, product_id))
    myconn.commit()

    return jsonify({"status":201, "message": "product modified succesfully"})

#OK - Eliminar Producto
@app.route('/products/deleteProduct/<string:product_id>', methods=['DELETE'])
def deleteProduct(product_id):
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""DELETE from producto WHERE id=%s""",(product_id))
    myconn.commit()
    return jsonify({"status":200, "message":"producto eliminado"})

#OK - registrar nueva venta
@app.route('/venta/addSell', methods=['POST'])
def newSell():
    id_product = request.json['id_product']
    name_product = request.json['name_product']
    price_product = request.json['price_product']
    
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""INSERT INTO venta(id_product,name_product,price_product) VALUES(%s,%s,%s)""",(id_product,name_product,price_product))
    myconn.commit()

    return jsonify({"status":201, "message": "new Sell succesfully"})

#OK - listar data para el grafico
@app.route('/venta/dataGraphic', methods=['GET'])
def getDataGraphic():
    cur=myconn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT name_product as name, count(id_product) as y FROM venta GROUP BY id_product, name")
    dataSells = cur.fetchall() 
    if (len(dataSells) > 0):
        return jsonify(dataSells)
    return jsonify({"status":201, "message": "not data"})

if __name__ == '__main__':
    app.run(debug=True, port=4000)