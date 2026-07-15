import json
import urllib.request
import urllib.error
import random

API_URL = "http://localhost:8000"
USER_EMAIL = "tester@example.com"
USER_PASS = "securepassword123"
USER_NAME = "tester"

def make_request(url, method="GET", data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8")), res.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            body = json.loads(body)
        except:
            pass
        return body, e.code
    except Exception as e:
        return str(e), 500

print("=== 1. Registrando / Iniciando sesión ===")
# Intentar registrar
make_request(f"{API_URL}/auth/register", "POST", {
    "username": USER_NAME,
    "email": USER_EMAIL,
    "password": USER_PASS
})

# Iniciar sesión
login_res, status = make_request(f"{API_URL}/auth/login", "POST", {
    "email": USER_EMAIL,
    "password": USER_PASS
})

if status != 200:
    print(f"Error al iniciar sesión ({status}): {login_res}")
    exit(1)

token = login_res.get("access_token")
print("¡Token de acceso obtenido correctamente!")

print("\n=== 2. Creando 50 Productos ===")
product_ids = []
for i in range(1, 51):
    prod_data = {
        "name": f"Producto de Prueba #{i}",
        "description": f"Esta es la descripción del producto de prueba número {i}",
        "price": float(random.randint(10, 110)),
        "images_products": [f"https://picsum.photos/200/300?random={i}"]
    }
    res, status = make_request(f"{API_URL}/api/v1/products", "POST", prod_data, token)
    if status == 201:
        prod_id = res.get("id")
        product_ids.append(prod_id)
        print(f"Creado Producto #{i}: {prod_id}")
    else:
        print(f"Error al crear Producto #{i} ({status}): {res}")

print("\n=== 3. Creando 20 Listas de Favoritos ===")
favorite_ids = []
for i in range(1, 21):
    fav_data = {
        "name": f"Mi Lista de Favoritos #{i}",
        "description": f"Esta lista de favoritos contiene una selección premium número {i}"
    }
    res, status = make_request(f"{API_URL}/api/v1/favorites", "POST", fav_data, token)
    if status == 201:
        fav_id = res.get("id")
        favorite_ids.append(fav_id)
        print(f"Creada Lista #{i}: {fav_id}")
    else:
        print(f"Error al crear Lista #{i} ({status}): {res}")

print("\n=== 4. Asociando Productos a Listas de Favoritos ===")
if not product_ids:
    print("Error: No se crearon productos, abortando asociación.")
    exit(1)

for fav_id in favorite_ids:
    num_associations = random.randint(3, 8)
    chosen_products = random.sample(product_ids, min(num_associations, len(product_ids)))
    print(f"Asociando {len(chosen_products)} productos a la lista {fav_id}...")
    
    for prod_id in chosen_products:
        res, status = make_request(
            f"{API_URL}/api/v1/favorites/{fav_id}/products/{prod_id}",
            "POST",
            token=token
        )
        if status != 200:
            print(f"  -> Error al asociar producto {prod_id}: {res}")
        else:
            print(f"  -> Agregado producto {prod_id}")

print("\n=== ¡Listo! Proceso de carga finalizado con éxito ===")
