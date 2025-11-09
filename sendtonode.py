import requests
from analyze_claim import analyze_claim

def send_to_node(data):
    try:
        res = requests.post("http://localhost:5000/api/claims/create", json=data)
        print("Sent to backend: ", res.status_code)
    except Exception as e:
        print("Error sending data: ", e)


if __name__ == "__main__":
    claim = input("Enter a claim: ")
    analysis = analyze_claim(claim)
    print(analysis)
    send_to_node(analysis)
