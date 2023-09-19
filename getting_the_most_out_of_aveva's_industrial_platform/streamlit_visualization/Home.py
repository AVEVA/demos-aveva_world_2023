import streamlit as st
from streamlit_autorefresh import st_autorefresh
from Common import resource, api_version, tenant_id, namespace_id, client, time_to_celebrate

status_mapping = {'UNPLUGGED': '#333333', 'ADAPTIVE': '#3DD56D', 'IDLE': '#ffbd45',
                  'NOT CHARGING': '#ff7d45', 'DISABLED_CHARGER': '#FF3333'}

st.set_page_config(page_icon='🔌', layout='wide')

st.header(f'Chargers Overview')

chargers = client.baseClient.request(
    'GET', f'{resource}/api/{api_version}/Tenants/{tenant_id}/Namespaces/{namespace_id}/Search/Assets?skip=0&count=100&query=&orderby=name%20asc&Filter%5BAssetTypeName%5D=Charging%20Station').json()['Results']

num_columns = 9
rows = [chargers[i:i + num_columns]
        for i in range(0, len(chargers), num_columns)]

for row in rows:
    columns = st.columns(num_columns)
    for i in range(len(row)):
        name = row[i]['Name']
        columns[i].markdown(
            f'<a href="/Car_Charger_Dashboard?charger={name}" style="width: 120px;display: inline-block; padding: 12px 20px; background-color: {status_mapping[row[i]["LastStatus"]["Value"]]}; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;">{name}</a>',
            unsafe_allow_html=True)

legend = st.columns(len(status_mapping))
index = 0
for status, color in status_mapping.items():
    legend[index].color_picker(label = status, value=color, disabled=True)
    index += 1

if (time_to_celebrate and 'celebrated' not in st.session_state):
    st.balloons()
    st.session_state['celebrated'] = True

st_autorefresh(interval=1*60*1000, key='refresh_charger_overview')