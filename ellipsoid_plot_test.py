import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from plot_helpers.covariance_ellipse import CovarianceEllipsoids3D
from scipy.stats import invwishart
from plot_helpers.axes_equal import axes_equal
from matplotlib.animation import FuncAnimation

# Create some multivariate data
mean = np.array([0, 0, 0])
Psi = 1 * np.eye(3)
cov = invwishart.rvs(size=1, df=5, scale=Psi)
pp = np.random.multivariate_normal(mean, cov, size=1000)

# Simple static plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(pp[:, 0], pp[:, 1], pp[:, 2], color="r")
ell = CovarianceEllipsoids3D(ax, mean, cov, edgecolor="none", color="g")
axes_equal(ax)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")


# Animated 3D plot
class CovarianceAnimator:
    def __init__(self, points, n_start=5) -> None:
        self.points = points
        self.n_frames = points.shape[0] - n_start
        self.n_start = n_start
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        axes_equal(self.ax, points)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        self._artists = []
        self._artists.append(
            self.ax.scatter(
                self.points[:n_start, 0],
                self.points[:n_start, 1],
                self.points[:n_start, 2],
                color="r",
            )
        )

        mu, cov = self._get_mean_cov(n_start)
        self._ellipses = CovarianceEllipsoids3D(self.ax, mu, cov, color="b")
        self._artists.extend(self._ellipses.get_artists())

        # Precalculate everything!
        print("Calculating means and covs...")
        self._means = []
        self._covs = []
        for i in range(self.n_frames):
            mu, cov = self._get_mean_cov(i + self.n_start)
            self._means.append(mu)
            self._covs.append(cov)
        print("Done.")

    def update(self, i):
        self._artists[0]._offsets3d = (
            self.points[: (self.n_start + i), 0],
            self.points[: (self.n_start + i), 1],
            self.points[: (self.n_start + i), 2],
        )
        self._ellipses.update(self._means[i], self._covs[i])
        self._artists[1:] = self._ellipses.get_artists()
        return self._artists

    def init(self):
        return self.update(0)

    def _get_mean_cov(self, n=None):
        if n is None:
            n = self.points.shape[0]
        return np.mean(self.points[:n], axis=0), np.cov(self.points[:n], rowvar=False)


ellipse_animator = CovarianceAnimator(pp)
ani = FuncAnimation(
    ellipse_animator.fig,
    ellipse_animator.update,
    frames=ellipse_animator.n_frames,
    repeat=True,
)

plt.show()
