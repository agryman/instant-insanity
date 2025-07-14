# instant-insanity

Animation showing how to solve Instant Insanity using Graph Theory.

## pip

I install this project as an editable package running the following command
in the project root directory with the virtual environment activated.

```shell
pip install -e .
```

Sometimes PyCharm fails to pick up changes.
Run this command to force an update to the virtual environment:

```shell
pip install -U -e .
```

## PyCharm

Sometimes PyCharm loses the project configuration.
I believe this is possibly associated with branch creation.
When this happens, run the menu command to recreate the project configuration.
Run the menu command `File -> Repair IDE` or `File -> Invalidate Caches...`.

## Google Colab

This project contains Jupyter notebooks.
It is convenient to run these notebooks in Google Colab, which at present
uses Python 3.11.11.
The code in this project will therefore run in Python 3.11.11.

I've installed Python 3.11.11 using homebrew on my Mac.
To invoke Python 3.11.11, I use the following command:

```shell
/opt/homebrew/opt/python@3.11/bin/python3.11
```

## Google Cloud Platform Text-to-Speech

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

## Manim Community Edition

I am using Manim to generate animations.

GitHub: https://github.com/manimcommunity/manim

PyPI: https://pypi.org/project/manim/

Docs: https://docs.manim.community/en/stable/index.html

The Manim documentation recommends inexperienced users to use `uv` to install Manim.
I already have a virtual environment and am comfortable with `pip` so I have installed `manim` using `pip`:

```shell
pip install manim
```

The Manim documentation describes how to set up remote Jupyter Notebook services, such as
Google Colab, to run Manim.
Defer setting up remote Jupyter Notebooks for now.

The Manim documentation also mentions a plig-in for VSCode called *Manim Sideview*.
I looked at a YouTube video about it. It didn't look significantly better than my
PyCharm setup, which is configured to launch the VLC mp4 viewer.
Defer VSCode for now.
