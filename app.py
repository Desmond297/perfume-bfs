from collections import deque
from flask import Flask, render_template_string, request

app = Flask(__name__)

store_tree = {
    "Homepage": {
        "Electronics": { "Phones": {}, "Laptops": {}, "Accessories": {} },
        "Clothing": { "Men": {}, "Women": {}, "Kids": {} },
        "Groceries": {
            "Fresh Produce": {}, "Snacks": {}, "Beverages": {},
            "Perfumes": { "Axe": {}, "Fogg": {}, "Luxe Noir": {} }
        },
        "Cosmetic": {
            "Skincare": {}, "Haircare": {},
            "Perfumes": {
                "Men's": { "Dior": {}, "Armani": {}, "Luxe Noir": {} },
                "Women's": { "Chanel": {}, "YSL": {} }
            }
        }
    }
}

def bfs_search(tree, target):
    from collections import deque
    queue = deque([("Homepage", ["Homepage"])])
    while queue:
        node, path = queue.popleft()
        current = get_subtree(tree, path)
        if node == target:
            return path
        for child in current.get(node, {}):
            queue.append((child, path + [child]))
    return None

def get_subtree(tree, path):
    for key in path:
        tree = tree[key]
    return {path[-1]: tree}

TEMPLATE = '''
<!DOCTYPE html>
<html><head><title>Store BFS UI</title></head><body>
<h2>Search Product</h2>
<form method="post">
  <input type="text" name="product" placeholder="Product name" required>
  <button type="submit">Search</button>
</form>
{% if result %}
  <h3>Path: {{ result|join(" → ") }}</h3>
{% elif product %}
  <p>“{{ product }}” not found.</p>
{% endif %}
</body></html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    product = None
    if request.method == 'POST':
        product = request.form['product']
        result = bfs_search(store_tree, product)
    return render_template_string(TEMPLATE, result=result, product=product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
