# Architecture of the Python Code for the Instant Insanity Video
*Arthur Ryman, last updated 2026-09-08*

The code for the Instant Insanity video began as a private Python repo 
named `agryman/instant-insanity`.
My plan was to make the code public after I submitted the video to [SoME5](https://some.3b1b.co/).

However, the video uses some images that I do not have permission to
redistribute under the MIT Licence.
I'd have to request permission from the copyright holders, or replace the images
with ones I create in order to make all the scenes public.

I am going to move forward by publishing the code that falls under the MIT Licence.
I'll work on the image problem later.

I decided to create a new GitHub organization named `kwargs-xyz` to host the published
code.

I decided to split the code into the following Python packages:

| Repo                             | Package                 | Description                            |
|----------------------------------|-------------------------|----------------------------------------|
| agryman/instant-insanity         | instant_insanity_scenes | video scenes                           |
| kwargs-xyz/instant-insanity-core | instant_insanity_core   | cubes, puzzles, graphs, solvers        |
| kwargs-xyz/manim-cairo3d         | manim_cairo3d           | projections, depth sort, 3d polygons   |
| kwargs-xyz/core                  | kwargs_xyz_core         | text-to-speech, image zoom, voiceovers |
| kwargs-xyz/studio                | kwargs_xyz_studio       | logo, branding                         |

## instant_insanity_scenes

The top-level package is `instant_insantity_scenes`. 
It contains manim scenes.
Most scenes contain animations and voiceovers.

This package MAY import any other package.
It MUST NOT be imported by any of the other packages.
No scene MAY import any other scene.
Any code not specific to one scene MUST be moved into another package.

The scenes are divided into two subpackages named `some5` and `outtakes`.
Scenes that were used in the video submitted to SoME5 are in the `some5` subpackage.
Scenes that were not used in the submitted video are in `outtakes` subpackages. 
These used scenes might appear in a future video.

Every scene module MUST contain code that renders the scene when the module is invoked as the main module.

## instant_insanity_core

The `instant_insantity_core` package contains code specific to Instant Insanity.
These include a puzzle solver, puzzle specifications, and manim objects for rendering cubes, puzzles, and opposite-face graphs.

This package MAY import any package except `instant_insantity_scenes`.
It SHOULD be imported by scenes in the `instant_insanity_scenes` package.

All modules MUST contain code that demonstrates the use of the module.
The demo code MUST run when the module is invoked as the main module.

## manim_cairo3d

The `manim_cairo3d` package contains general purpose code for rendering 3d scenes using the Cairo renderer.
This includes perspective and orthographic projections, a depth-sort algorithm, and lists of 3d convex polygons.

This package MUST NOT import any of the other packages.

## kwargs_xyz_core

The `kwargs_xyz_core` package contains code that is generally useful for creating manim animations.
This includes calling the Google Text-to-Speech service, and image zoom class, and helper functions for voiceovers.
This package MUST NOT contain any code that is specific to Instant Insanity.

This package MUST NOT import any of the other packages.

## kwargs_xyz_studio

The `kwargs_xyz_studio` package contains code for branding the `kwargs.xyz` organization.
At present, it just contains the logo.

This package MUST NOT import any of the other packages.

