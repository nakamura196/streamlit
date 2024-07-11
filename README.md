# Zotero x Streamlit Integration

This repository hosts the code for an app developed using Zotero's API and Streamlit. The app demonstrates how to integrate Zotero's bibliographic management capabilities with a web application, providing a user-friendly interface to interact with your Zotero collections.

## App Overview

The app is deployed and can be viewed at:

🔗 [Zotero x Streamlit App](https://nakamura196-zotero.streamlit.app/)

![App Screenshot](https://storage.googleapis.com/zenn-user-upload/37c9984861f5-20240711.png)

## Key Features

- **Collection Listing**: Fetch and display a list of collections from a Zotero library.
- **Items Viewing**: View details of items within a selected collection, filtering out attachments.
- **Interactive Charts**: Visualize data distributions using Plotly charts.

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: An open-source app framework for Machine Learning and Data Science projects.
- **[Zotero API](https://www.zotero.org/support/dev/web_api/v3/start)**: Used for accessing bibliographic data stored in Zotero.
- **[Pyzotero](https://github.com/urschrei/pyzotero)**: A Python client for the Zotero API.

## Quick Start

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/nakamura196/zotero_streamlit.git
   cd zotero_streamlit
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Zotero API credentials. Create a file named `.streamlit/secrets.toml` and fill it with your Zotero details:

   ```toml
   [zotero]
   library_id = "your_library_id"
   library_type = "user"
   api_key = "your_api_key"
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment

This app is deployed on Streamlit Community Cloud. You can deploy your own version by clicking the 'Deploy' button in Streamlit and following the prompts. Don't forget to add your secrets in the Streamlit Cloud dashboard under 'Advanced settings'.

## How It Works

### Fetch Collections

Retrieve a list of collections from your Zotero library:

```python
def fetch_collections(zot):
    collections = zot.collections()
    return [{"name": collection['data']['name'], "key": collection['data']['key']} for collection in collections]
```

### Create DataFrames

Convert item data from Zotero into a pandas DataFrame, excluding attachments:

```python
def create_df(zot, collection_id):
    items = zot.collection_items(collection_id)
    return pd.DataFrame([{
        'title': item['data']['title'],
        "itemType": item['data']['itemType'],
        "creators": ", ".join(f"{creator['firstName']} {creator['lastName']}" for creator in item['data'].get('creators', [])),
        "date": item['data'].get('date', "")
    } for item in items if item['data']['itemType'] != "attachment"])
```

### Configure Page Settings

Set up the page with title, icon, and additional menu options:

```python
st.set_page_config(
    page_title="Zotero x Streamlit",
    page_icon="🧊",
    menu_items={
        'Get Help': "https://github.com/nakamura196/zotero_streamlit/",
        'Report a bug': 'https://github.com/nakamura196/zotero_streamlit/issues',
        'About': "This is an app developed using Zotero's API and Streamlit."
    }
)
```

## Conclusion

This project illustrates the power of combining Zotero's bibliographic tools with Streamlit's interactive capabilities. It's a practical example of how these technologies can be used to enhance the accessibility and visualization of bibliographic data.
