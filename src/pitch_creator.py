import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def pitch_plotter(size, alpha_pitch_boundaries, alpha_grid_lines):
    with plt.style.context("bmh"):
        fig = plt.figure(figsize=size)
        plt.axis([-5, 125, -10, 90])
        plt.grid(False)

        plt.plot([60, 60], [0, 80], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([120, 120], [0, 80], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([60, 120], [0, 0], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([60, 120], [80, 80], color="black", alpha=alpha_pitch_boundaries)

        plt.plot([0, 0], [0, 80], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([60, 60], [0, 80], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([0, 60], [0, 0], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([0, 60], [80, 80], color="black", alpha=alpha_pitch_boundaries)
        # add boxes to split into thirds
        plt.plot(
            [40, 40], [0, 80], color="black", linestyle="--", alpha=alpha_grid_lines
        )
        plt.plot(
            [80, 80], [0, 80], color="black", linestyle="--", alpha=alpha_grid_lines
        )

        plt.plot(
            [0, 120],
            [26.7, 26.7],
            color="black",
            linestyle="--",
            alpha=alpha_grid_lines,
        )
        plt.plot(
            [0, 120],
            [53.3, 53.3],
            color="black",
            linestyle="--",
            alpha=alpha_grid_lines,
        )

        centreCircle = plt.Circle((60, 40), 9.15, color="black", fill=False)

        # right penalty area
        plt.plot([120, 102], [18, 18], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([102, 102], [18, 62], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([102, 120], [62, 62], color="black", alpha=alpha_pitch_boundaries)

        # left penalty area
        plt.plot([0, 18], [18, 18], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([18, 18], [18, 62], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([18, 0], [62, 62], color="black", alpha=alpha_pitch_boundaries)

        # right six yard box
        plt.plot([120, 114], [30, 30], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([114, 114], [30, 50], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([114, 120], [50, 50], color="black", alpha=alpha_pitch_boundaries)

        # left six yard box
        plt.plot([0, 6], [30, 30], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([6, 6], [30, 50], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([6, 0], [50, 50], color="black", alpha=alpha_pitch_boundaries)

        # right goal posts
        plt.plot([120, 122], [36, 36], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([120, 122], [44, 44], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([122, 122], [36, 44], color="black", alpha=alpha_pitch_boundaries)

        # left goal posts
        plt.plot([0, -2], [36, 36], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([0, -2], [44, 44], color="black", alpha=alpha_pitch_boundaries)
        plt.plot([-2, -2], [36, 44], color="black", alpha=alpha_pitch_boundaries)

        # right Arc
        rightArc = Arc(
            (108, 40),
            height=18.3,
            width=18.3,
            angle=0,
            theta1=130,
            theta2=230,
            color="black",
        )

        # left Arc
        leftArc = Arc(
            (12, 40),
            height=18.3,
            width=18.3,
            angle=0,
            theta1=310,
            theta2=50,
            color="black",
        )

        ax = plt.gca()
        ax.add_patch(centreCircle)
        ax.add_patch(rightArc)
        ax.add_patch(leftArc)

        ax.set_ylim(ax.get_ylim()[::-1])
        return fig
