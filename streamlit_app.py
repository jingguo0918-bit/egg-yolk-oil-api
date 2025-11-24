import streamlit as st
import requests
import json

# -------------------------------------------------
# App UI (C 风格：科研简洁风 + 食品工业色彩)
# -------------------------------------------------

st.set_page_config(
    page_title="Egg Yolk Oil Predictor",
    page_icon="🥚",
    layout="centered"
)

st.title("🥚 Egg Yolk Oil Release Prediction System")
st.write("基于蛋黄氧化指标的 **AI 出油率预测模型（v1.0）**")

st.markdown("---")
st.subheader("🔬 输入你的检测指标（可来自实验或生产线传感器）")

# -------------------------------------------------
# 用户输入
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    SH = st.number_input("SH（μmol/g）", min_value=0.0, value=10.0)
    MDA = st.number_input("MDA（nmol/g）", min_value=0.0, value=1.0)
    Carbonyl = st.number_input("Carbonyl（nmol/mg）", min_value=0.0, value=0.5)

with col2:
    D50 = st.number_input("粒径 D50（μm）", min_value=0.0, value=40.0)
    T2 = st.number_input("T₂（ms）", min_value=0.0, value=50.0)

st.markdown("---")

# -------------------------------------------------
# 调用你的后端 server.py API
# -------------------------------------------------

API_URL = "https://egg-yolk-oil-api.streamlit.app/?path=predict/expert"

def call_api(SH, MDA, D50, T2, Carbonyl):
    params = {
        "SH": SH,
        "MDA": MDA,
        "D50": D50,
        "T2": T2,
        "Carbonyl": Carbonyl
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        return response.json()
    except:
        return {"error": "无法连接到服务器，请检查 API 是否在线。"}

# -------------------------------------------------
# 风险评估
# -------------------------------------------------

def risk_level(oil):
    if oil < 20:
        return "🟢 低风险（出油率低）"
    elif 20 <= oil <= 40:
        return "🟡 中风险（需要关注）"
    else:
        return "🔴 高风险（出油率高，需重点监控）"

# -------------------------------------------------
# 预测按钮
# -------------------------------------------------

if st.button("🚀 一键预测蛋黄出油率"):
    with st.spinner("AI 正在分析中…"):

        result = call_api(SH, MDA, D50, T2, Carbonyl)

        if "prediction" in result:
            oil = float(result["prediction"])

            st.success(f"预测出油率：**{oil:.2f}%**")
            st.info(risk_level(oil))

            st.markdown("---")
            st.subheader("📊 输入参数回顾")
            st.json(result["inputs"])

        else:
            st.error("服务器返回错误，请检查 API。")
            st.json(result)

