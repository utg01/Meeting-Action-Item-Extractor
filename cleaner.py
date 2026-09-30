import re


def clean_transcripts(transcript):

    if not transcript or not transcript.strip():
        return ""

    cleaned_lines = []

    for line in transcript.splitlines():

        if not line.strip():
            continue

        line = line.strip()
        line = re.sub(r"[ \t]+", " ", line)
        line = re.sub(r"\s*:\s*", ": ", line)

        if ":" in line:
            speaker, message = line.split(":", 1)

            if not message.strip():
                continue

        if line.strip():
            cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines)