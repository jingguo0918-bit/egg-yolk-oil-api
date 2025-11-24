import streamlit as st
import pandas as pd
import numpy as np
import json

st.set_page_config(page_title="Egg Yolk Oil API", layout="wide")

def risk_level(v):
    if v < 20:
        return "🟢 低风险"
    elif v < 40:
        return "🟡 中风险"
    else:
        return "🔴 高风险"

def suggestion(v):
    if v < 20:
        return "适合烘焙、蛋黄酥、月饼馅料，油脂稳定。"
    elif v < 40:
        return "适用于一般咸蛋黄加工，可适当调整腌制周期。"
    else:
        return "风险偏高，建议降低自由基强度或缩短腌制时间。"

def model_quick(value):
    oil = 15 + 1.1 * value
    return {
        "OilYield": round(oil, 2),
        "Risk": risk_level(oil),
        "Suggestion": suggestion(oil)
    }

def model_expert(SH, MDA, D50, T2, Carbonyl):
    oil = (
        0.5 * SH +
        2.0 * MDA +
        0.1 * D50 +
        0.05 * T2 +
        3.0 * Carbonyl
    )
    return {
        "OilYield": round(oil, 2),
        "Risk": risk_level(oil),
        "Suggestion": suggestion(oil)
    }

query_params = st.experimental_get_query_params()
path = query_params.get("path", [""])[0]

if path == "predict/quick":
    value = float(query_params.get("value", [0])[0])
    result = model_quick(value)
    st.write(result)

elif path == "predict/expert":
    SH = float(query_params.get("SH", [0])[0])
    MDA = float(query_params.get("MDA", [0])[0])
    D50 = float(query_params.get("D50", [0])[0])
    T2 = float(query_params.get("T2", [0])[0])
    C = float(query_params.get("Carbonyl", [0])[0])
    result = model_expert(SH, MDA, D50, T2, C)
    st.write(result)

elif path == "realtime/latest":
    x = np.random.uniform(5, 60)
    result = model_quick(x)
    st.write(result)

else:
    st.json({
        "API": "Egg Yolk Oil AI Cloud API",
        "Routes": {
            "/?path=predict/quick&value=10": "快速模式预测",
            "/?path=predict/expert&SH=10&MDA=1&D50=40&T2=50&Carbonyl=0.5": "专家模式预测",
            "/?path=realtime/latest": "实时监测数据",
        }
    })
