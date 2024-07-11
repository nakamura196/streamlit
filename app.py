import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree


input_num = st.number_input('Input a number', value=0)

result = input_num ** 2
st.write('Result: ', result)

st.title('streamlit Tutorial')

st.header('This is a header')

st.subheader('This is a subheader')

st.text('Hello World!')

# st.write()はMarkdown表記対応
st.write('# headline1')
# 以下のように明示的に書くことも可能
st.markdown('# headline2')

st.write(['apple', 'orange', 'banana'])

# ダミーデータの作成
df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
    'gender': ['female', 'male']
})

# DataFrameを表示
st.write(df)
# st.dataframe()でも表示可能
st.dataframe(df)

if st.button('Say hello'):
    st.write('Hello World!')


options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    default=['Yellow', 'Red'] # デフォルトの設定
)

value = st.slider('Select a value', 0, 100, 50) # min, max, default

# Sidebarの選択肢を定義する
options = ["Option 1", "Option 2", "Option 3"]
choice = st.sidebar.selectbox("Select an option", options)

# Mainコンテンツの表示を変える
if choice == "Option 1":
    st.write("You selected Option 1")
elif choice == "Option 2":
    st.write("You selected Option 2")
else:
    st.write("You selected Option 3")


# 2列のカラムを作成
col1, col2 = st.columns(2)

# col1にテキストを表示
with col1:
    st.header("Column 1")
    st.write("This is column 1.")

# col2にDataFrameを表示
with col2:
    st.header("Column 2")
    # DataFrameを表示
    st.write(df)

# Warningの非表示
st.set_option('deprecation.showPyplotGlobalUse', False)

# グラフを描画する
def plot_graph():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    st.pyplot()

# グラフを表示するボタンを表示する
if st.button('Plot graph'):
    plot_graph()

# データをロードする
iris = load_iris()
X, y = iris.data, iris.target

# モデルを学習する
model = DecisionTreeClassifier()
model.fit(X, y)

# モデルを可視化する
def plot_model():
    plot_tree(model)
    st.pyplot()

# モデルを表示するボタンを表示する
if st.button('Plot model'):
    plot_model()

# ボタンが押された回数を保持する
if "count" not in st.session_state:
    st.session_state.count = 0

# ボタンを表示し、クリックされた回数を表示する
if st.button("Click me"):
    st.session_state.count += 1

st.write(f"You clicked the button {st.session_state.count} times.")