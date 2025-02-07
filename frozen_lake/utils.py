import json
import os
import pandas as pd
import matplotlib.pyplot as plt


def custom_step(env, agent, action, observation):
    obs, r, terminated, truncated, info = env.step(action)
    agent.add_record(observation, action)
    if r == 0:
        if terminated:
            r = -1  # Lake
        elif obs == observation:
            r = -0.1  # Don't move (hitting the wall)
        # else:
        #     r = -0.01  # Each step has a cost
        #     # r=0
    agent.episode.append([int(observation), int(action), float(r)])
    return obs, r, terminated, truncated, info


def score(episodes):
    return pd.DataFrame(
        [
            {
                "Episode": i + 1,
                "Length": len(episode),
                "Score": sum(ele[2] for ele in episode),
                "Success": 1 if int(episode[-1][2]) == 1 else 0,
            }
            for i, episode in enumerate(episodes)
        ]
    )


def plots(episodes, title, save=False):

    # Compute cumulative mean score
    episodes["Cumulative_Mean_Score"] = episodes["Score"].expanding().mean()

    # Create the figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
    fig.suptitle("Episode Analysis " + title, fontsize=14, fontweight="bold")

    # 1️⃣ Plot of scores per episode
    axes[0, 0].plot(
        episodes["Episode"],
        episodes["Score"],
        marker="o",
        linestyle="-",
        color="blue",
        label="Score",
    )
    axes[0, 0].set_ylabel("Score")
    axes[0, 0].set_title("Score per Episode")
    axes[0, 0].grid(True)
    axes[0, 0].legend()

    # 2️⃣ Plot of cumulative mean score (highlight transition at 0)
    crossing_idx = (episodes["Cumulative_Mean_Score"] > 0).idxmax()
    crossing_episode = (
        episodes.loc[crossing_idx, "Episode"]
        if (episodes["Cumulative_Mean_Score"] > 0).any()
        else None
    )

    axes[0, 1].plot(
        episodes["Episode"],
        episodes["Cumulative_Mean_Score"],
        marker="o",
        linestyle="-",
        color="orange",
        label="Cumulative Mean",
    )
    axes[0, 1].axhline(
        0, color="black", linestyle="--", linewidth=1
    )  # Ligne horizontale à y=0

    # Ajouter un marqueur et une annotation si un croisement existe
    if crossing_episode:
        axes[0, 1].scatter(
            crossing_episode, 0, color="red", zorder=3
        )  # Point rouge au croisement
        axes[0, 1].annotate(
            f"Crosses 0 at Episode {crossing_episode}",
            (crossing_episode, 0),
            textcoords="offset points",
            xytext=(-20, 10),
            ha="center",
            fontsize=10,
            color="red",
        )

    axes[0, 1].set_ylabel("Cumulative Mean Score")
    axes[0, 1].set_title("Cumulative Mean Score Over Episodes")
    axes[0, 1].grid(True)
    axes[0, 1].legend()

    # 3️⃣ Episode length with color based on success
    colors = episodes["Success"].map(
        {1: "green", 0: "red"}
    )  # Green if success, red otherwise
    success_rate = episodes["Success"].mean() * 100
    label = f"Episode Length: {episodes['Length'].mean()}\nSuccess Rate: {success_rate:.1f}%"
    axes[1, 0].bar(episodes["Episode"], episodes["Length"], color=colors, label=label)
    axes[1, 0].set_ylabel("Length")
    axes[1, 0].set_title("Episode Length (Green = Success, Red = Failure)")
    axes[1, 0].grid(True)
    axes[1, 0].legend(loc="upper right")

    # 4️⃣ Score/Length ratio
    axes[1, 1].plot(
        episodes["Episode"],
        episodes["Score"] / episodes["Length"],
        marker="o",
        linestyle="-",
        color="purple",
        label="Score/Length",
    )
    axes[1, 1].set_xlabel("Episode")
    axes[1, 1].set_ylabel("Score / Length")
    axes[1, 1].set_title("Score-to-Length Ratio per Episode")
    axes[1, 1].grid(True)
    axes[1, 1].legend()

    # Show the plots
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    title_ = os.path.join(os.path.join("frozen_lake", "results"), title)

    if save:
        plt.savefig(title_ + ".png")
    else:
        plt.show()
    plt.close()
    # return agent, score_mean, length_mean, success_rate, score-length_mean, first episode with positive cumulative mean
    score_length = episodes["Score"] / episodes["Length"]
    return (
        title,
        episodes["Score"].mean(),
        episodes["Length"].mean(),
        success_rate,
        score_length.mean(),
        crossing_episode,
    )


def save_results(score_agents, allrecord_results):
    df = pd.DataFrame(
        score_agents,
        columns=[
            "Agent",
            "Score",
            "Length",
            "Success",
            "Score/Length",
            "Cumulative mean above 0",
        ],
    )

    df = df.fillna(-1).round(5).to_dict(orient="records")
    df_json = sorted(
        df,
        key=lambda x: (
            x["Cumulative mean above 0"] == -1,
            x["Cumulative mean above 0"],
        ),  # The faster the mean goes above 0 the better the agent is
    )
    title1 = os.path.join(os.path.join("frozen_lake", "results"), "agents_results.json")
    with open(title1, "w") as f:
        json.dump(df_json, f, indent=4)

    dfs_json = [df.to_dict(orient="records") for df in allrecord_results]
    title2 = os.path.join(
        os.path.join("frozen_lake", "results"), "all-record_results.json"
    )
    with open(title2, "w") as f:
        json.dump(dfs_json, f, indent=4)
    return title1, title2
