const response = await fetch("http://127.0.0.1:5000/api/recieve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({message:"Hello World"})
});
const data = await response.json(); 

// 2. Log the actual data object
console.log(data);
