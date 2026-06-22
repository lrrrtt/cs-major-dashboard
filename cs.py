import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. 页面基础配置 (宽屏模式 + 科技感深色系视觉)
# ==========================================
st.set_page_config(
    page_title="CS 历届 Major 赛事全景数据大屏",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #f0f2f6; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 内置数据集 (已更新至 2026 年科隆 Major)
# ==========================================
@st.cache_data
def load_data():
    raw_data = {
        "Year": [2013, 2014, 2014, 2014, 2015, 2015, 2015, 2016, 2016, 2017, 2017, 2018, 2018, 2019, 2019, 2021, 2022, 2022, 2023, 2024, 2024, 2025, 2025, 2026],
        "Event_Name": [
            "DreamHack Winter 2013", "EMS One Katowice 2014", "ESL One Cologne 2014", "DreamHack Winter 2014",
            "ESL One Katowice 2015", "ESL One Cologne 2015", "DreamHack Cluj-Napoca", "MLG Columbus",
            "ESL One Cologne 2016", "ELEAGUE Atlanta 2017", "PGL Major Kraków 2017", "ELEAGUE Boston 2018",
            "FACEIT London 2018", "IEM Katowice 2019", "StarLadder Berlin 2019", "PGL Stockholm 2021",
            "PGL Antwerp 2022", "IEM Rio 2022", "BLAST Paris 2023", "PGL Copenhagen 2024",
            "Perfect World Shanghai 2024", "BLAST Austin 2025", "StarLadder Budapest 2025", "IEM Cologne 2026"
        ],
        "City": ["Jönköping", "Katowice", "Cologne", "Jönköping", "Katowice", "Cologne", "Cluj-Napoca", "Columbus", "Cologne", "Atlanta", "Krakow", "Boston", "London", "Katowice", "Berlin", "Stockholm", "Antwerp", "Rio de Janeiro", "Paris", "Copenhagen", "Shanghai", "Austin", "Budapest", "Cologne"],
        "Country": ["Sweden", "Poland", "Germany", "Sweden", "Poland", "Germany", "Romania", "USA", "Germany", "USA", "Poland", "USA", "UK", "Poland", "Germany", "Sweden", "Belgium", "Brazil", "France", "Denmark", "China", "USA", "Hungary", "Germany"],
        "Latitude": [57.78, 50.26, 50.93, 57.78, 50.26, 50.93, 46.77, 39.96, 50.93, 33.75, 50.06, 42.36, 51.51, 50.26, 52.52, 59.33, 51.22, -22.90, 48.85, 55.67, 31.23, 30.26, 47.49, 50.93],
        "Longitude": [14.16, 19.02, 6.95, 14.16, 19.02, 6.95, 23.60, -83.00, 6.95, -84.39, 19.94, -71.06, -0.13, 19.02, 13.40, 18.06, 4.40, -43.20, 2.35, 12.56, 121.47, -97.74, 19.04, 6.95],
        "Winner": ["fnatic", "Virtus.pro", "Ninjas in Pyjamas", "LDLC", "fnatic", "fnatic", "EnVyUs", "Luminosity", "SK Gaming", "Astralis", "Gambit", "Cloud9", "Astralis", "Astralis", "Astralis", "Natus Vincere", "FaZe Clan", "Outsiders", "Team Vitality", "Natus Vincere", "Team Spirit", "Team Vitality", "Team Vitality", "Team Falcons"],
        "Prize_Pool_USD": [250000, 250000, 250000, 250000, 250000, 250000, 250000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 2000000, 1000000, 1250000, 1250000, 1250000, 1250000, 1250000, 1250000, 1250000],
        "Peak_Viewers": [145000, 250000, 409368, 400000, 982000, 1300000, 973604, 1600000, 850000, 1200000, 961000, 1326000, 1084000, 1205000, 836000, 2748000, 2113000, 1428000, 1528000, 1853000, 1780000, 1650000, 1590000, 1910000],
        "Iconic_Score": [8.0, 8.5, 9.0, 8.2, 8.8, 9.2, 7.5, 9.5, 8.5, 9.0, 8.0, 10.0, 8.5, 8.8, 7.8, 9.8, 9.2, 8.0, 9.0, 8.9, 9.0, 8.7, 8.8, 9.2]
    }
    return pd.DataFrame(raw_data)

df = load_data()

# ==========================================
# 3. 侧边栏交互组件 (过滤器)
# ==========================================
st.sidebar.title("🎮 控制面板")
st.sidebar.info("💡 **提示**：为保证多选框正常运作，请关闭浏览器的“网页自动翻译”功能。")

# 年份上限更新至 2026
year_range = st.sidebar.slider(
    "选择年份范围",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2013, 2026)
)

all_winners = df["Winner"].unique().tolist()
selected_winners = st.sidebar.multiselect(
    "筛选夺冠战队",
    options=all_winners,
    default=all_winners
)

filtered_df = df[
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1]) & 
    (df["Winner"].isin(selected_winners))
]

# ==========================================
# 4. 主页面头部：大标题与核心指标卡 (KPI)
# ==========================================
st.title("🏆 CS 历届 Major 赛事全景数据分析大屏")
st.markdown("展现自2013年至2026年的地理空间演变、王朝更迭与电竞流量演进。")

st.divider()

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("举办Major总届数", f"{len(filtered_df)} 届")
with m2:
    if not filtered_df.empty:
        max_viewers = filtered_df["Peak_Viewers"].max()
        st.metric("最高观赛峰值", f"{max_viewers:,} 人")
    else:
        st.metric("最高观赛峰值", "N/A")
with m3:
    if not filtered_df.empty:
        total_prize = filtered_df["Prize_Pool_USD"].sum()
        st.metric("累计发放奖金", f"${total_prize / 1000000:.2f} M")
    else:
        st.metric("累计发放奖金", "N/A")
with m4:
    if not filtered_df.empty:
        top_winner = filtered_df["Winner"].value_counts().idxmax()
        win_count = filtered_df["Winner"].value_counts().max()
        st.metric("筛选期内最强霸主", f"{top_winner} ({win_count}冠)")
    else:
        st.metric("筛选期内最强霸主", "N/A")

st.divider()

# ==========================================
# 5. 图表模块一：3D 全球足迹 与 观赛热度趋势
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 模块一：Major 全球迁徙轨迹")
    st.caption("3D 视角下的赛事扩张路线 (可鼠标拖拽旋转地球)")
    if not filtered_df.empty:
        path_df = filtered_df.sort_values(by=["Year", "Event_Name"])
        fig_map = go.Figure()

        # 添加航线轨迹连线
        fig_map.add_trace(go.Scattergeo(
            lon=path_df["Longitude"],
            lat=path_df["Latitude"],
            mode="lines",
            line=dict(width=2, color="rgba(255, 75, 75, 0.6)"),
            hoverinfo="none"
        ))

        # 添加举办城市气泡
        marker_sizes = (path_df["Peak_Viewers"] / path_df["Peak_Viewers"].max()) * 20 + 5
        fig_map.add_trace(go.Scattergeo(
            lon=path_df["Longitude"],
            lat=path_df["Latitude"],
            text=path_df["Year"].astype(str) + " " + path_df["Event_Name"] + "<br>峰值: " + path_df["Peak_Viewers"].astype(str) + " 人<br>冠军: " + path_df["Winner"],
            mode="markers",
            marker=dict(
                size=marker_sizes,
                color=path_df["Iconic_Score"],
                colorscale="Viridis",
                showscale=True,
                colorbar_title="经典指数"
            ),
            hoverinfo="text"
        ))

        # 设置为 3D 正交投影
        fig_map.update_layout(
            template="plotly_dark",
            margin=dict(l=0, r=0, t=30, b=0),
            geo=dict(
                projection_type="orthographic",
                showland=True,
                landcolor="#2d3a4b", 
                showocean=True,
                oceancolor="#0e1117", 
                showcountries=True,
                countrycolor="#4b5d78",
                bgcolor='rgba(0,0,0,0)'
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ 当前筛选条件下无数据进行空间显示。")

with col2:
    st.subheader("📈 模块二：观赛流量爆发趋势")
    st.caption("2013-2026年历届赛事观赛峰值变化")
    if not filtered_df.empty:
        fig_line = px.area(
            filtered_df,
            x="Event_Name",
            y="Peak_Viewers",
            text="Winner",
            labels={"Peak_Viewers": "观赛峰值人数", "Event_Name": "赛事名称"}
        )
        fig_line.update_traces(
            mode="lines+markers+text", 
            textposition="top center",
            textfont_size=10,
            marker=dict(size=8, color="#ff4b4b"), 
            line=dict(width=3, color="#ff4b4b"),
            fillcolor="rgba(255, 75, 75, 0.2)"
        )
        fig_line.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("⚠️ 当前筛选条件下无趋势数据。")

# ==========================================
# 6. 图表模块二：战队夺冠排行 与 赛事终极排行榜
# ==========================================
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("👑 模块三：诸神殿 (战队夺冠次数)")
    st.caption("统计各大战队捧起 Major 奖杯的总次数")
    if not filtered_df.empty:
        winner_counts = filtered_df["Winner"].value_counts().reset_index()
        winner_counts.columns = ["Team", "Count"]
        
        fig_bar = px.bar(
            winner_counts,
            y="Team",
            x="Count",
            color="Count",
            color_continuous_scale="Blues",
            orientation="h",
            labels={"Team": "战队名称", "Count": "捧杯次数"}
        )
        fig_bar.update_layout(
            template="plotly_dark", 
            yaxis={'categoryorder':'total ascending'},
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ 暂无战队夺冠统计数据。")

with col4:
    st.subheader("🔥 模块四：历届 Major 终极评分榜")
    st.caption("基于赛事热度与社区评价计算的综合排行榜")
    if not filtered_df.empty:
        display_df = filtered_df.sort_values(by="Iconic_Score", ascending=False)[
            ["Year", "Event_Name", "Winner", "Peak_Viewers", "Iconic_Score"]
        ].reset_index(drop=True)
        
        display_df.columns = ["年份", "赛事名称", "夺冠战队", "观赛峰值", "综合评分"]
        
        st.dataframe(
            display_df.style.background_gradient(cmap="Oranges", subset=["综合评分"]),
            use_container_width=True,
            height=380 
        )
    else:
        st.warning("⚠️ 暂无排行榜数据。")

# ==========================================
# 7. 图表模块三：王朝战队多维能力雷达图
# ==========================================
st.divider()
st.subheader("🕸️ 模块五：核心战队多维能力画像")
st.caption("对比 CS 历史上极具统治力战队的微观特征，探究数据密码。")

# 加入了 Vitality 和 Spirit，以匹配最新的夺冠战队趋势
radar_data = {
    "能力维度": ["综合枪法 (KD)", "首杀破点率 (Entry)", "残局胜率 (Clutch)", "道具管理 (Utility)", "战术执行力 (Tactics)"],
    "Astralis": [85, 80, 95, 100, 100],  
    "Natus Vincere": [98, 95, 85, 80, 85], 
    "fnatic": [90, 85, 90, 75, 80],        
    "FaZe Clan": [95, 90, 80, 85, 85],
    "Team Vitality": [95, 92, 88, 85, 90],
    "Team Spirit": [99, 95, 82, 80, 85]
}
df_radar = pd.DataFrame(radar_data)

col5, col6 = st.columns([1, 3])

with col5:
    st.markdown("#### ⚔️ 战术风格对比")
    st.markdown("请勾选您想要对比的队伍：")
    teams_available = ["Astralis", "Natus Vincere", "fnatic", "FaZe Clan", "Team Vitality", "Team Spirit"]
    selected_radar_teams = st.multiselect(
        "选择战队 (可多选)",
        options=teams_available,
        default=["Astralis", "Natus Vincere", "Team Vitality"]
    )

with col6:
    if selected_radar_teams:
        fig_radar = go.Figure()

        for team in selected_radar_teams:
            r_values = df_radar[team].tolist() + [df_radar[team][0]]
            theta_values = df_radar["能力维度"].tolist() + [df_radar["能力维度"][0]]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=r_values,
                theta=theta_values,
                fill='toself',   
                name=team,
                hoverinfo="text",
                text=[f"{dim}: {val}" for dim, val in zip(theta_values, r_values)]
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#444", linecolor="#444"),
                angularaxis=dict(gridcolor="#444", linecolor="#444"),
                bgcolor="rgba(0,0,0,0)" 
            ),
            template="plotly_dark",
            margin=dict(l=40, r=40, t=20, b=20),
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center") 
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.warning("⚠️ 请在左侧至少选择一支战队进行雷达图对比。")
