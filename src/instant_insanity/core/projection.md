# Projections

A projection is a mapping from 3d space to 2d space.
Projections let us draw 3d objects on 2d screens.
This document gives a precise, mathematical specification of projections.

Implementing projections will let us draw simple 3d scenes in Manim
using the `Scene` class and the Cairo renderer.

Although work is underway to produce a high-quality OpenGL renderer for use with the `ThreeDScene` class,
the majority of our planned content is 2d so using Cairo with the `Scene` class
is an acceptable short-term workaround.

## Model Space

Let $S = \mathbb{R}^3$ denote the 3d model space.
Model space is where our simple 3d objects live.

Let $x, y, z$ be the usual Cartesian coordinates on model space.

We will use the default Manim orientation of model space relative to the display screen, 
namely:
* x increases from left to right,
* y increases from bottom to top, and 
* z increases from in (back) to out (front).

## The Camera Plane 

Let $C$ denote the camera plane in model space.
The camera plane is where we will draw the 2d projections of 3d objects.
The points in the camera plane get mapped to the pixels of the 
display screen by the Manim `Scene` class.

The camera plane is oriented parallel to the plane z = 0.
Let $c$ be a real number that defines the camera plane 
as the solutions to the equation $z = c$.

$$
C = \{~(x, y, c) \mid (x, y) \in \mathbb{R}^2~\}
$$

## Projections

Our goal is to draw 3d objects that live in model space $S$ as 2d objects on the camera plane $C$.
However, we need to draw the 2d projections of our 3d objects in the correct order to achieve the correct appearance.
If object A is behind object B in model space then we need to draw the 2d projection
of object A before we draw that of object B. 
This procedure is known as the [Painter's Algorithm](https://en.wikipedia.org/wiki/Painter%27s_algorithm).

For simplicity, we will assume that our 3d objects can be modelled as collections of opaque, convex, planar
polygons and that we can always sort them into some drawing order that will produce the correct visual appearance.

Note that it is possible to arrange three nonintersecting, convex, 
planar polygons in a way that has no corresponding correct drawing order.

Given the known requirements for our current project, 
all collections of 3d objects will be simple enough so that a correct
drawing order always exists.

If we actually needed to draw some collection of polygons that had no correct drawing order,
then we would have to split some of the polygons.
If we split the polygons enough then a correct drawing order always exists.
In the extreme case, we could split each polygon into individual pixels.
We'll defer dealing with this situation until project requirements force us to do so.


A projection 
$P: S \rightarrow C \times \mathbb{R}$
is a pair of functions $(p, t)$
where $p$ maps the model space to the camera plane
$$
p: S \rightarrow C 
$$
and $t$ maps model space to the real numbers
$$
t: S \rightarrow \mathbb{R}
$$

The function $t$ preserves the relative visibility of distinct
points in model space that map to the same point in the camera plane.
Let $M_1$ and $M_2$ be distinct points in model space that project to the same
point in the camera plane
$$p(M_1) = p(M_2)$$
Suppose that $M_1$ is behind $M_2$.
Denote this as
$$ M_1 \prec M_2$$
Then their $t$ values must satisfy
$$t(M_1) < t(M_2)$$

There are two commonly used projections, namely perspective and orthographic.
These will be defined next.

## Perspective Projection

A perspective projection models the way we see things.
Objects that are further away appear smaller and parallel lines converge.

A perspective projection is defined by giving a viewpoint $V \in S$.
The viewpoint represents the position of our eyes.

Treat $V$ as a fixed parameter in what follows.
Consider points $M$ that are distinct from $V$.
If $M = V$ then its projection is not defined.

Let $L(M)$ be the line in model space that passes through the points $M$ and $V$.
This line exists because we have assumed that $M \ne V$.
Think of $L(M)$ as a light ray that leaves the 3d object at $M$ and enters our eye at $V$.
The projection $p(M)$ is the unique point where the light ray intersects the camera plane.

$$
L(M) \cap C = \{ p(M) \}
$$

Therefore,
$$
p(M) = (x, y, c)
$$
where $x, y$ are unknowns that we have to compute.

Let $\hat{u}(M)$ denote the unit vector that points from $M$ to $V$.
$$
\hat{u}(M) = \frac{V - M}{\lVert V - M \rVert}
$$

Let $\hat{u}(M)$ have the following components:
$$
\hat{u}(M) = (u_x, u_y, u_z)
$$

Define $L(M,\lambda)$ to be the point on $L(M)$ corresponding to the
real parameter $\lambda$ as follows:
$$
L(M, \lambda) = p(M) + \lambda \hat{u}(M)
$$
With this parameterization, we can think of the line as being directed from
$M$ to $V$.

In terms of coordinates, we have:
$$
L(M,\lambda) = (x + \lambda u_x, y + \lambda u_y, c + \lambda u_z)
$$

By construction, the parameter value $\lambda = 0$ maps to the point $p(M)$.
$$
L(M, 0) = p(M)
$$

By construction, the parameter value $\lambda = \lVert V - M \rVert$ maps to the point $V$.
$$
L(M, \lVert V - M \rVert) = V
$$

Define $\lambda = t(M)$ to be the parameter value that maps to the point $M$.
$$
L(M, t(M)) = M
$$

Let $M$ have the following components:
$$
M = (m_x, m_y, m_z)
$$

In terms of coordinates, we have
$$
(x + t(M) u_x, y + t(M) u_y, c + t(M) u_z) = (m_x, m_y, m_z)
$$

Now solve for $t(M), x, y$ as follows:
$$
\begin{align}
t(M) &= \frac{m_z - c}{u_z} \\
x &= m_x - t(M) u_x \\
y &= m_y - t(M) u_y
\end{align}
$$

## Orthographic Projection

An orthographic projection is a limiting case of a perspective projection as
the viewpoint $V$ moves off to infinity in a fixed direction.
Let $\hat{v}$ be a unit vector that defines the direction that the viewpoint moves in.
Let $\mu$ be a real parameter and define $V(\mu)$ as follows:
$$
V(\mu) = V + \mu \hat{v}
$$

Define $\hat{u}(M, \mu)$ to be the unit vector that points from $M$ to $V(\mu)$.
$$
\hat{u}(M, \mu) = \frac{V(\mu) - M}{\lVert V(\mu) - M \rVert}
$$

Clearly, as $\mu$ becomes very large, 
$V(\mu)$ approaches $\mu \hat{v}$.
$$
\begin{align}
\lim_{\mu \to \infty} \hat{u}(M, \mu) 
&= \lim_{\mu \to \infty} \frac{V(\mu) - M}{\lVert V(\mu) - M \rVert} \\
&= \lim_{\mu \to \infty} \frac{V + \mu \hat{v} - M}{\lVert V + \mu \hat{v} - M \rVert} \\
&= \lim_{\mu \to \infty} \frac{\mu \hat{v}}{\lVert \mu \hat{v} \rVert} \\
&= \lim_{\mu \to \infty} \frac{\mu \hat{v}}{\mu \lVert \hat{v} \rVert} \\
&= \hat{v}
\end{align}
$$

Therefore, an orthographic projection is like a perspective projection except that
rather than compute the unit vector $\hat{u}(M)$ we use the given constant unit vector $\hat{v}$.