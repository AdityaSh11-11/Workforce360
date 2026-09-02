import plotly.graph_objects as go
import plotly.express as px

COLORS = [
    "#2563EB",  # Blue
    "#06B6D4",  # Cyan
    "#14B8A6",  # Teal
    "#22C55E",  # Green
    "#F59E0B",  # Amber
    "#EF4444",  # Red
    "#8B5CF6",  # Purple
    "#EC4899"   # Pink
]

BACKGROUND = "#111827"
PAPER = "#0F172A"
GRID = "#334155"
TEXT = "#E2E8F0"


def apply_theme(fig, title=None):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PAPER,
        plot_bgcolor=BACKGROUND,
        font=dict(
            family="Inter",
            color=TEXT,
            size=13
        ),
        title=dict(
            text=title if title else fig.layout.title.text,
            x=0.02,
            xanchor="left",
            font=dict(size=20, color="white")
        ),
        colorway=COLORS,
        margin=dict(l=10, r=10, t=55, b=10),
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
            bgcolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_color="white",
            bordercolor="#2563EB"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor=GRID,
        tickfont=dict(color="#CBD5E1")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,.15)",
        zeroline=False,
        tickfont=dict(color="#CBD5E1")
    )

    return fig


def health_gauge(value, title="Health Score"):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"font": {"size": 36, "color": "white"}},
            title={"text": title, "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "bgcolor": "#1E293B",
                "steps": [
                    {"range": [0, 60], "color": "#7F1D1D"},
                    {"range": [60, 80], "color": "#B45309"},
                    {"range": [80, 100], "color": "#14532D"},
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(color="white", family="Inter"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=280
    )

    return fig



def donut_chart(df, column, title):

    fig = px.pie(
        df,
        names=column,
        hole=0.65,
        color_discrete_sequence=COLORS
    )

    fig.update_traces(
        textinfo="percent+label",
        pull=[0.03] * len(df[column].unique())
    )

    return apply_theme(fig, title)


def bar_chart(data, x, y, color=None, title=""):

    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color if color else y,
        color_discrete_sequence=COLORS,
        text_auto=True
    )

    fig.update_traces(marker_line_width=0)

    return apply_theme(fig, title)



def line_chart(data, x, y, color=None, title=""):

    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        markers=True,
        color_discrete_sequence=COLORS
    )

    fig.update_traces(line=dict(width=3))

    return apply_theme(fig, title)



def area_chart(data, x, y, title=""):

    fig = px.area(
        data,
        x=x,
        y=y,
        color_discrete_sequence=["#2563EB"]
    )

    return apply_theme(fig, title)


def scatter_chart(data, x, y, size=None, color=None, title=""):

    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        size=size,
        color_discrete_sequence=COLORS
    )

    return apply_theme(fig, title)


def heatmap(matrix, title="Heatmap"):

    fig = px.imshow(
        matrix,
        color_continuous_scale="Blues",
        aspect="auto"
    )

    return apply_theme(fig, title)



def histogram(data, column, color=None, title=""):

    fig = px.histogram(
        data,
        x=column,
        color=color,
        nbins=25,
        color_discrete_sequence=COLORS
    )

    return apply_theme(fig, title)
