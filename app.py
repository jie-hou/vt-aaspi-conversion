#################################################################
# Date        Aurthor    Notes
# 09/07/2019  Tim Roden  Initial Impolementation for vt to aaspi
# 05/19/2020  Jie Hou    Add streamlit for GUI and aaspi to vt
#################################################################

import streamlit as st
import SessionState
from geoio import GeoIoVolume
from utils import *


def main():
    """
    This function is the main function for the seismic format conversion utility. 
    It uses streamlit for the web interface. 
    """

    session_state = SessionState.get(
        inputvt='', inputaaspi='', outputpath='', horizontal_unit='', vertical_unit='')

    st.title("Seismic Format Conversion Utility")
    st.info("This is an utility to convert seismic data between vt and aaspi(.H) format!")

    st.header("**Input Summary:**")

    st.sidebar.title("Setting")
    st.sidebar.markdown("Please set up the input/output paramters here!")
    selection = st.sidebar.radio("Go to", ["vt to aaspi","aaspi to vt"])
    st.sidebar.header("**Set Up Input**")

    if selection == 'vt to aaspi':

        if st.sidebar.button('Selct VT File...'):
            session_state.inputvt = select_vt()
        horizontal_unit = st.sidebar.selectbox(
            "Select the horizontal unit", ['m', 'ft'])
        vertical_unit = st.sidebar.selectbox(
            "Select the vertical unit", ['ms', 's', 'ft', 'm'])
        st.write("**The selected input vt is:**", session_state.inputvt)

        st.sidebar.header("**Set Up Output**")
        if st.sidebar.button('Selct Output Path...'):
            session_state.outputpath = select_output()

        st.write("**The selected output path is:**", session_state.outputpath)

        st.write("**The horizon unit is :**", horizontal_unit)
        st.write("**The vertical unit is :**", vertical_unit)

        if session_state.inputvt:
            vt = GeoIoVolume(session_state.inputvt)

            vt_params = set_vt_params(vt)
            aaspi_params = set_aaspi_params(vt.get_filename(),
                                       session_state.outputpath, horizontal_unit,
                                         vertical_unit)
        
      
        if st.button('Convert from VT to AASPI'):
            progress = st.progress(0)
            status_text = st.empty()
            write_aaspi_header(vt_params, aaspi_params)
            write_aaspi_idents_header(vt_params, aaspi_params)
            write_aaspi_binaries_from_vt(vt, vt_params, aaspi_params, progress, status_text)
            status_text.text("Apply pad3d on the volume...")
            run_pad3d(aaspi_params)
            msg = {'Operation': 'VT to AASPI',
                'VT Name': vt.get_filename(),
                'VT Size': str(os.path.getsize(vt.get_filename())), 
                'Survey Location': str(vt.get_survey().epsg_code())
            }
            track_usage(msg)
            st.success("Successfully converted!")
    else: 
        if st.sidebar.button('Selct AASPI File...'):
            session_state.inputaaspi = select_aaspi()

        if st.sidebar.button('Selct VT File...'):
            session_state.inputvt = select_vt()



        st.write("**The selected input aaspi file is:**", session_state.inputaaspi)
        st.write("**The selected input vt file is:**", session_state.inputvt)

        st.sidebar.header("**Set Up Output**")
        if st.sidebar.button('Selct Output Path...'):
            session_state.outputpath = select_output()
        st.write("**The selected output path is:**", session_state.outputpath)

        if st.button('Convert from AASPI to VT'):
            progress = st.progress(0)
            status_text = st.empty()
            write_vt_data(session_state, progress, status_text)
            inputvt = GeoIoVolume(session_state.inputvt)
            msg = { 'Operation': 'AASPI to VT',
                'VT Name': inputvt.get_filename(),
                'Survey Location': str(inputvt.get_survey().epsg_code())
            }
            track_usage(msg)
            st.success("Successfully converted!")

    st.sidebar.title("About")
    st.sidebar.info(
            "This app is not fully tested. Please use at your own risk. Contact Jie.Hou@shell.com for questions.\n"
    )

if __name__ == "__main__":
    main()
