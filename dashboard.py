#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'UNCC MSOC 2023.csv')

# In[26]:


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/top_scorers')
def top_scorers():
    df = pd.read_csv(DATA_PATH)

    top_scorers = df[['Player Name', 'Total Goals', "Player's Role"]].sort_values(
        by='Total Goals', ascending=False).head(10)

    role_colors = {
        'ATTACKER': '#1f77b4',    # blue
        'MIDFIELDER': '#ff7f0e',  # orange
        'DEFENDER': '#2ca02c',    # green
        'GOALKEEPER': '#d62728'   # red (in case any show up)
    }

    bar_colors = [role_colors.get(role, '#7f7f7f') for role in top_scorers["Player's Role"]]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_scorers['Player Name'], top_scorers['Total Goals'], color=bar_colors)
    plt.xlabel('Total Goals')
    plt.title('Top 10 Goal Scorers - UNCC MSOC 2023')
    plt.gca().invert_yaxis()  # highest scorer on top

    legend_handles = [
        plt.Line2D([0], [0], color=color, lw=8, label=role)
        for role, color in role_colors.items()
        if role in top_scorers["Player's Role"].values
    ]
    plt.legend(handles=legend_handles, title="Player Role", loc='lower right')

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Top 10 Goal Scorers - UNCC MSOC 2023")

@app.route('/duels')
def duel_efficiency():
    df = pd.read_csv(DATA_PATH)

    df_clean = df[df["Duels Won %"] != '-'].copy()
    df_clean["Duels Won %"] = df_clean["Duels Won %"].astype(float)
    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df_clean = df_clean[df_clean["Player's Role"].isin(roles)]

    efficiency = df_clean.groupby("Player's Role")["Duels Won %"].mean().reset_index()
    efficiency["Duels Won %"] *= 100  

    team_avg = df_clean["Duels Won %"].mean() * 100  

    plt.figure(figsize=(6, 4))
    bars = plt.bar(efficiency["Player's Role"], efficiency["Duels Won %"], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Duel Win % by Field Position')
    plt.ylabel('Duel Win Percentage')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height + 1,
        f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

    plt.axhline(team_avg, color='red', linestyle='--', linewidth=1.5, label=f'Team Avg: {team_avg:.1f}%')
    plt.legend()

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Duel Win % by Field Position")

@app.route('/pass_accuracy')
def pass_accuracy():
    df = pd.read_csv(DATA_PATH)

    df_clean = df[df["Pass Accuracy %"] != '-'].copy()
    df_clean["Pass Accuracy %"] = df_clean["Pass Accuracy %"].astype(float)
    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df_clean = df_clean[df_clean["Player's Role"].isin(roles)]

    accuracy = df_clean.groupby("Player's Role")["Pass Accuracy %"].mean().reset_index()
    accuracy["Pass Accuracy %"] *= 100 

    team_avg = df_clean["Pass Accuracy %"].mean() * 100 

    plt.figure(figsize=(6,4))
    bars = plt.bar(accuracy["Player's Role"], accuracy["Pass Accuracy %"], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Pass Accuracy % by Field Position')
    plt.ylabel('Pass Accuracy (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 1, f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

    plt.axhline(team_avg, color='red', linestyle='--', linewidth=1.5, label=f'Team Avg: {team_avg:.1f}%')
    plt.legend()

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Pass Accuracy % by Field Position")

@app.route('/dribble_success')
def dribble_success():
    df = pd.read_csv(DATA_PATH)

    df_clean = df[df["Successful Dribbles %"] != '-'].copy()
    df_clean["Successful Dribbles %"] = df_clean["Successful Dribbles %"].astype(float)
    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df_clean = df_clean[df_clean["Player's Role"].isin(roles)]

    dribble = df_clean.groupby("Player's Role")["Successful Dribbles %"].mean().reset_index()
    dribble["Successful Dribbles %"] *= 100  

    team_avg = df_clean["Successful Dribbles %"].mean() * 100

    plt.figure(figsize=(6, 4))
    bars = plt.bar(dribble["Player's Role"], dribble["Successful Dribbles %"], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Dribble Success % by Field Position')
    plt.ylabel('Dribble Success (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height + 1,
        f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

    plt.axhline(team_avg, color='red', linestyle='--', linewidth=1.5, label=f'Team Avg: {team_avg:.1f}%')
    plt.legend()

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Dribble Success % by Field Position")

@app.route('/shot_accuracy')
def shot_accuracy():
    df = pd.read_csv(DATA_PATH)

    df_clean = df[df["Shot Accuracy %"] != '-'].copy()
    df_clean["Shot Accuracy %"] = df_clean["Shot Accuracy %"].astype(float)
    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df_clean = df_clean[df_clean["Player's Role"].isin(roles)]

    accuracy = df_clean.groupby("Player's Role")["Shot Accuracy %"].mean().reset_index()
    accuracy["Shot Accuracy %"] *= 100  

    team_avg = df_clean["Shot Accuracy %"].mean() * 100

    plt.figure(figsize=(6, 4))
    bars = plt.bar(accuracy["Player's Role"], accuracy["Shot Accuracy %"], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Shot Accuracy % by Field Position')
    plt.ylabel('Shot Accuracy (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height + 1,
        f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

    plt.axhline(team_avg, color='red', linestyle='--', linewidth=1.5, label=f'Team Avg: {team_avg:.1f}%')
    plt.legend()

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Shot Accuracy % by Field Position")

@app.route('/fouls_vs_yellow')
def fouls_vs_yellow():
    df = pd.read_csv(DATA_PATH)

    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df = df[df["Player's Role"].isin(roles)]

    # numeric conversion
    df["Fouls Committed"] = pd.to_numeric(df["Fouls Committed"], errors='coerce')
    df["Yellow Cards"] = pd.to_numeric(df["Yellow Cards"], errors='coerce')

    # group by role
    grouped = df.groupby("Player's Role")[["Fouls Committed", "Yellow Cards"]].sum().reset_index()

    x = grouped["Player's Role"]
    fouls = grouped["Fouls Committed"]
    yellows = grouped["Yellow Cards"]

    x_indexes = range(len(x))
    width = 0.35  # Width of bars

    plt.figure(figsize=(8, 5))
    plt.bar([i - width/2 for i in x_indexes], fouls, width=width, label='Fouls Committed', color='#d62728')
    plt.bar([i + width/2 for i in x_indexes], yellows, width=width, label='Yellow Cards', color='#ffbb78')

    plt.xticks(ticks=x_indexes, labels=x)
    plt.ylabel('Total Count')
    plt.title('Fouls vs Yellow Cards by Field Position')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for i, (f, y) in enumerate(zip(fouls, yellows)):
        plt.text(i - width/2, f + 0.5, str(int(f)), ha='center', va='bottom')
        plt.text(i + width/2, y + 0.5, str(int(y)), ha='center', va='bottom')

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Fouls vs Yellow Cards by Field Position")

@app.route('/yellow_rate')
def yellow_rate():
    df = pd.read_csv(DATA_PATH)

    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df = df[df["Player's Role"].isin(roles)]

    # Convert columns to numeric
    df["Fouls Committed"] = pd.to_numeric(df["Fouls Committed"], errors='coerce')
    df["Yellow Cards"] = pd.to_numeric(df["Yellow Cards"], errors='coerce')

    # group by role and calculate rate
    grouped = df.groupby("Player's Role")[["Fouls Committed", "Yellow Cards"]].sum()
    grouped["Yellow Card Rate"] = (grouped["Yellow Cards"] / grouped["Fouls Committed"]) * 100
    grouped = grouped.reset_index()

    plt.figure(figsize=(6, 4))
    bars = plt.bar(grouped["Player's Role"], grouped["Yellow Card Rate"], color=['#9467bd', '#8c564b', '#e377c2'])
    plt.title('Yellow Card Rate per Foul by Field Position')
    plt.ylabel('Yellow Card Rate (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1,
        f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="Yellow Card Rate per Foul by Field Position")

@app.route('/xg_vs_goals')
def xg_vs_goals():
    df = pd.read_csv(DATA_PATH)

    roles = ["ATTACKER", "MIDFIELDER", "DEFENDER"]
    df = df[df["Player's Role"].isin(roles)]

    # Convert columns to numeric
    df["xG (expected goals)"] = pd.to_numeric(df["xG (expected goals)"], errors='coerce')
    df["Total Goals"] = pd.to_numeric(df["Total Goals"], errors='coerce')

    grouped = df.groupby("Player's Role")[["xG (expected goals)", "Total Goals"]].sum().reset_index()

    # extract values for plotting
    x = grouped["Player's Role"]
    xg = grouped["xG (expected goals)"]
    goals = grouped["Total Goals"]
    x_indexes = range(len(x))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar([i - width/2 for i in x_indexes], xg, width=width, label='xG (Expected Goals)', color='#1f77b4')
    plt.bar([i + width/2 for i in x_indexes], goals, width=width, label='Total Goals', color='#2ca02c')

    plt.xticks(ticks=x_indexes, labels=x)
    plt.ylabel('Total Goals / xG')
    plt.title('xG vs Actual Goals by Field Position')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, (xg_val, g_val) in enumerate(zip(xg, goals)):
        plt.text(i - width/2, xg_val + 0.3, f'{xg_val:.1f}', ha='center', va='bottom')
        plt.text(i + width/2, g_val + 0.3, f'{g_val:.1f}', ha='center', va='bottom')

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render_template('dashboard.html', image_base64=image_base64, chart_title="xG vs Actual Goals by Field Position")

@app.route('/test_page')
def test_page():
    return "<h1>This is a test</h1><p>If you see this, Flask is rendering HTML properly.</p>"

# In[28]:


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

