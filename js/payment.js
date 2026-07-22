async function pay() {
  const amount = document.getElementById("amount").value;

  const res = await fetch("http://localhost:5000/api/payment/pay", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ amount })
  });

  const data = await res.json();

  alert(data.message);
}
