function applySelfState(state){
  const id = "system.self";

  const n = getNode(id);

  // self node is always centered slightly
  n.x = window.innerWidth * 0.5;
  n.y = window.innerHeight * 0.5;

  // pulse intensity scales with system activity
  n.pulse = Math.min(1.0,
    (state.trace_len / 50) +
    (state.registry_size / 200)
  );

  // create meta-links
  link(id, "trace");
  link(id, "registry");
  link(id, "ledger");
}
