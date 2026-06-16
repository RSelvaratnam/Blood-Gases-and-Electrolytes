import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_excel('LHPP GEM 5000 patients.xlsx', sheet_name='Export')
df = df[df['Source'] != 'Cord']


fig = px.scatter(
    df,
    x='Po2_3500',
    y='sO2_3500',
    color='Source',
    color_discrete_map={
        'Arterial': 'red',
        'Venous': 'blue'
    },
    title="Hemoglobin Oxygen Saturation Curve",
    labels={
        'Po2_3500': 'pO2 [mm Hg]', 
        'sO2_3500': r'$\%SO_2 = \frac{OHb}{OHb+Hb}$',
        'Source': 'Blood Source' 
    }
)

# Create an array of X values from 0 to 120 
x_vals = np.linspace(0, 140, 200)

# Calculating three logistic curve Y values
y_main = 100 * (1 / (1 + np.exp(-0.075 * (x_vals - 32))))
y_left = 100 * (1 / (1 + np.exp(-0.075 * (x_vals - 25))))
y_right = 100 * (1 / (1 + np.exp(-0.075 * (x_vals - 39))))

# Layer the Curves onto the Figure
# Main line
fig.add_trace(
    go.Scatter(
        x=x_vals, y=y_main, 
        mode='lines', 
        line=dict(color='black', width=2),
        name='Main Curve'
    )
)

# Add the left shit
fig.add_trace(
    go.Scatter(
        x=x_vals, y=y_left, 
        mode='lines', 
        line=dict(color='black', width=0.75, dash='dot'),
        name='Left Shift',
        showlegend=False
    )
)

# Add the right dashed line
fig.add_trace(
    go.Scatter(
        x=x_vals, y=y_right, 
        mode='lines', 
        line=dict(color='black', width=0.75, dash='dot'),
        name='Right Shift',
        showlegend=False
    )
)

# plt.axvline(x=60) equivalent
fig.add_vline(x=60, line_dash="dot", line_color="red", opacity=0.8)

# plt.axhline(y=90) equivalent
fig.add_hline(y=90, line_dash="dot", line_color="red", opacity=0.25)

# plt.annotate equivalent
fig.add_annotation(
    x=90, y=30, 
    text='Data from RS/LakeRidge', 
    showarrow=False, 
    font=dict(size=12)
)

# Left Shift Text Block ---
fig.add_annotation(
    x=2, y=90, # Position on the graph (x=pO2, y=sO2)
    xref="x", yref="y",
    # Using HTML for arrows (↑, ↓), subscripts, and line breaks
    text=(
        "<b>Left Shift (↑ affinity for O<sub>2</sub>)</b><br>"
        "↓ [H<sup>+</sup>] or ↑ pH<br>"
        "↓ DPG<br>"
        "↓ Temperature<br>"
        "↓ pCO<sub>2</sub><br><br>"
        "↑ COHb<br>"
        "↑ MetHb<br>"
        "↑ Fetal Hb"
    ),
    showarrow=False,
    font=dict(color="#d62728", size=12), # Red text
    align="left",
    xanchor="left",
    yanchor="top"
)

# --- 2. Left Shift Arrow ---
fig.add_annotation(
    x=32.5, y=68.5,     # Arrow HEAD coordinates
    ax=42.5, ay=68.5,   # Arrow TAIL coordinates
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True,
    arrowhead=2,    # Style of the arrow head
    arrowsize=1.5,  # Size of the arrow head
    arrowwidth=4,   # Thickness of the line
    arrowcolor="#e61b22" # Muted red/salmon arrow
)

# --- 3. Right Shift Text Block ---
fig.add_annotation(
    x=70, y=80, # Position on the graph
    xref="x", yref="y",
    text=(
        "<b>Right Shift (↓ affinity for O<sub>2</sub>)</b><br>"
        "↑ [H<sup>+</sup>] or ↓ pH<br>"
        "↑ DPG<br>"
        "↑ Temperature<br>"
        "↑ pCO<sub>2</sub><br>"
        "↑ HBS"
    ),
    showarrow=False,
    font=dict(color="blue", size=12),
    align="left",
    xanchor="left",
    yanchor="top"
)

# --- 4. Right Shift Arrow ---
fig.add_annotation(
    x=55, y=73,     # Arrow HEAD coordinates
    ax=45, ay=73,   # Arrow TAIL coordinates
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=4,
    arrowcolor="blue"
)

# plt.xlim(0, 120) equivalent
fig.update_xaxes(range=[0, 200])
# Optional: Set y-axis limits to match the 0-100 percentage scale closely
fig.update_yaxes(range=[-5, 105]) 
# Saves an interactive web page
fig.write_image("HOD_Curve2.png", width=1024, height=800, scale=2)

fig.show()