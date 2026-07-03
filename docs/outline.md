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

- Arthur was one of those teenagers that got hooked by Instant Insanity
- In 1967, he entered Northview Heights S.S. which had just acquired a new IBM 1130 computer
  - The 1130 was the first computer installed in a Canadian high school for educational purposes
- Arthur wrote a Fortran program for the 1130 to do a brute-force search of all 331,776 combinations 
  - the program found 8 solutions which were all related to each other by the rotations we discussed above
- One day in 1968 Prof. Ross Honsberger from U. Waterloo, Dept. of Combinatorics and Optimizatiobn,
gave a lecture on Graph Theory which ended with him showing how to use it to solve Instant Insanity
  - Honsberger had been the head of the math department at Northview Heights 1958-1963
- Arthur was blown away by the elegance of the solution and showed it to anyone who would listen
  - he found Graph Theory to be very useful throughout his career

## Part 6 - History
- in 1900 US Patent 646463 issued to Frederick A. Schossow, 1900-04-03
- in 1935 Bill Tutte entered Trinity College, Cambridge in 1935 where he became close friends with three other students 
  - they became known as the Trinity Four
  - show an image of the Trinity Four
  - they published recreational mathematical papers under the pseudonyms Blanche Descartes and Filet de Carteblanche
- in 1941, during the Second World War, he was recruited to break ciphers at Bletchley Park where Alan Turing had just cracked the Enigma cipher
  - Tutte was assigned to crack the much more difficult Lorenz cipher
  - this has been described as one of the greatest intellectual feats of World War II
- in 1944 the ability to decipher Lorenz saved the lives of thousands of Allied soldiers who took part in the Normandy Invasion,
  - one of those soldiers would become Arthur's father
- in 1945 Tutte returned to Cambridge to resume his graph theory research
- in 1947 Filet de Carteblanche published The Coloured Cubes Problem in Eureka, the Cambridge Mathematical Society journal. 
  The Coloured Cubes Problem is now called Instant Insanity. The paper presented the graph theory solution shown in this video.
- in 1948 Tutte moved to the Department of Mathematics, University of Toronto at the invitation of the great geometer Donald Coxeter
- in 1962 Tutte moved to the Department of Mathematics, University of Waterloo
- in 1967 Tutte helps found the Department of Combinatorics and Optimization
- in 1967 Ross Honsberger becomes a colleague of Bill Tutte in the newly formed Department of Combinatorics and Optimization
- in 1968 Ross Honsberger returns to Northview Heights S.S. and gives his lecture on Graph Theory and Instant Insanity
  - Tutte probably showed the solution to Honsberger, who showed it to Arthur, who is now showing it to you!

## Acknowledgements
- Will Anielewicz, who, after attending Northview Heights, went on to become a professional animator.
  - Will catalyzed Arthur into creating this video.
  - Will prototyped many animation scenes using Houdini in the formative stages of this project.
  - Will also dug into Google Cloud Text-to-Speech AI and selected the Aoede voice which is what you are listening to now.
- Grant Sanderson of 3blue1brown, for creating the manim mathematical animation Python package and for fostering the Summer of Math Exposition (SoME) event
- the Manim Community, for maintaining and enhancing manim which was used to generate all the animations
- Google Cloud Platform, for providing the Text-to-Speech service and the Aoede voice
- Claude Code, for being a tireless coding partner
