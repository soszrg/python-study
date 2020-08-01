import requests

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
push_data = {
    "UnitNumber": "F8N70290",
    "repairOrderID": "123456",
    "occurTime": "123456"
}
res = requests.post("https://as-customer-portal.azurewebsites.net/otis/sendEntrapmentMsg",
                    headers=headers,
                    data=push_data,
                    timeout=5)
print(res.text)
