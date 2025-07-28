from collections import deque
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Tree structure as a nested dictionary
store_tree = {
    "Homepage": {
        "Electronics": {
            "Phones": {},
            "Laptops": {},
            "Accessories": {}
        },
        "Clothing": {
            "Men": {},
            "Women": {},
            "Kids": {}
        },
        "Groceries": {
            "Fresh Produce": {},
            "Snacks": {},
            "Beverages": {},
            "Perfumes": {
                "Axe": {},
                "Fogg": {},
                "Luxe Noir": {}
            }
        },
        "Cosmetic": {
            "Skincare": {},
            "Haircare": {},
            "Perfumes": {
                "Men's": {
                    "Dior": {},
                    "Armani": {},
                    "Luxe Noir": {}
                },
                "Women's": {
                    "Chanel": {},
                    "YSL": {}
                }
            }
        }
    }
}

# BFS Search (find all paths to the target)
def bfs_search_all_paths(tree, target):
    queue = deque([("Homepage", ["Homepage"])])
    found_paths = []
    while queue:
        node, path = queue.popleft()
        subtree = get_subtree(tree, path)
        if node == target:
            found_paths.append(path)
        for child in subtree.get(node, {}):
            queue.append((child, path + [child]))
    return found_paths

def get_subtree(tree, path):
    for p in path:
        tree = tree[p]
    return {path[-1]: tree}

# HTML Template
TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>LUZORE Product Search</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #e9f5f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 700px;
            margin: 60px auto;
            background: #ffffff;
            padding: 35px;
            box-shadow: 0 0 20px rgba(0, 128, 128, 0.2);
            border-radius: 12px;
        }
        h2 {
            text-align: center;
            color: #006666;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        input[type="text"] {
            padding: 12px;
            border: 1px solid #b0d9e8;
            border-radius: 6px;
            font-size: 17px;
        }
        button {
            padding: 12px;
            background-color: #00aaff;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 17px;
        }
        button:hover {
            background-color: #0077aa;
        }
        .result {
            margin-top: 25px;
            font-size: 18px;
            text-align: center;
        }
        .result-path {
            margin: 6px 0;
        }
        .brand-logo {
            display: block;
            margin: 0 auto 20px auto;
            height: 80px;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Perfume_bottle_icon.svg/1200px-Perfume_bottle_icon.svg.png" alt="LUZORE Logo" class="brand-logo">
        <h2>💎 Welcome to LUZORE Product Search</h2>
        <form method="post">
            <input type="text" name="product" placeholder="Enter product name (e.g., Luxe Noir)" required>
            <button type="submit">Search</button>
        </form>

        {% if result_paths %}
            <div class="result">
                <h3>✅ All Paths to "{{ product }}":</h3>
                {% for path in result_paths %}
                    <p class="result-path">{{ path|join(" → ") }}</p>
                {% endfor %}
            </div>
        {% elif product %}
            <div class="result">
                <p>❌ Product "{{ product }}" not found.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    product = None
    result_paths = []
    if request.method == 'POST':
        product = request.form['product']
        result_paths = bfs_search_all_paths(store_tree, product)
    return render_template_string(TEMPLATE, result_paths=result_paths, product=product)

if __name__ == '__main__':
    app.run(debug=True)
