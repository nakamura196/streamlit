import streamlit as st
from pyzotero import zotero
import pandas as pd
import plotly.express as px

# Zotero APIの初期設定
def init_zotero():
    library_id = st.secrets["zotero"]["library_id"]
    library_type = st.secrets["zotero"]["library_type"]
    api_key = st.secrets["zotero"]["api_key"]
    return zotero.Zotero(library_id, library_type, api_key)

def fetch_collections(zot):
    """ Zoteroライブラリからコレクション一覧を取得する """
    collections = zot.collections()
    # 各コレクションからタイトルとキー（ID）を取得
    collection_list = [{"name": collection['data']['name'], "key": collection['data']['key']} for collection in collections]
    return collection_list

# サイドバー設定
def set_sidebar(collection_list):
    collection_options = [col['name'] for col in collection_list]
    collection_keys = {col['name']: col['key'] for col in collection_list}
    selected_collection_name = st.sidebar.selectbox("Select a collection", options=collection_options)
    return collection_keys.get(selected_collection_name, ""), selected_collection_name


# 文献データをDataFrameに変換
def create_df(zot, collection_id):
    if not collection_id:
        return pd.DataFrame()

    try:
        items = zot.collection_items(collection_id)
        rows = [{
            'title': item['data']['title'],
            "itemType": item['data']['itemType'],
            "creators": ", ".join(f"{creator['firstName']} {creator['lastName']}" for creator in item['data'].get('creators', [])),
            "date": item['data'].get('date', "")
        } for item in items if item['data']['itemType'] != "attachment"]
        
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Failed to load items from collection: {e}")
        return pd.DataFrame()

# アプリケーションのメイン関数
def main():

    # ページの設定
    st.set_page_config(
        page_title="Zotero x Streamlit",  # ブラウザのタイトルバーに表示されるタイトル
        page_icon="🧊",               # ブラウザのタブに表示されるアイコン
        # layout="wide",                # レイアウトを広いものに設定
        # initial_sidebar_state="expanded",  # サイドバーの初期状態を展開に設定
        menu_items={                  # 追加のメニューオプションとともにメタタグ設定
            'Get Help': "https://github.com/nakamura196/zotero_streamlit/",
            'Report a bug': 'https://github.com/nakamura196/zotero_streamlit/issues',
            'About': "App development using [Zotero](https://www.zotero.org/)'s API and Streamlit"
        }
    )

    zot = init_zotero()
    collection_list = fetch_collections(zot)
    collection_id, collection_name = set_sidebar(collection_list)
    df = create_df(zot, collection_id)

    st.title('Zotero x Streamlit')

    st.write(collection_name)

    st.header('Table')
    if not df.empty:
        st.write(df)
        st.header('Chart')
        fig = px.pie(df, names='itemType', title='Item Type Distribution')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

    
if __name__ == "__main__":
    main()