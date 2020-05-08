import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Arc
from pprint import pprint

# function to get length and angle frequencies
def frequencies(df, parameters, nbins=20):
    for par in parameters:
        n, bins, _ = plt.hist(df[par].values, bins=nbins)

        norm_n_values = n / max(n)

        norm_n_bin_dict = dict(zip(range(20), norm_n_values))

        par_bin_map = pd.cut(df[par], bins, labels=False, retbins=True, right=False)

        col_name_bin = par + "_bin"

        df[col_name_bin] = par_bin_map[0].values

        par_frequency = []

        df = df.fillna(nbins - 1)

        for _, row in df.iterrows():
            par_frequency.append(norm_n_bin_dict[int(row[col_name_bin])])

        col_name_freq = par + "_frequency"

        df[col_name_freq] = par_frequency

    return df


# function to filter data into boxes
def box_split(df):
    # box1
    filtx_box1 = df.start_X < 40
    filty_box1 = df.start_Y < 26.7
    filt_box1 = filtx_box1 & filty_box1
    # box2
    filtx1_box2 = df.start_X > 40
    filtx2_box2 = df.start_X < 80
    filty_box2 = df.start_Y < 26.7
    filt_box2 = filtx1_box2 & filtx2_box2 & filty_box2
    # box3
    filtx_box3 = df.start_X > 80
    filty_box3 = df.start_Y < 26.7
    filt_box3 = filtx_box3 & filty_box3
    # box4
    filtx_box4 = df.start_X < 40
    filty1_box4 = df.start_Y > 26.7
    filty2_box4 = df.start_Y < 53.3
    filt_box4 = filtx_box4 & filty1_box4 & filty2_box4
    # box5
    filtx1_box5 = df.start_X > 40
    filtx2_box5 = df.start_X < 80
    filty1_box5 = df.start_Y > 26.7
    filty2_box5 = df.start_Y < 53.3
    filt_box5 = filtx1_box5 & filtx2_box5 & filty1_box5 & filty2_box5
    # box6
    filtx_box6 = df.start_X > 80
    filty1_box6 = df.start_Y > 26.7
    filty2_box6 = df.start_Y < 53.3
    filt_box6 = filtx_box6 & filty1_box6 & filty2_box6
    # box7
    filtx_box7 = df.start_X < 40
    filty_box7 = df.start_Y > 53.3
    filt_box7 = filtx_box7 & filty_box7
    # box8
    filtx1_box8 = df.start_X > 40
    filtx2_box8 = df.start_X < 80
    filty_box8 = df.start_Y > 53.3
    filt_box8 = filtx1_box8 & filtx2_box8 & filty_box8
    # box9
    filtx_box9 = df.start_X > 80
    filty_box9 = df.start_Y > 53.3
    filt_box9 = filtx_box9 & filty_box9

    df_1 = df[filt_box1]
    df_2 = df[filt_box2]
    df_3 = df[filt_box3]
    df_4 = df[filt_box4]
    df_5 = df[filt_box5]
    df_6 = df[filt_box6]
    df_7 = df[filt_box7]
    df_8 = df[filt_box8]
    df_9 = df[filt_box9]

    return [df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9]


# plot pitch and sonar


def plot_sonar(
    main_df,
    list_of_sub_df,
    player_name,
    parameter,
    alpha_pitch_boundaries,
    alpha_grid_lines,
    figsize,
):
    fig, (ax1) = plt.subplots(figsize=figsize)

    font_dict1 = {"fontsize": 20, "verticalalignment": "baseline"}
    font_dict2 = {"fontsize": 13}

    ax1.axis([-5, 125, -10, 90])
    ax1.grid(False)

    ax1.plot([60, 60], [0, 80], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([120, 120], [0, 80], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([60, 120], [0, 0], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([60, 120], [80, 80], color="black", alpha=alpha_pitch_boundaries)

    ax1.plot([0, 0], [0, 80], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([60, 60], [0, 80], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([0, 60], [0, 0], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([0, 60], [80, 80], color="black", alpha=alpha_pitch_boundaries)
    # add boxes to split into thirds
    ax1.plot([40, 40], [0, 80], color="black", linestyle="--", alpha=alpha_grid_lines)
    ax1.plot([80, 80], [0, 80], color="black", linestyle="--", alpha=alpha_grid_lines)

    ax1.plot(
        [0, 120], [26.7, 26.7], color="black", linestyle="--", alpha=alpha_grid_lines,
    )
    ax1.plot(
        [0, 120], [53.3, 53.3], color="black", linestyle="--", alpha=alpha_grid_lines,
    )

    centreCircle = plt.Circle((60, 40), 9.15, color="black", fill=False)

    # right penalty area
    ax1.plot([120, 102], [18, 18], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([102, 102], [18, 62], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([102, 120], [62, 62], color="black", alpha=alpha_pitch_boundaries)

    # left penalty area
    ax1.plot([0, 18], [18, 18], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([18, 18], [18, 62], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([18, 0], [62, 62], color="black", alpha=alpha_pitch_boundaries)

    # right six yard box
    ax1.plot([120, 114], [30, 30], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([114, 114], [30, 50], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([114, 120], [50, 50], color="black", alpha=alpha_pitch_boundaries)

    # left six yard box
    ax1.plot([0, 6], [30, 30], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([6, 6], [30, 50], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([6, 0], [50, 50], color="black", alpha=alpha_pitch_boundaries)

    # right goal posts
    ax1.plot([120, 122], [36, 36], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([120, 122], [44, 44], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([122, 122], [36, 44], color="black", alpha=alpha_pitch_boundaries)

    # left goal posts
    ax1.plot([0, -2], [36, 36], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([0, -2], [44, 44], color="black", alpha=alpha_pitch_boundaries)
    ax1.plot([-2, -2], [36, 44], color="black", alpha=alpha_pitch_boundaries)

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

    ax1 = plt.gca()
    ax1.add_patch(centreCircle)
    ax1.add_patch(rightArc)
    ax1.add_patch(leftArc)
    ax1.set_ylim(ax1.get_ylim()[::-1])
    ax1.text(
        0.5,
        0.925,
        "{} {} Sonars".format(player_name, parameter),
        horizontalalignment="center",
        transform=ax1.transAxes,
        fontdict=font_dict1,
    )
    ax1.axis("off")

    left1, bottom1, width1, height1 = [0.175, 0.61, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax2 = fig.add_axes([left1, bottom1, width1, height1], polar=True)

    ax2.bar(
        list_of_sub_df[0].angle.values,
        list_of_sub_df[0].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[0].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax2.axis("off")

    left2, bottom2, width2, height2 = [0.4125, 0.61, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax3 = fig.add_axes([left2, bottom2, width2, height2], polar=True)

    ax3.bar(
        list_of_sub_df[1].angle.values,
        list_of_sub_df[1].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[1].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax3.axis("off")

    left3, bottom3, width3, height3 = [0.66, 0.61, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax4 = fig.add_axes([left3, bottom3, width3, height3], polar=True)

    ax4.bar(
        list_of_sub_df[2].angle.values,
        list_of_sub_df[2].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[2].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax4.axis("off")

    left4, bottom4, width4, height4 = [0.175, 0.41, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax5 = fig.add_axes([left4, bottom4, width4, height4], polar=True)

    ax5.bar(
        list_of_sub_df[3].angle.values,
        list_of_sub_df[3].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[3].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax5.axis("off")

    left5, bottom5, width5, height5 = [0.4125, 0.41, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax6 = fig.add_axes([left5, bottom5, width5, height5], polar=True)

    ax6.bar(
        list_of_sub_df[4].angle.values,
        list_of_sub_df[4].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[4].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax6.axis("off")

    left6, bottom6, width6, height6 = [0.66, 0.41, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax7 = fig.add_axes([left6, bottom6, width6, height6], polar=True)

    ax7.bar(
        list_of_sub_df[5].angle.values,
        list_of_sub_df[5].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[5].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax7.axis("off")

    left7, bottom7, width7, height7 = [0.175, 0.2, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax8 = fig.add_axes([left7, bottom7, width7, height7], polar=True)

    ax8.bar(
        list_of_sub_df[6].angle.values,
        list_of_sub_df[6].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[6].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax8.axis("off")

    left8, bottom8, width8, height8 = [0.4125, 0.2, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax9 = fig.add_axes([left8, bottom8, width8, height8], polar=True)

    ax9.bar(
        list_of_sub_df[7].angle.values,
        list_of_sub_df[7].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[7].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax9.axis("off")

    left9, bottom9, width9, height9 = [0.66, 0.2, 0.2, 0.2]
    # ax2 = plt.subplot(212,projection='polar')
    ax10 = fig.add_axes([left9, bottom9, width9, height9], polar=True)

    ax10.bar(
        list_of_sub_df[8].angle.values,
        list_of_sub_df[8].angle_frequency.values,
        width=0.2,
        bottom=0.0,
        color=plt.cm.GnBu(list_of_sub_df[8].length.values / max(main_df.length.values)),
        alpha=1,
    )
    ax10.axis("off")

    left10, bottom10, width10, height10 = [0.4125, 0.175, 0.2, 0.01]
    ax11 = fig.add_axes([left10, bottom10, width10, height10])
    cmap = mpl.cm.GnBu
    norm = mpl.colors.Normalize(
        vmin=main_df.length.values.min(), vmax=main_df.length.values.max()
    )

    cb1 = mpl.colorbar.ColorbarBase(
        ax11,
        cmap=cmap,
        norm=norm,
        orientation="horizontal",
        boundaries=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90],
    )
    cb1.set_label("{} Distance".format(parameter), fontdict=font_dict2)
    plt.annotate(
        "Shard Length = {} Angle Frequency".format(parameter),
        xy=(0.9, 0.2),
        xytext=(1.2, 0.2),
    )
    plt.show()
