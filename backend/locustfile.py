from locust import HttpUser, task, between


class FastAPILoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def read_brands(self):
        self.client.get("/api/brands")
        
    @task
    def read_categories(self):
        self.client.get("/api/categories")
    
    @task
    def read_products(self):
        self.client.get("/api/products")
        
    @task
    def read_product(self):
        self.client.get("/api/products/8848b92c-0d6f-4779-92e3-54da4731608a")
        
    @task
    def read_products_by_category(self):
        self.client.get("/api/products?page_size=12&brand_ids=bbbe86f0-5b5e-4169-a536-4b1bb0f81b54")
        