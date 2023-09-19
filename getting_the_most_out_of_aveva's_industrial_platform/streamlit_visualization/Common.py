import pandas as pd
import plotly.express as px
import streamlit as st
from adh_sample_library_preview import ADHClient


time_to_celebrate = True
resource = st.secrets['resource']
api_version = st.secrets['api_version']
tenant_id = st.secrets['tenant_id']
namespace_id = st.secrets['namespace_id']

# Read client from session state or create one if it does not already exist
if 'client' in st.session_state:
    client = st.session_state['client']
else:
    client_id = st.secrets['client_id']
    client = ADHClient(api_version, tenant_id, resource,
                       client_id, accept_verbosity=True)
    st.session_state['client'] = client

def get_figure(data_frame: pd.DataFrame, range_slider: bool):
    fig = px.line(data_frame, x='Timestamp', y=data_frame.columns,
                  color_discrete_sequence=px.colors.qualitative.Alphabet)

    for index in range(len(fig.data)):
        fig.data[index].yaxis = f'y{"" if index == 0 else index+1}'
        fig.update_layout({
            f'yaxis{"" if index==0 else index + 1}': {
                'title': fig.data[0].name if len(fig.data) == 1 else 'Value' if index == 0 else '',
                'anchor': 'free',
                'position': index/12,
                'overlaying': None if index == 0 else 'y',
                'tickfont': dict(
                    color=px.colors.qualitative.Alphabet[index]
                ),
                'titlefont': dict(
                    color=px.colors.qualitative.Alphabet[index]
                )
            }
        })
    fig.update_xaxes(
        domain=[.05*len(fig.data), 1],
        rangeslider_visible=range_slider,
        fixedrange=range_slider
    )

    return fig
