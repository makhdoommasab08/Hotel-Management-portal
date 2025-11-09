import streamlit as st

def render_kpis(df):
    k1, k2, k3, k4 = st.columns(4)
    total = len(df)
    booked = int(df['is_booked'].sum()) if total > 0 else 0
    vacant = total - booked
    avg_rating = round(df['rating'].mean(), 2) if total > 0 else 0
    cancel_rate = round(df['is_canceled'].mean() * 100, 2) if total > 0 else 0

    with k1:
        st.markdown(f"<div class='card'><div style='font-weight:700'>Booked Rooms</div><div style='font-size:20px'>{booked}</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='card'><div style='font-weight:700'>Vacant Rooms</div><div style='font-size:20px'>{vacant}</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='card'><div style='font-weight:700'>Average Rating</div><div style='font-size:20px'>{avg_rating} ⭐</div></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='card'><div style='font-weight:700'>Cancellation Rate</div><div style='font-size:20px'>{cancel_rate}%</div></div>", unsafe_allow_html=True)