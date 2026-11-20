#!/bin/sh
# Run the bundled installer from one checkout, including its matching assets.
set -eu
main() {
    bundle=$(mktemp -d)
    trap 'rm -rf "$bundle"' EXIT
    trap 'exit 1' HUP INT TERM
    git clone --quiet --depth 1 https://github.com/ta-dadadada/skills.git "$bundle/repo"
    cli="$bundle/repo/dev/install-agent-rules/scripts/install_rules.py"
    if [ "$#" -eq 0 ]; then
        python3 "$cli" list
        printf 'Rule ID to install/update in %s (blank to cancel): ' "$PWD" >&2
        if ! IFS= read -r rule </dev/tty; then
            echo 'No terminal. Pass install --rule ID --project PATH, or list.' >&2
            return 2
        fi
        [ -n "$rule" ] || return 0
        set -- install --rule "$rule" --project "$PWD"
    fi
    case "$1" in
        install|uninstall)
            operation=$1
            shift
            if python3 "$cli" plan "$@" --operation "$operation" > "$bundle/plan.json"; then
                id=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["plan_id"])' < "$bundle/plan.json")
                python3 "$cli" apply "$@" --operation "$operation" --plan-id "$id"
            else
                status=$?
                cat "$bundle/plan.json"
                return "$status"
            fi
            ;;
        *) python3 "$cli" "$@" ;;
    esac
}
main "$@"
