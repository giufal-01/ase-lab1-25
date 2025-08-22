from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    @task()
    def add(self):
        for a in range(1,10):
            self.client.get(f"/calc/add?a={a}&b=9", name = "Calc Add Endpoint")

