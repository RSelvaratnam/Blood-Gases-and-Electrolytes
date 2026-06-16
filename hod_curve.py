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

# plt.xlim(0, 120) equivalent
fig.update_xaxes(range=[0, 200])
# Optional: Set y-axis limits to match the 0-100 percentage scale closely
fig.update_yaxes(range=[-5, 105]) 
# Saves an interactive web page
fig.write_image("HOD_Curve.png", width=1024, height=800, scale=2)

#fig.show()