#!/bin/zsh

# Check argument count
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <name>"
  exit 1
fi

BASENAME="$1"
INPUT_FILE="${BASENAME}.txt"
OUTPUT_FILE="${BASENAME}.mp3"
REQUEST_FILE="${BASENAME}.request.json"
RESPONSE_FILE="${BASENAME}.response.json"

# Check if input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input file '$INPUT_FILE' not found."
  exit 1
fi

# Sanitize input text: remove non-printable/control characters except for space and punctuation
SANITIZED_TEXT=$(LC_ALL=C tr -cd '\11\12\15\40-\176' < "$INPUT_FILE" | tr '\n\r\t' ' ' | sed 's/  */ /g')

# Escape the text for JSON
ESCAPED_TEXT=$(printf '%s' "$SANITIZED_TEXT" | jq -Rs .)

# Build request JSON
cat > "$REQUEST_FILE" <<EOF
{
  "input": {"text": $ESCAPED_TEXT},
  "voice": {
    "name": "en-US-Chirp3-HD-Aoede",
    "languageCode": "en-US"
  },
  "audioConfig": {
    "audioEncoding": "MP3",
    "volumeGainDb": 0.0
  }
}
EOF

# Get access token
ACCESS_TOKEN=$(gcloud auth application-default print-access-token)

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [[ -z "$PROJECT_ID" ]]; then
  echo "Error: No active project set. Run 'gcloud config set project PROJECT_ID'"
  exit 1
fi

# Send request and save response
curl -s -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: $PROJECT_ID" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data @"$REQUEST_FILE" \
  "https://texttospeech.googleapis.com/v1/text:synthesize" \
  -o "$RESPONSE_FILE"

# Extract audio content
AUDIO_CONTENT=$(jq -r '.audioContent' < "$RESPONSE_FILE")

# Check for error
if [[ "$AUDIO_CONTENT" == "null" || -z "$AUDIO_CONTENT" ]]; then
  echo "❌ Error: API response did not contain audioContent."
  echo "Check $RESPONSE_FILE for details."
  exit 1
fi

# Decode audio content to mp3
echo "$AUDIO_CONTENT" | base64 --decode > "$OUTPUT_FILE"

echo "✅ Speech synthesis complete."
echo "→ Output audio: $OUTPUT_FILE"
echo "→ Request saved to: $REQUEST_FILE"
echo "→ Response saved to: $RESPONSE_FILE"
