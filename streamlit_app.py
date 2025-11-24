import streamlit as st
import numpy as np

# ------------------------------
# 内置本地预测模型（代替 API）
# ------------------------------
def predict_oil_release(SH, MDA, D50, T2, Carbonyl):
    """
    一个示例预测模型（线性回归形式）
    你可以根据真实公式修改
    """
    # 你的模型权重（示例）
    coef_SH = -0.8
    coef_MDA = 1.2
    coef_D50 = 0.05
    coef_T2 = -0.03
    coef_Carbonyl = 2.0
    bias = 10

    oil = (coef_SH * SH +
           coef_MDA * MDA +
           coef_D50 * D50 +
           coef_T2 * T2 +
           coef_Carbonyl * Carbonyl +
           bias)

    # 结果限制在合理区间
    return max(0, min(round(oil, 2), 100))


# ------------------------------
# Streamlit 页面
# ------------------------------
st.set_page_config(page_title="蛋黄出油率预测系统", page_icon="🥚", layout="wide")

st.title("🥚 Egg Yolk Oil Release Prediction System")
st.write("基于蛋黄氧化指标的 AI 出油率预测模型（本地版，无需 API）")

# 输入参数
st.header("🧪 输入你的检测指标（可来自实验或产线传感器）")

col1, col2 = st.columns(2)

with col1:
    SH = st.number_input("SH（μmol/g）", value=10.0)
    MDA = st.number_input("MDA（nmol/g）", value=1.0)
    Carbonyl = st.number_input("Carbonyl（nmol/mg）", value=0.5)

with col2:
    D50 = st.number_input("粒径 D50（μm）", value=40.0)
    T2 = st.number_input("T₂（ms）", value=50.0)

# ------------------------------
# 按钮触发本地预测
# ------------------------------
st.write("---")
if st.button("🚀 一键预测蛋黄出油率"):
    oil_rate = predict_oil_release(SH, MDA, D50, T2, Carbonyl)

    st.success(f"预测的蛋黄出油率：**{oil_rate}%**")

    st.progress(min(1.0, oil_rate / 100))


