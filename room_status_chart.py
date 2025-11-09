import streamlit as st
import plotly.graph_objects as go
import time

def show_room_status_chart(df):
    booked = df["is_booked"].sum()
    vacant = len(df) - booked

    # Button with hover glow effect
    st.markdown("""
    <style>
    .hover-btn {
        background: linear-gradient(90deg, #2563eb, #06b6d4);
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.4rem;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        box-shadow: 0 0 8px rgba(14,165,233,0.6);
        transition: all 0.3s ease-in-out;
    }
    .hover-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(14,165,233,0.9);
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🎯 View Live Room Status", key="room_status_btn"):
        with st.spinner("Analyzing room data..."):
            time.sleep(1.2)

        # Animated Donut Chart
        fig = go.Figure(data=[go.Pie(
            labels=["Booked Rooms", "Vacant Rooms"],
            values=[booked, vacant],
            hole=.55,
            marker=dict(colors=["#38bdf8", "#4ade80"]),
            textinfo="label+percent",
            pull=[0.03, 0]
        )])

        fig.update_layout(
            title="<b>🏠 Room Occupancy Overview</b>",
            title_font_size=20,
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend=dict(orientation="h", x=0.3, y=-0.15),
            transition={"duration": 800, "easing": "cubic-in-out"}
        )

        st.plotly_chart(fig, use_container_width=True)
