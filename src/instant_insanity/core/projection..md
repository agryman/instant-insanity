# Projections

This document gives a precise, mathematical specification of projections.
Projections let us draw 3d objects on 2d screens.

Implementing projections will let us draw simple 3d scenes in Manim
using the `Scene` class and the Cairo renderer.

Although work is underway to finalize the OpenGL renderer for use with the `ThreeDScene` class,
the majority of our planned content is 2d so using the `Scene` class is attractive.

## Model Space

Let $S = \mathbb{R}^3$ denote the 3d model space.
Model space is where our simple 3d objects live.

Let $x, y, z$ be the usual Cartesian coordinates on model space.

We will use the default Manim orientation of model space relative to the display screen, 
namely x increases from left to right,
y increases from bottom to top, 
and z increases from in (back) to out (front).

## The Camera Plane 

Let $C \subset S$ denote the camera plane in model space.
The camera plane is where we will draw the 2d projections of 3d objects.
The camera plane itself will be mapped to the display screen but the Manim Scene class
handles that.

The camera plane is oriented parallel to the plane z = 0.
Let $c \in \mathbb{R}$ be a real number that defines the camera plane 
given by the equation $z = c$.

$$
C = \{~(x, y, c) \mid (x, y) \in \mathbb{R}^2~\}
$$

## Projections

Our goal is to draw 3d objects that live in model space $S$ as 2d objects on the camera plane $C$.
However, we need to draw the 2d objects in the right order to achieve the correct appearance.
If object A is behind object B in model space then we need to draw the 2d projection
of object A before we draw that of object B.

For simplicity, we will assume that 3d objects can be modelled as sets of opaque, convex, planar
polygons so that we can always draw their 2d projections in the right order.

A projection 
$P: S \rightarrow C \times \mathbb{R}$
is a pair of functions $(p, t)$
where $p$ maps model space to the camera plane
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

A perspective projection models the way we see things in the sense that
objects that are further away appear smaller and parallel lines converge.

A perspective projection is defined by giving a viewpoint $V \in S$.
The viewpoint represents the position of our eyes.

Treat $V$ as a fixed parameter in what follows.

Let $L(M) \subset S$ be the line in model space that passes through $M$ and $V$.
The projection $p(M)$ is the unique point where this line intersects the camera plane.

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

The line $L(M)$ has the following equation in terms of the real
parameter $\lambda$:
$$
L(M, \lambda) = p(M) + \lambda \hat{u}(M)
$$
With this parameterization, we can think of the line as being directed from
$M$ to $V$.

In terms of coordinates, we have:
$$
L(M,\lambda) = (x + \lambda u_x, y + \lambda u_y, c + \lambda u_z)
$$

By construction, the parameter value $\lambda = 0$ corresponds to the point $p(M)$.
$$
L(M, 0) = p(M)
$$

By construction, the parameter value $\lambda = \lVert V - M \rVert$ corresponds to the point $V$.
$$
L(M, \lVert V - M \rVert) = V
$$

Define $t(M)$ to be the parameter value that corresponds to the point $M$.
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

Clearly, as $\mu$ becomes very large $V(\mu) - M$ is dominated by $\mu \hat{v}$.
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