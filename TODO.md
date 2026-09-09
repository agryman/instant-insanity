# TODO List
*Arthur Ryman, last updated 2026-09-08*

* Fix import of scene into instant_insanity_core/demos/cube_lables_demo.py


Refactor the source code into the following packages.

* instant_insantity_scenes - the scenes specific to the Instant Insanity video
* instant_insantity_core - the modules that model Instant Insanity objects such as cubes, puzzles, and graphs
* kwargs_xyz_studio - the branding specific to the kwargs.xyz organization
* kwargs_xyz_core - generally useful code that is not specific to Instant Insanity
* manim_cairo3d - code used to achieve 3d animation in the main Cairo renderer

The refactoring will be implemented in two phase:
1. refactor the code in the agryman.instant-insanity repo
2. move packages into new kwargs-xyz repos

## Phase 1: Refactor agryman.instant-insanity repo

Use the following package directory structure in agryman.instant-insanity:

* /src
  * /instant_insanity_core
  * /instant_insanity_scenes
  * /kwargs_xyz_core
  * /kwargs_xyz_studio
  * /manim_cairo3d

## Phase 2: Move selected refactored code into new public kwargs-xyz repos

My goal is to publish as much code as possible in the kwargs-xyz organization using 
the MIT licence which allows redistribution.

I will initially keep the instant_insantity_scenes package as private in the agryman account, 
mainly because it contains some images that I copied from other websites. I don't have permission
to redistribute some of those images.

I will then move the public packages into new repositories in the kwargs-xyz organisation.
For simplicity of bookkeeping, I will create one repo for each package as follows:

* kwargs-xyz.instant-insanity-core
* kwargs-xyz.manim-core
* kwargs_xyz.manim-cairo3d
* kwargs-xyz.studio
