#!/usr/bin/env bash
set -euo pipefail

runSeq() {
	local PNAME_A = "${1:-}"
	local PNAME_B = "${2:-}"
	BASE_PATH = $HOME/.local/bin/amie/addOn	
	if [[ -z "$PNAME_A" || -z "$PNAME_B" ]]; then
		echo "usage of $0 failed!" >&2
		return 1 
	fi	
	echo "Sequential Pipeline: Because multiple versions were detected (future fix)" 
	    local output_A
	    output_A=$("$BASE_PATH/$PNAME_A/seqRun.sh") #add pipeline for Convertors

	    local output_B
	    output_B=$("$BASE_PATH/$PNAME_B/seqRun.sh" "$output_A")

	    echo "$output_B"	
	}
runSeq "${1:-}" "${2:-}"
