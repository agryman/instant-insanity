# Projections
*Arthur Ryman, lasted updated 2025-08-28*

A projection is a mapping from 3d space to 2d space.
Projections let us draw 3d objects on 2d screens.
This document gives a precise, mathematical specification of projections.

Implementing projections will let us draw simple 3d scenes in Manim
using the `Scene` class and the Cairo renderer.

Although work is underway to produce a high-quality OpenGL renderer for use with the `ThreeDScene` class,
the majority of our planned content is 2d so using Cairo with the `Scene` class
is an acceptable short-term workaround.

## Model Space

Let $M = \mathbb{R}^3$ denote the 3d model space.
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

Given any point $m$ in model space, we define its projection $\pi(m)$ onto the camera
plane by:
$$
\pi(m_x, m_y, m_z) = (m_x, m_y, c)
$$

Thus, $\pi$ maps $M$ onto $C$:
$$
\pi: M \rightarrow C
$$

The projection $\pi$ does nothing to the $(x,y)$-coordinates
and forgets the $z$-coordinate of points in $M$.

We need more sophisticated projections that give us the illusion of 3d scenes
but don't forget information so that we can invert them and compute the relative
ordering of model space points that project to the same camera plane points.
These are referred to as 3d projections, and they include perspective and orthographic
projections.

## Projections

Our goal is to draw 3d objects that live in model space $M$ as 2d objects on the camera plane $C$.
However, we need to draw the 2d projections of our 3d objects in the correct order to achieve the correct appearance.
If object A is behind object B in model space then we need to draw the 2d projection
of object A before we draw that of object B. 
This procedure is known as the 
[Painter's Algorithm](https://en.wikipedia.org/wiki/Painter%27s_algorithm).

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


A 3d projection 
$$f: M \rightarrow M$$
is linear transformation of model space that preserves $z$-coordinates.

Let $$m \in M$$ map to: $$f(m) = n \in M$$

Let $$m = (m_x, m_y, m_z)$$ 
and let 
$$f(m) = n = (n_x, n_y, n_z)$$
be its projection.
Then we require:
$$m_z = n_z$$ 
This means that the $z$-depth of the point hasn't changed,
only its $(x, y)$ coordinates.

Let $m$ and $m'$ be distinct points in model space that project to the same
point in the camera plane:
$$\pi(f(m)) = \pi(f(m'))$$

We say that $m$ and $m'$ are *collinear* with respect to $f$.

Suppose that $m$ is behind $m'$.
Denote this as:
$$ m \prec m'$$

We will define a real-valued $t_f$ function for $f$ 
$$ t_f: M \rightarrow \mathbb{R}$$
with the property that it respects
the relative ordering of collinear points in the sense that
their $t_f$ values must satisfy:
$$t_f(m) < t_f(m')$$

There are two commonly used 3d projections, namely perspective and orthographic.
These will be defined next.

## Perspective Projection

A perspective projection models the way we see things.
Objects that are further away appear smaller and parallel lines converge.

A perspective projection is defined by giving a viewpoint $v \in M$.
The viewpoint represents the position of our eyes.

Treat $v$ as a fixed parameter in what follows.
Consider points $m$ that are distinct from $v$.
If $m = v$ then the projection of $m$ is not defined.

Let $L(v;m)$ be the line in model space that passes through the points $m$ and $v$.
This line exists because we have assumed that $m \ne v$.

Think of $L(v;m)$ as a light ray that leaves the 3d object at 
$m$ and enters our eye at $v$.
The projection $f(v;m)$ is defined in terms of the unique point $b(v;m)$ where 
the light ray intersects the camera plane.

$$
L(v;m) \cap C = \{ b(v;m) \}
$$

Therefore,
$$
b(v;m) = (b(v;m)_x, b(v;m)_y, c)
$$
where $b(v;m)_x$ and $b(v;m)_y$ are unknown quantities that we have to compute.

Let $\hat{u}(v;m)$ denote the unit vector that points from $m$ to $v$.
$$
\hat{u}(v;m) = \frac{v - m}{\lVert v - m \rVert}
$$

Let $\hat{u}(v;m)$ have the following components:
$$
\hat{u}(v;m) = (u(v;m)_x, u(v;m)_y, u(v;m)_z)
$$

Define $L(v;m,\lambda)$ to be the point on $L(v;m)$ corresponding to the
real parameter $\lambda$ as follows:
$$
L(v;m, \lambda) = b(v;m) + \lambda \hat{u}(v;m)
$$
With this parameterization, we can think of the line as being directed from
$m$ to $v$.

In terms of coordinates, we have:
$$
L(v;m,\lambda) = (b(v;m)_x + \lambda u_x, b(v;m)_y + \lambda u_y, c + \lambda u_z)
$$

By construction, the parameter value $\lambda = 0$ maps to the point $b(v;m)$.
$$
L(v;m, 0) = b(v;m)
$$

By construction, the parameter value $\lambda = \lVert v - m \rVert$ 
maps to the point $v$.
$$
L(v;m, \lVert v - m \rVert) = v
$$

Define $t(v;m)$ to be the parameter value that maps to the point $m$.
$$
L(v;m, t(v;m)) = m
$$

In terms of coordinates, we have
$$
\begin{align}
b(v;m)_x + t(v;m) u_x &= m_x \\
b(v;m)_y + t(v;m) u_y &= m_y \\
c + t(v;m) u_z &= m_z
\end{align}
$$

Now solve for $t(v;m), b(v;m)_x, b(v;m)_y$ as follows:
$$
\begin{align}
t(v;m) &= \frac{m_z - c}{u_z} \\
b(v;m)_x &= m_x - t(v;m) u_x \\
b(v;m)_y &= m_y - t(v;m) u_y
\end{align}
$$

In summary, a viewpoint $v$ defines a 3d projection $f$ as follows:

$$
f(v;m) = (b(v;m)_x, b(v;m_y), m_z))
$$

Given $b(v;m)$, we can compute $m$ as follows:
$$
\begin{align}
t(v;m) &= \frac{m_z - c}{u_z} \\
m_x &= b(v;m)_x + t(v;m) u_x \\
m_y &= b(v;m)_y + t(v;m) u_y
\end{align}
$$

## Orthographic Projection

An orthographic projection is a limiting case of a perspective projection as
the viewpoint $v$ moves off to infinity in a fixed direction.
Let $\hat{u}$ be a unit vector that defines the direction that the viewpoint moves in.
Let $\mu$ be a real parameter, let $v_0$ be an initial viewpoint,
and define the viewpoint $v(\hat{u};\mu)$ as follows:
$$
v(\hat{u};\mu) = v_0 + \mu \hat{u}
$$

Define $\hat{u}(m; \mu)$ to be the unit vector that points from $m$ to $v(\mu)$.
$$
\hat{u}(m; \mu) = \frac{v(\hat{u};\mu) - m}{\lVert v(\hat{u};\mu) - m \rVert}
$$

Clearly, as $\mu$ becomes very large, 
$v(\hat{u};\mu)$ approaches $\mu \hat{v}$.
$$
\begin{align}
\lim_{\mu \to \infty} \hat{u}(m; \mu) 
&= \lim_{\mu \to \infty} \frac{v(\hat{u};\mu) - m}{\lVert v(\hat{u};\mu) - m \rVert} \\
&= \lim_{\mu \to \infty} \frac{v_0 + \mu \hat{u} - m}{\lVert v_0 + \mu \hat{v} - m \rVert} \\
&= \lim_{\mu \to \infty} \frac{\mu \hat{u}}{\lVert \mu \hat{u} \rVert} \\
&= \lim_{\mu \to \infty} \frac{\mu \hat{u}}{\mu \lVert \hat{u} \rVert} \\
&= \hat{u}
\end{align}
$$

Therefore, an orthographic projection is like a perspective projection except that
rather than compute the unit vector $\hat{u}(v;m)$ we use the given constant unit vector $\hat{u}$.

## Mapping from Model Space to Scene Scape

In practice, it is useful to not regard the camera as being embedded in scene space.
For example, the puzzle cubes have side length 2 which may be too big for the scene.
In this case allowing a scaling factor is handy.
Also, the objects in model space may appear to be shifted after applying a 3d projection.
In this case allowing a translation is handy.

We therefore allow the following mapping from model space to scene space which
we apply after the 3d projection. Let $o$ be a point in model space that will map to
the origin in scene space. The $\alpha$ be a real number scaling factor. The mapping $g$
from model space to space if given by:
$$
g(o,\alpha;m) = \alpha (m - o)
$$

The inverse is:
$$
g^{-1}(s) = o + s / \alpha
$$



