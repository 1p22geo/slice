function submitQuery(query, tags) {
  const url = new URL("/search", window.location.origin);
  url.searchParams.append("query", query);
  url.searchParams.append("tags", JSON.stringify(tags ?? []));
  window.location.replace(url);
}

async function request() {
  const query = new URL(window.location.href).searchParams.get("query");
  const res = await fetch(`${API_URL}/api/samples/search`, {
    body: JSON.stringify({
      query: query,
      tags: JSON.parse(new URL(window.location.href).searchParams.get('tags')) ?? [],
      btags: [],
      start: 0,
      count: 10,
    }),
    method: "POST",
    mode: "cors",
  });
  const json = await res.json();
  return json;
}

async function fetchTags() {
  const res = await fetch(`${API_URL}/api/tags/tags`, {
    method: "GET",
    mode: "cors",
  });
  const json = await res.json();
  return json;
}
