# PolygonToDotAnimation

The purpose of this animation is to smoothly morph a `Polygon` into a `Dot`.
For simplicity, we'll assume that the polygon is convex since that is all we require for our current
purposes.

The built-in Manim `Transform` animation simply morphs the polygon path into the dot path.
Unfortunately, this simple rule may result in visual anomalies.
The polygon path may start at any angle with respect to its centre and have either clockwise or
counterclockwise orientation.
* First, if the orientation of the polygon is opposite to that of the dot then the polygon appears to
twist.
* Second, if the starting vertex of the polygon path is not at zero degrees, then the poly appears to
rotate.

While these may seem like minor nuances, they are visually distracting, and we may be able to resolve
them with a relatively small effort.

An ideal animation would have the following properties:
* the centre of the polygon should morph linearly to the centre of the dot
* points on the boundary of the polygon should morph radially with respect to the polygon centre until
they become the corresponding points on the boundary of the dot, i.e. their angles with respect to the
centres does not change
* the final result should be a polygon whose shape smoothly approximates a circle, i.e. we should
add enough new vertices to the initial polygon so that the final polygon looks like a circle

The algorithm is as follows:

Input: 
* v, the vertex path of a convex polygon
* theta_min, the minimum angle between points on the vertices of the dot
Output:
* w, the refined vertex path of the polygon centered on the origin
Algorithm
* force v to be oriented ccw 
* set n = len(v)
* compute c, the centre of v 
* compute v_0 = v - c, the list of relative $(x,y)$ coordinates. None of v_0 will be $(0,0)$ since are 
assuming that the polygon is convex.
* compute theta, the list of angles corresponding to xy_0.
* set w to be an empty list
* append v_0[0] to w
* build up the points in w by refining each sector i in range(n) as follows
  * set v0 = v_0[i]
  * set v1 = v_0[0] if i == n - 1 else v_0[i + 1]
  * compute the sector angle, delta_theta, for sector i which starts at v0 and goes to v1
  * if delta_theta <= theta_min then no need to refine
    * append v1 to w
  * else refine the sector as follows
    * N = ceiling(theta_min / delta_theta)
    * by construction, N > 1
    * set u = v1 - v0, this vector points from v0 to v1
    * set wk = v0
    * for k in range(N)
      * wk = wk + u
      * append wk to w
  * at this point w contains the refinement of v_0
  * translate w back to the actual position of v, w = w + c

We now have enough points in w to make a smooth circle.

To animate the process, we need to both translate the centre of the polygon to the centre of the
dot, and scale the radial position of each vertex relative to its centre.

Let C be the centre of the dot and let R be its radius.
Let w_0[i] be vertex i of the refined vertex path.
To compute w at animation stage alpha, do the following.

* c_alpha = c + (C - c) * alpha
* r_alpha[i] = r[i] + (R - r[i] * alpha)
* w_alpha[i] = r_alpha[i] * (cos(theta_w[i], sin(theta_w[i])) + c_alpha

