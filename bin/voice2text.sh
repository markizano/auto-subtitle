#!/bin/bash

# Takes the rough edges off docker and makes it look like this script runs natively in the system.
. common.sh

grep -qiP "\x2D-?h(?:elp)?"<<<"$1" && {
    echo "Usage: $0 [options] <audio file>"
    echo "Options:"
    echo "  -h, --help: Show this help message"
    echo "  -l, --language: Language of the audio file (default: en-US)"
    echo "  -o, --output: Output file (default: <audio file>.srt)"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -l|--language)
            LANGUAGE="$2"
            shift
            ;;
        -o|--output)
            OUTPUT="$2"
            shift
            ;;
        *)
            AUDIO_FILE="`realpath $1`"
            ;;
    esac
    shift
done

log_info_msg "Operating on ${AUDIO_FILE}"
docker run --name voice2text -it --rm \
  -v "$(dirname $AUDIO_FILE):/tmp/workspace" \
  -w "/tmp/workspace" \
  voice2text --language en --verbose --srt_only "/tmp/workspace/$(basename $AUDIO_FILE)"
