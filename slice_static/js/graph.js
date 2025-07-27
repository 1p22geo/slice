async function fetchSimilar(id) {
  const res = await fetch(`${API_URL}/api/samples/similar`, {
    body: JSON.stringify({
      id: id,
      start: 0,
      count: 5,
    }),
    method: "POST",
    mode: "cors",
  });
  const json = await res.json();
  return json.results;
}

async function load(nodes, links) {
  const id = new URL(window.location.href).searchParams.get("id");
  const samples = await fetchSimilar(id);

  for (let i = 0; i < samples.length; i++) {
    fetchSimilar(samples[i]._id).then(neighbors =>
      neighbors.forEach((node1) => {
        if (!nodes.find(n => n._id == node1._id)) {
          nodes.push(node1)
        }
        if (!links[samples[i]._id]) links[samples[i]._id] = {};
        links[samples[i]._id][node1._id] = node1.score

        fetchSimilar(node1._id).then(neighbors =>
          neighbors.forEach((node2) => {
            if (!nodes.find(n => n._id == node2._id)) {
              nodes.push(node2)
            }
            if (!links[node1._id]) links[node1._id] = {};
            links[node1._id][node2._id] = node2.score

            if (!links[node2._id]) links[node2._id] = {};
            links[node2._id][node1._id] = node2.score
          }))

      }))
  }

  setInterval(() => {
    const ctx = document.querySelector("canvas").getContext("2d")
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
    ctx.lineWidth = 1
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      const nodeElement = document.getElementById(node._id);

      // Initialize positions if not already set
      if (!nodeElement.style.left || !nodeElement.style.top) {
        nodeElement.style.left = Math.random() * window.innerWidth + "px";
        nodeElement.style.top = Math.random() * window.innerHeight + "px";
      }

      let node_x = parseInt(nodeElement.style.left);
      let node_y = parseInt(nodeElement.style.top);
      const neighbors = Object.keys(links[node._id]);

      // Apply random movement
      node_x += (Math.random() - 0.5) * 1 + 0.2;
      node_y += (Math.random() - 0.5) * 1 + 0.2;

      neighbors.forEach(neighbor => {
        const neighborElement = document.getElementById(neighbor);
        const neighbor_x = parseInt(neighborElement.style.left);
        const neighbor_y = parseInt(neighborElement.style.top);

        const diff_x = (node_x - neighbor_x);
        const diff_y = (node_y - neighbor_y);
        const correlation = links[node._id][neighbor];
        const proper_distance = (1 - correlation) * 10000;
        const actual_distance = Math.sqrt(diff_x ** 2 + diff_y ** 2);
        const factor = proper_distance - actual_distance;

        const damping = 0.001; // Damping factor
        node_x += diff_x * factor * damping;
        node_y += diff_y * factor * damping;

        ctx.beginPath()
        ctx.moveTo(node_x, node_y)
        ctx.lineTo(neighbor_x, neighbor_y)
        ctx.stroke()
      });

      // Boundary checks
      node_x = Math.max(0, Math.min(node_x, window.innerWidth));
      node_y = Math.max(0, Math.min(node_y, window.innerHeight));

      nodeElement.style.left = node_x + "px";
      nodeElement.style.top = node_y + "px";
    }
  }, 50)
}
