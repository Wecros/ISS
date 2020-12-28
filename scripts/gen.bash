#!/usr/bin/env bash

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/28
# Details: Auxiliary bash script generating useful information for the protocol.

# CONSTANTS
readonly SAMPLE_RATE=16000
readonly audio_files=(../audio/*)
readonly audio_files_lastpos=$(( ${#audio_files[@]} - 1 ))
readonly audio_files_last=${audio_files[$audio_files_lastpos]}

# AUXILIARY FUNCTIONS
function show_audio_file() {
    printf "Name: %s\n" "$1"
    printf "Duration: %g seconds\n" "$2"

    printf "          %'d frames\n" "$3"
}

# CODE LOGIC
# Set the script's location as the pwd
cd "$(dirname "$0")" || exit 1

# List the audio files and their length
for file in "${audio_files[@]}"; do
    name=$(basename "$file")
    length=$(soxi "$file" | grep "Duration" | awk '{print $3}' | \
             awk -F: '{print ($1 * 3600) +  ($2 * 60) + $3}')
    frames=$(awk -v time="$length" -v rate="$SAMPLE_RATE" 'BEGIN{print(time * rate)}')
    show_audio_file "$name" "$length" "$frames"
    if [[ "$file" != "$audio_files_last" ]]; then
        printf "\n"
    fi
done
