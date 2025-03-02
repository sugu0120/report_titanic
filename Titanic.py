import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🚢 タイタニック生存者分析")


df = pd.read_csv("./data/tested.csv",encoding="utf-8")
st.write("データのサンプル:")
st.dataframe(df)
#年齢と乗船港の欠損を中央値と最頻値にする
df["Age"].fillna(df["Age"].median(), inplace=True)           
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

#性別を「男性」「女性」から「1」「0」に変換
df["Sex"] = df["Sex"].map({"male": 1, "female": 0})

#サイドバーを追加（乗客クラスを１，２，３、乗船港をC,Q,Sとしてサイドバーに表示）
target_classes = st.sidebar.multiselect("乗船クラス", df["Pclass"].unique(), df["Pclass"].unique())
target_ports = st.sidebar.multiselect("乗船港", df["Embarked"].unique(), df["Embarked"].unique())

df = df[df["Pclass"].isin(target_classes)]
df = df[df["Embarked"].isin(target_ports)]

st.write(f"データ件数: {len(df)} 件")

st.subheader("乗船クラスごとの生存率")
fig, ax = plt.subplots()
sns.barplot(x=df["Pclass"], y=df["Survived"], ax=ax, palette="coolwarm")
st.pyplot(fig)

#年齢を10歳間隔ごとに生存者の平均値を計算して生存率を算出
df["AgeGroup"] = pd.cut(df["Age"], bins=range(0, 101, 10), right=False)
age_survival = df.groupby("AgeGroup")["Survived"].mean().reset_index()


st.subheader("年齢層ごとの生存率")
fig, ax = plt.subplots()
sns.barplot(x="AgeGroup", y="Survived", data=age_survival, ax=ax, palette="viridis")
st.pyplot(fig)
