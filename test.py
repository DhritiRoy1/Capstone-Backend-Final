import requests
url = "http://127.0.0.1:5000/"
data = [{"Url":"https://www.youtube.com/watch?v=0Cjph5CvErE","Time":590823},{"Url":"https://www.youtube.com/","Time":44150},{"Url":"https://www.netflix.com/browse","Time":337799}]
for i in range(len(data)):
    requests.put(url+str(i),json=data[i])
    response = requests.get(url+str(i))
    print(f"Status Code: {response.status_code}")
    print(f"Response Text (Snippet): {response.text[:200]}") # Print the first 200 chars
    print("-" * 20)
