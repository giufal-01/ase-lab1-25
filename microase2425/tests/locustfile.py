from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    @task()
    def add(self):
        for a in range(1,10):
            self.client.get(f"/calc/add?a={a}&b=9", name = "Calc Add Endpoint")

    @task()
    def mod(self):
        for a in range(1,10):
            self.client.get(f"/calc/mod?a={a}&b=9", name = "Calc Mod Endpoint")

    @task()
    def random(self):
        for a in range(1,10):
            self.client.get(f"/calc/random?a={a}&b=15", name = "Calc Random Endpoint")

    @task()
    def lower(self):
        for a in range(1,10):
            self.client.get(f"/str/lower?a={a}&b=bbb", name = "Str Lower Endpoint")

    @task()
    def concat(self):
        for a in range(1,10):
            self.client.get(f"/str/concat?a={a}&b=aa", name = "Str Concat Endpoint")

