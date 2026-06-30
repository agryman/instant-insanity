# Outline of Instant Insanity Video
*Arthur Ryman, last edited 2025-09-25*

This document outlines the contents of the Instant Insanity video.
It describes the main parts of the video and each of its scenes.

## Title Page

- A Puzzling Introduction to Graph Theory

## Part 1 - Introduction

- describe the goal of the puzzle
  - animate the cubes to give the solution and rotate it to show all sides
- explain that the puzzle is difficult to solve by trial and error
- an ingenious solution published in 1947 uses graph theory
- state that graph theory is very relevant, useful, and worth learning
- mention that Instant Insanity has been the subject of many papers and videos
- the goals of this video are:
  - to explain the graph theory solution using animation
  - and teach some graph theory in the process

## Part 2 - Combinatorics

- how difficult is it to find the solution?
- how many combinations of the cubes are there?
- the Instant Insanity box and two YouTube videos say 82,944
  - show the box and screenshots
  - Winning Solutions box
  - Robin Wilson, Gresham College video
  - Tai-Danae Bradley, PBS Infinite Series video (refers to Robin Wilson)
- the 1947 Eureka paper by Carteblanche says 41,472 
  - show the paper
- who's right?
- use the Carteblanche labelling of cubes and faces
- What do we mean by a combination?
- combinatorics is the branch of math that investigates how to count things
- show that each cube has 24 orientations
- compute $24^4$
- show that 4 cubes have 24 permuations
- compute $24^5$ = 7,962,624
- drawing the cubes at random from a bag gives 7,962,624 combinations
- if we permute a solution we get a solution
- explain that permuting the cubes does not count as a different solution
- there are 24 orders for 4 cubes so get 7,962,624/24 = 331,776 combinations
- fix an order for the cubes
- explain that the 4-fold rotations about the long axis does not produce new solutions
- if we rotate a solution by 90 degrees along the horizontal axis we get a solution
- get 331,776 / 4 = 82,944 combinations
- explain that the 2-fold rotations about the vertical axis does not produce new solutions
- if we rotate each cube in a solution by 180 degrees around the vertical axis we get a solution
- get 82,944 / 2 = 41,472 combinations

## Part 3 - Graph Theory

- explain the difference between the graph of a function and a graph
- say that a graph is a set of dots connected by lines
  - define graph terminology
  - simple graphs
  - directed graphs
  - labelled graphs
- show examples of why graphs are useful
  - London Tube map
  - rock-paper-scissors
  - Bridges of Konisberg
- discuss the opposite-face graph
  - show the search tree
  - discuss the Python code for searching
  - animate the search

## Part 4 - Closing

- say that graphs are very important in our digital society
- the Internet is a network of servers connected by digital links
- the Web is a network of pages connected by links
  - Google PageRank is a graph algorithm
- Facebook is a social network of people and linked by friend and follower relations
- AI is powered by artificial neural networks

## Part 5 - Epilogue

- Arthur was one of those teenagers that got fascinated by Instant Insanity
- He attended Northview Heights SS which had just installed an IBM 1130 computer
- Arthur wrote a Fortran program that did a brute-force search of 331,776 combinations and found 8 solutions
which were all essentially the same modulo rotations
- One day Prof. Ross Honsberger from U. Waterloo gave a lecture on Graph Theory where he used it to solve Instant Insanity
- Honsberger had previously been the head of the math department at Northview Heights
- Arthur was blown away by the elegance of the solution and showed it to whoever would listen

## Part 6 - History
- US Patent 646463 issued to Frederick A. Schossow, 1900-04-03
- state that an ingenious graph theory solution was discovered in 1947 by some Cambridge math students
- they were known as the Trinity Four
  - show an image of the Trinity Four
  - they wrote under the pseudonym Carteblanche
- Carteblanche was a group of Cambridge undergraduates known as the Trinity Four
- Bill Tutte was one of them
- In 1943 he was recruited to Bletchley Park and assigned to crack the Lorenz Cipher 
- Lorenz was much more difficult than Enigma, which was cracked by Alan Turing and stimulated the development
of the first digital computer
- Tutte returned to Cambridge and became an eminent graph theorist
- Tutte was probably the main author of the 1947 Eureka paper
- Tutte then moved to University of Toronto and then to University of Waterloo
- It is likely that Tutte showed the solution to Honsberger who showed it to Arthur who is showing it to you

## Acknowledgements
- Will, a fellow Northview Heights student became an animator and encouraged me the create this video.
  - He prototyped many animation scenes using Houdini and selected Google text-to-speech and the Aeode voice
- Grant Sanderson for creating manim and running the SoME event
- the Manim Community for maintaining and enhancing manim which I used to generate the animations
- Google Cloud Platform for providing the text-to-speech service and the Aeode voice
- Claude Code for being my tireless coding partner
