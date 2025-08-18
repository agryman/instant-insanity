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

### Other Dependencies

For generating videos:

```shell
brew install ffmpeg
```
Other Python dependencies:

```shell
pip install networkx shapely matplotlib scipy pytest mypy
```
For voiceovers:

```shell
pip install "manim-voiceover[azure,gtts]"
```

```shell
brew install portaudio
pip install pyaudio
```

```shell
brew install sox
```

For translations of voiceovers:

```shell
brew install gettext
```

For Google Cloud Platform TTS:

```shell
pip install google-cloud-texttospeech
```

## PyCharm

Sometimes PyCharm loses the project configuration.
I believe this is possibly associated with branch creation.
When this happens, run the menu command to recreate the project configuration.
Run the menu command `File -> Repair IDE` or `File -> Invalidate Caches...`.

The repair tactic no longer works.
The code editor fails to resolve Python objects contained
in the modules I import, which are present in the venv.
I reported this bug:
* 2025-07-14 PyCharm is unusable: https://youtrack.jetbrains.com/issue/PY-82615/PyCharm-code-editor-fails-to-find-packages-installed-in-my-virtual-environment

I found the cause of the problem. 
I had moved my Manim examples directory named `manim` to the top level under
my `src` folder, which made it a package named `manim`. This conflicted
with the Manim CE package named `manim`.
The PyCharm editor found my `manim` first and stopped searching for references.
The Python runtime kept searching and found the Manim CE objects.
The lesson learned is to avoid using `manim` as a directory name in your Python
source directory.

TODO: Create a gist and post it to the Discord discussion:
https://discord.com/channels/581738731934056449/1019649969596153968/threads/1395943742925443174

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

### Manim Bugs

#### Cairo does not respect order of mobjects when rendering a 3d scene #4336

I hit a bug in the Cairo renderer for 3d scenes.
See https://github.com/ManimCommunity/manim/issues/4336

The OpenGL renderer works so use it for 3D scenes.
Use Cairo for 2d scenes.

### Manim Workarounds

I hit a couple of bugs using 3D scenes and OpenGL.
In order to produce something, I am going to avoid those and instead
restrict my use of Manin to Scene and the Cairo renderer.

I make limited use of 3D content, namely to show the cubes, the cubes rotating,
and the cubes unfolding into a net.
I can simulate 3D by using orthographic projection, converting the cube faces into
Polygon objects.
All the resulting polygons are convex so it should be possible to sort them into
a correctly-ordered set in which any polygon that is obscured by another one is drawn
before it.
This boils down to creating a directed graph of convex polygons in which an edge
from polygon X to polygon Y means that polygon X must be drawn before polygon Y.
I then need to perform a 
[topological sort
](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_sort.html) 
on this graph, say using 
[NetworkX](https://networkx.org/).
