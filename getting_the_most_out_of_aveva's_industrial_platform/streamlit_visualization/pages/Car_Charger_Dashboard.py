from adh_sample_library_preview import Asset
from datetime import datetime, timedelta
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from Common import get_figure, namespace_id, client

st.set_page_config(page_icon='🔌', layout='centered')

status_mapping = {'UNPLUGGED': 'grey', 'IDLE': 'orange',
                  'NOT CHARGING': 'orange', 'ADAPTIVE': 'green', 'DISABLED_CHARGER': 'red'}
image_mapping = {'Webasto DX': 'https://www.kia.com/us/en/ev/_jcr_content/root/responsivegrid/quizform.coreimg.100.400.png/1681792146933/quizform.png',
                 'Tesla': 'https://www.tesla.com/sites/default/files/images/charging/wall_connector_home_installation.jpg'}

header = st.empty()

# Create inputs
chargers = client.Assets.getAssets(
    namespace_id, 'assetTypeName:"Charging Station"')
selected_charger_name = st.selectbox(
    'Car Charger', [charger.Name for charger in chargers])
if (st.experimental_get_query_params() and 'charger' in st.experimental_get_query_params()):
    selected_charger_name = st.experimental_get_query_params()['charger'][0]
    st.experimental_set_query_params()

selected_charger: Asset = next((charger for charger in chargers if charger.Name.casefold() ==
                                selected_charger_name.casefold()), None)
header = header.header(f'{selected_charger_name} Dashboard')

# Create multi tab view
current_values_tab, trend_tab = st.tabs(['Current Values', 'Trend'])

# Create current values tab
left_column, right_column = current_values_tab.columns(2)
timestamp = left_column.empty()
status = left_column.empty()
amps = left_column.empty()
started_session_count = left_column.empty()
evese_type = next((metadatum.Value for metadatum in selected_charger.Metadata if metadatum.Name.casefold() ==
                   'EVSE Type'.casefold()), None)
right_column.image(
    image_mapping[selected_charger.Metadata[2].Value], use_column_width=True)

# Create trend tab
amps_trend = trend_tab.empty()

# Set metrics data
charger_data = client.Assets.getAssetLastData(
    namespace_id,
    selected_charger.Id
).Results

timestamp = timestamp.metric(
    f'Timestamp', charger_data['PilotSignalAmps'][0]['Timestamp'])
status = status.metric(
    f':{status_mapping[charger_data["Status"][0]["Value"]]}[Status]', charger_data['Status'][0]['Value'])
amps = amps.metric(
    f'Current', f'{float(charger_data["PilotSignalAmps"][0]["Value"]):.2f} A')
started_session_count = started_session_count.metric(
    f'Session Count', f'{int(charger_data["StartedSessionCount"][0]["Value"])}')

# Set trend data
raw_data = client.Assets.getAssetSampledData(namespace_id, selected_charger.Id, start_index=(
    datetime.utcnow() - timedelta(hours=2)).isoformat(), end_index=datetime.utcnow().isoformat(), intervals=350).Results
amps_data_frame = pd.DataFrame.from_dict(raw_data["PilotSignalAmps"])
amps_data_frame['Timestamp'] = pd.to_datetime(amps_data_frame['Timestamp'])

fig = get_figure(amps_data_frame, False)
amps_trend.plotly_chart(fig)

st_autorefresh(interval=1*60*1000, key='refresh_charger_daahsboard')
