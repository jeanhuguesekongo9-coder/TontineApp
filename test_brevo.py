import requests

response = requests.post(
    "https://api.brevo.com/v3/smtp/email",
    headers={
        "api-key": "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",
        "Content-Type": "application/json"
    },
    json={
        "sender": {"name": "TontineSecure", "email": "jeanhuguesekongo9@gmail.com"},
        "to": [{"email": "jeanhuguesekongo9@gmail.com"}],
        "subject": "Test Brevo",
        "htmlContent": "<h1>Test email Brevo fonctionne !</h1>"
    }
)
print("Status:", response.status_code)
print("Reponse:", response.text)
