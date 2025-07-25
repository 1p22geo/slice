async function request() {
  const id = new URL(window.location.href).searchParams.get("id");
  const res = await fetch(`${API_URL}/api/samples/similar`, {
    body: JSON.stringify({
      id: id,
      start: 0,
      count: 10,
    }),
    method: "POST",
    mode: "cors",
  });
  const json = await res.json();
  return json;
}
