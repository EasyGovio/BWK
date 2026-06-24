import os

domain = "example.com"
if os.path.exists("CNAME"):
    with open("CNAME") as f:
        domain = f.read().strip()
if not domain:
    domain = os.path.basename(os.getcwd())  # repo adını domain olarak kullan
print("Domain:", domain)
