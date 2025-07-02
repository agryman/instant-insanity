# instant-insanity

Animation showing how to solve Instant Insanity using Graph Theory.

## Google Colab

This project contains Jupyter notebooks.
It is convenient to run these notebooks in Google Colab which at present
uses Python 3.11.11.
The code in this project will therefore run in Python 3.11.11.

I've installed Python 3.11.11 using homebrew on my Mac.
To invoke Python 3.11.11, I use the following command:

```shell
/opt/homebrew/opt/python@3.11/bin/python3.11
```

## Google Cloud Platform Text-to-speech

The `notebooks` directory contains Jupyter notebooks.
Some notebooks contain voice-overs. All text for these
voice-overs is stored in plain text files in the `voiceovers` subdirectory.

That subdirectory contains the `speak.zsh` shell script which uses `curl` to
call the Google Cloud Platform (GCP) `texttospeech` service.
That script depends on the `gcloud` CLI to generate an access token and get the 
active GCP user project which is used for billing.

WillA previously developed a Python script that called the `texttospeech` service.
However, Arthur noticed that all processing could be done with a shell script.
The shell script also sanitizes the input text by removing nontext characters
and replacing tabs and newlines
with spaces since the latter cause anomalies in the synthesized speech.

You must install the `gcloud` CLI, create a GCP account and project, and initialize
your development machine as described in the GCP documentation.
