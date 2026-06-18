import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. 页面基础配置 (宽屏模式 + 科技感深色系视觉)
# ==========================================
st.set_page_config(
    page_title="CS 历届 Major 赛事全景数据大屏",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入自定义 CSS 进一步美化界面
st.markdown("""
    <style>
    /* 主背景与字体颜色 */
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #f0f2f6; }
    /* 隐藏顶部的装饰条和底部的全屏按钮以保持清爽 */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 内置数据集 (免去读取外部文件的麻烦，加入缓存提升加载速度)
# ==========================================
@st.cache_data
def load_data():
    raw_data = {
        "Year": [2013, 2014, 2014, 2014, 2015, 2015, 2015, 2016, 2016, 2017, 2017, 2018, 2018, 2019, 2019, 2021, 2022, 2022, 2023, 2024],
        "Event_Name": [
            "DreamHack Winter 2013", "EMS One Katowice 2014", "ESL One: Cologne 2014", "DreamHack Winter 2014",
            "ESL One: Katowice 2015", "ESL One: Cologne 2015", "DreamHack Open Cluj-Napoca", "MLG Major Championship: Columbus",
            "ESL One: Cologne 2016", "ELEAGUE Major Atlanta 2017", "PGL Major Kraków 2017", "ELEAGUE Major Boston 2018",
            "FACEIT Major: London 2018", "IEM Katowice Major 2019", "StarLadder Berlin Major 2019", "PGL Major Stockholm 2021",
            "PGL Major Antwerp 2022", "IEM Rio Major 2022", "BLAST.tv Paris Major 2023", "PGL Major Copenhagen 2024"
        ],
        "City": ["Jönköping", "Katowice", "Cologne", "Jönköping", "Katowice", "Cologne", "Cluj-Napoca", "Columbus", "Cologne", "Atlanta", "Krakow", "Boston", "London", "Katowice", "Berlin", "Stockholm", "Antwerp", "Rio de Janeiro", "Paris", "Copenhagen"],
        "Country": ["Sweden", "Poland", "Germany", "Sweden", "Poland", "Germany", "Romania", "USA", "Germany", "USA", "Poland", "USA", "UK", "Poland", "Germany", "Sweden", "Belgium", "Brazil", "France", "Denmark"],
        "Latitude": [57.78, 50.26, 50.93, 57.78, 50.26, 50.93, 46.77, 39.96, 50.93, 33.75, 50.06, 42.36, 51.51, 50.26, 52.52, 59.33, 51.22, -22.90, 48.85, 55.67],
        "Longitude": [14.16, 19.02, 6.95, 14.16, 19.02, 6.95, 23.60, -83.00, 6.95, -84.39, 19.94, -71.06, -0.13, 19.02, 13.40, 18.06, 4.40, -43.20, 2.35, 12.56],
        "Winner": ["fnatic", "Virtus.pro", "Ninjas in Pyjamas", "LDLC", "fnatic", "fnatic", "EnVyUs", "Luminosity", "SK Gaming", "Astralis", "Gambit", "Cloud9", "Astralis", "Astralis", "Astralis", "Natus Vincere", "FaZe Clan", "Outsiders", "Team Vitality", "Natus Vincere"],
        "Prize_Pool_USD": [250000, 250000, 250000, 250000, 250000, 250000, 250000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 2000000, 1000000, 1250000, 1250000, 1250000],
        "Peak_Viewers": [145000, 250000, 409368, 400000, 982000, 1300000, 973604, 1600000, 850000, 1200000, 961000, 1326000, 1084000, 1205000, 836000, 2748000, 2113000, 1428000, 1528000, 1853000],
        "Iconic_Score": [8.0, 8.5, 9.0, 8.2, 8.8, 9.2, 7.5, 9.5, 8.5, 9.0, 8.0, 10.0, 8.5, 8.8, 7.8, 9.8, 9.2, 8.0, 9.0, 8.9]
    }
    return pd.DataFrame(raw_data)

df = load_data()

# ==========================================
# 3. 侧边栏交互组件 (过滤器)
# ==========================================
st.sidebar.title("🎮 控制面板")
st.sidebar.markdown("通过以下控件动态筛选大屏数据：")

# 温馨提示：解决浏览器自动翻译导致的筛选失效问题
st.sidebar.info("💡 **提示**：为保证多选框正常运作，请关闭浏览器的“网页自动翻译”功能。")

# 年份筛选滑块
year_range = st.sidebar.slider(
    "选择年份范围 (Year Range)",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2013, 2024)
)

# 战队多选框
all_winners = df["Winner"].unique().tolist()
selected_winners = st.sidebar.multiselect(
    "筛选夺冠战队 (Filter by Winner)",
    options=all_winners,
    default=all_winners
)

# 根据侧边栏输入过滤数据集
filtered_df = df[
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1]) & 
    (df["Winner"].isin(selected_winners))
]

# ==========================================
# 4. 主页面头部：大标题与核心指标卡 (KPI)
# ==========================================
st.title("🏆 CS 历届 Major 赛事全景数据分析大屏")
st.markdown("展现自2013年成立以来的地理空间轨迹、诸神更迭与电竞流量演变。")

# 【修复点】：使用 st.divider() 替代 st.hr()
st.divider()

# 核心数据卡片展示 (KPI)
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
        # 将奖金格式化为百万单位，看起来更高端
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
# 5. 图表模块一：全球足迹 与 观赛热度趋势
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 模块一：Major 全球足迹")
    st.caption("气泡大小代表观赛峰值，颜色代表经典指数评分")
    if not filtered_df.empty:
        # 优化点：增加 hover_data 让悬停提示信息更丰富
        fig_map = px.scatter_geo(
            filtered_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Event_Name",
            hover_data={"Winner": True, "Peak_Viewers": True, "Iconic_Score": True, "Latitude": False, "Longitude": False},
            size="Peak_Viewers",
            color="Iconic_Score",
            projection="natural earth",
            color_continuous_scale="Viridis",
            size_max=25 # 优化气泡最大比例，避免过分遮挡
        )
        fig_map.update_layout(
            template="plotly_dark", 
            margin=dict(l=0, r=0, t=30, b=0),
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#1f2630') # 让地图融入深色背景
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ 当前筛选条件下无数据进行空间显示。")

with col2:
    st.subheader("📈 模块二：观赛流量爆发趋势")
    st.caption("2013-2024年历届赛事观赛峰值变化")
    if not filtered_df.empty:
        # 优化点：添加动态面积填充，使趋势图看起来更饱满
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
            fillcolor="rgba(255, 75, 75, 0.2)" # 半透明红色填充
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
        
        # 优化点：改为水平条形图，战队名字显示更完整
        fig_bar = px.bar(
            winner_counts,
            y="Team",
            x="Count",
            color="Count",
            color_continuous_scale="Blues",
            orientation="h", # 水平显示
            labels={"Team": "战队名称", "Count": "捧杯次数"}
        )
        fig_bar.update_layout(
            template="plotly_dark", 
            yaxis={'categoryorder':'total ascending'}, # 按夺冠次数由高到低排序
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ 暂无战队夺冠统计数据。")

with col4:
    st.subheader("🔥 模块四：历届 Major 终极评分榜")
    st.caption("基于赛事热度与社区评价计算的综合排行榜")
    if not filtered_df.empty:
        # 重命名列名，让前端展示对非技术人员更友好
        display_df = filtered_df.sort_values(by="Iconic_Score", ascending=False)[
            ["Year", "Event_Name", "Winner", "Peak_Viewers", "Iconic_Score"]
        ].reset_index(drop=True)
        
        display_df.columns = ["年份", "赛事名称", "夺冠战队", "观赛峰值", "综合评分"]
        
        # 优化表格样式，高亮重点列
        st.dataframe(
            display_df.style.background_gradient(cmap="Oranges", subset=["综合评分"]),
            use_container_width=True,
            height=380 # 固定高度匹配左侧柱状图
        )
    else:
        st.warning("⚠️ 暂无排行榜数据。")