import streamlit as st
from pyzotero import zotero
import pandas as pd
import json
import plotly.express as px

library_id = st.secrets["zotero"]["library_id"]
library_type = st.secrets["zotero"]["library_type"]
api_key = st.secrets["zotero"]["api_key"]

zot = zotero.Zotero(library_id, library_type, api_key)

def set_sidebar():
    # Sidebarの選択肢を定義する
    options = ["dh2024", "jadh2024"]
    choice = st.sidebar.selectbox("Select a collection", options)

    # Mainコンテンツの表示を変える
    if choice == "dh2024":
        # st.write("You selected Option 1")
        collection_id = "LC33JC8D"
    elif choice == "jadh2024":
        collection_id = "P2R95QRF"
        # st.write("You selected Option 2")
    else:
        collection_id = ""
        # st.write("You selected Option 3")

    return collection_id

def create_df(collection_id):

    if collection_id == "":
        return

    # コレクション ID を指定して文献を取得
    # collection_id = 'LC33JC8D'
    items = zot.collection_items(collection_id)

    with open('items.json', 'w') as f:
        # f.write(str(items))
        json.dump(items, f, indent=4, ensure_ascii=False)

    rows = []

    for item in items:
        item_type = item['data']['itemType']

        if item_type == "attachment":
            continue

        rows.append({
            'title': item['data']['title'],
            "itemType": item_type,
            "creators": ", ".join([f"{creator['firstName']} {creator['lastName']}" for creator in item['data']['creators']]) if "creators" in item['data'] else "",
            "date": item['data']['date'] if "date" in item['data'] else "",
        })

    df = pd.DataFrame(rows)

    return df

collection_id = set_sidebar()
df = create_df(collection_id)

st.title('Zotero x Streamlit')

st.header('Table')

if not df.empty:
    st.write(df[['title', 'itemType', 'creators', 'date']])

    # Chart
    st.header('Chart')
    fig = px.pie(df, names='itemType', title='Item Type Distribution')
    st.plotly_chart(fig)
else:
    st.write("No data available.")

