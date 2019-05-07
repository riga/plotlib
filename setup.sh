#!/usr/bin/env bash

action() {
    # determine the directory of this file
    if [ ! -z "$ZSH_VERSION" ]; then
        local this_file="${(%):-%x}"
    else
        local this_file="${BASH_SOURCE[0]}"
    fi
    local this_dir="$( cd "$( dirname "$this_file" )" && pwd )"

    # update the python path
    export PYTHONPATH="$this_dir:$PYTHONPATH"
}
action "$@"
