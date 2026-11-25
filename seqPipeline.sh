#!/usr/bin/env bash
# Converts a torch.export .pt2 package (an ExportedProgram) to CoreML with pt2ToMlmodel/main.py, in that folder's own Python
# environment (venv).
# Usage: seqPipeline.sh [source.pt2 [destination.mlpackage]]
# Without a source, main.py builds MobileNetV2 as it does on its own. The default destination is pt2ToMlmodel/coreMl.mlpackage.
# The converter's output goes to stderr; the last line on stdout is the destination path.
set -euo pipefail

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
converter="$here/pt2ToMlmodel"
python="$converter/venv/bin/python"

if [[ $# -gt 2 ]]; then
    echo "usage: $0 [source.pt2 [destination.mlpackage]]" >&2
    exit 2
fi
if [[ $# -ge 1 && ! -f "$1" ]]; then
    echo "no source package at $1" >&2
    exit 2
fi
if [[ ! -x "$python" ]]; then
    echo "no Python at $python; set up the converter's environment first (install114.sh)" >&2
    exit 1
fi

input_args=()
if [[ $# -ge 1 ]]; then
    input_args=(--input "$(cd -- "$(dirname -- "$1")" && pwd)/$(basename -- "$1")")
fi

dest="$converter/coreMl.mlpackage"
if [[ $# -ge 2 ]]; then
    mkdir -p -- "$(dirname -- "$2")"
    dest="$(cd -- "$(dirname -- "$2")" && pwd)/$(basename -- "$2")"
fi

(cd "$converter" && "$python" main.py ${input_args[@]+"${input_args[@]}"} --output "$dest" >&2)
echo "$dest"
