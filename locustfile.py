from locust import HttpUser, task, between
import random

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Connexion au démarrage"""
        self.client.post("/login", data={
            "username": "admin123",
            "password": "admin123"
        })

    @task(5)
    def voir_produits(self):
        self.client.get("/")

    @task(3)
    def voir_detail_produit(self):
        product_id = random.randint(1, 5)
        self.client.get(f"/product/{product_id}")

    @task(2)
    def ajouter_au_panier(self):
        product_id = random.randint(1, 5)
        self.client.get(f"/add_to_cart/{product_id}")

    @task(1)
    def voir_panier(self):
        self.client.get("/cart")

    @task(1)
    def rechercher(self):
        queries = ["souris", "clavier", "écran"]
        self.client.get(f"/search?q={random.choice(queries)}")