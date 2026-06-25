#!/usr/bin/env bash

MYCELIUM_HOME="$HOME/mycelium-hub"

# detect if command should go to Mycelium
route_to_mycelium() {
  python3 "$MYCELIUM_HOME/mycelium.py" "$*"
}

# core routing logic
mycelium_router() {
  local cmd="$1"

  # RULE 1: explicit system commands
  if [[ "$cmd" == system* ]]; then
    route_to_mycelium "$@"
    return
  fi

  # RULE 2: media intent keywords
  if [[ "$cmd" == play* ]] || [[ "$cmd" == watch* ]]; then
    route_to_mycelium "$@"
    return
  fi

  # RULE 3: knowledge queries
  if [[ "$cmd" == what* ]] || [[ "$cmd" == search* ]]; then
    route_to_mycelium "$@"
    return
  fi

  # DEFAULT: fallback to shell
  command "$@"
}

# expose function globally
alias m=mycelium_router
