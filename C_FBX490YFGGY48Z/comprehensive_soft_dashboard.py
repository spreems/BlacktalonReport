import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os
from advanced_soft_reports import AdvancedSoftReports
import rpt_utils
# from snowflake_integration import SnowflakeIntegration

# Page configuration
st.set_page_config(
    page_title="Comprehensive Software Asset Dashboard",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .report-section {
        margin-top: 2rem;
        padding: 2rem;
        border: 2px solid #e0e0e0;
        border-radius: 1rem;
        background: #f8f9fa;
    }
    # .sidebar .sidebar-content {
    #     background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    # }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    st.write('  56  cs ')
    try:
        df = st.session_state.rpt_data_df
        df_filtered = st.session_state.rpt_data_filtered_df
        df = df.dropna(subset=['NAME'])
        df['NAME'] = df['NAME'].astype(str)
        st.write('csd  61  ')
        st.write(df)
        return df, df_filtered
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() 

def my_function(publisher, status):
    st.write(f"Publisher '{publisher}' checkbox is {status}")

def handle_change(key_prefix=None, label=None, key=None, idxx=None , value001=None,col_name=None, cn=None,disable=None):
    # st.write(f" 74 cs.handle_change ")
    # st.write(st.session_state['wrk_rpt_fltr_col_df'])
    # st.write(st.session_state.reset_selected_value)
    # st.write(f"58  {key_prefix}_{idxx}_{cn}  : " + str(st.session_state[key]) + "  " + str(datetime.now()))
    # st.write(f"59  →→→ key_prefix  {key_prefix} →→ label → {label} →→ key  →  {key} →→ idxx → {idxx} →→ value001 → {value001} →→ col_name → {col_name} →→ cn → {cn} →→ disable → {disable} ")
    st.session_state.curr_fltr_selected_kp = key_prefix
    st.session_state.curr_fltr_selected_cn = cn
    st.session_state['curr_fltr_selected'] = key_prefix
    # st.write('  74   '  + st.session_state['curr_fltr_selected'])
    st.session_state['key_selected'] = key
    session_rpt_fltr_var = 'rpt_fltr_' + col_name
    # st.write( ' 80   : ' + session_rpt_fltr_var)
    # st.write(st.session_state[session_rpt_fltr_var])
    chk_box_df = st.session_state[session_rpt_fltr_var]
    checkbox_status = st.session_state[key]
    if 'prev_fltr_selected_kp' in st.session_state:
        if st.session_state.curr_fltr_selected_kp != st.session_state.prev_fltr_selected_kp:
            st.session_state['wrk_rpt_fltr_col_df']["PREV_VISIBLE"] = False
        else:
            st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["COL_NAME"] == col_name, "VISIBLE"] = st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["COL_NAME"] == col_name, "PREV_VISIBLE"]    
    else:
        st.session_state['wrk_rpt_fltr_col_df']["PREV_VISIBLE"] = False
        
    st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["COL_NAME"] == col_name, "PREV_VISIBLE"] = st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["COL_NAME"] == col_name, "VISIBLE"]
    # st.write(f"cs handle_change Before")
    # st.write(chk_box_df)
# START  2025-10-26  3;11    Temp Moved from set-check_box
    if 'filtered_df_001' in  st.session_state:
        # st.write(st.session_state['filtered_df_001'])
        # st.write(st.session_state['wrk_rpt_fltr_col_df'])
        filtered_df_001 = st.session_state['filtered_df_001']
        st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']['VALUE'] == cn, 'CHECKED'] = checkbox_status
        st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']['VALUE'] == cn, 'FILTER'] = checkbox_status        
        # st.write('91   cs')
        # st.write(st.session_state['wrk_rpt_fltr_col_df'])
        chk_box_df.loc[idxx, "CHECKED"] = checkbox_status
        # st.write(chk_box_df)
        checked_map = chk_box_df.loc[chk_box_df['CHECKED'] == True, [col_name, 'CHECKED']].set_index(col_name)['CHECKED']
        # st.write(checked_map)
        # st.write(chk_box_df.loc[idxx])
            
    # START  2025-10-26  3:36    Temp Moved from set-check_box    
        # st.write('checkbox_status 153  : ' + selected_key + ' ---- '  +  str(checkbox_status) )
        # if 'change_log' in st.session_state and len(st.session_state.change_log) > 0:
        # st.write(st.session_state.change_log)
        #     kp_to_flase = st.session_state.change_log.loc[st.session_state.change_log["key"] == cn, "key_prefix"].iloc[0]
        #     st.write(f"*** kp_to_flase ***  --> {kp_to_flase}")
        df = filtered_df_001
        if 1 == 1:  #'key_selected' in st.session_state and  st.session_state['key_selected'] == selected_key:
            # st.write( ' 115   ' + st.session_state['key_selected'] + ' ---- '  + str(st.session_state[st.session_state.key_selected]))
            if cn not in st.session_state.change_log["key"].values:               
                new_row = {
                    "key_prefix": key_prefix,
                    "col_name": col_name,
                    "label": label,
                    "key": cn,
                    "value001": True,
                    "filtered": False,
                    "filter": True,
                    "checked": True,
                    "disabled": disable
                }
                
                # Append to session_state DataFrame
                st.session_state.change_log = pd.concat([st.session_state.change_log, pd.DataFrame([new_row])], ignore_index=True )
                st.session_state.set_selected_value = cn
            else:
                st.session_state.reset_selected_value = cn
                st.session_state.change_log["UNCHECKED"] = False
                st.session_state.change_log["CLEAR"] = False
                inactive_idx = st.session_state.change_log.index[st.session_state.change_log["key"] == cn]
                st.session_state.change_log.loc[inactive_idx, "UNCHECKED"] = True
                inactive_idx = st.session_state.change_log.index[st.session_state.change_log["UNCHECKED"] == True]
                # st.write(inactive_idx)
                if not inactive_idx.empty:
                    start_idx = inactive_idx[0]
                    a = st.session_state.change_log.iloc[start_idx]["col_name"]
                    b = st.session_state.change_log.iloc[start_idx]["key"]
                    c = st.session_state.change_log.iloc[start_idx]["key_prefix"]
                    # st.write(f"139   {a} →→ {b} →→ {c}")
                    df.loc[df[a] == b, c] = False
                    st.session_state.change_log.loc[start_idx + 1:, "CLEAR"] = True                    
                    st.session_state.change_log = st.session_state.change_log.drop(index=start_idx)
                    st.session_state.change_log = st.session_state.change_log.reset_index(drop=True)
                    # st.write(df)
                for _, row in st.session_state.change_log.iterrows(): 
                    if row["CLEAR"] == True:
                        a = row["col_name"]
                        b = row["key"]
                        c = row["key_prefix"]
                        # st.write(f"150   {a} →→ {b} →→ {c}")
                        df.loc[df[a] == b, c] = False
                        st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VALUE"]== st.session_state.reset_selected_value,"FILTERED"] = False
                    
                    # Set UNCHECKED = True for all rows after that index

                # st.write(' 140 cn  ' + cn)
#                st.session_state.change_log = st.session_state.change_log[st.session_state.change_log["key"] != cn].reset_index(drop=True)
                st.session_state[session_rpt_fltr_var].loc[st.session_state[session_rpt_fltr_var][col_name] == cn, "CHECKED"] = False
            # str(st.session_state[st.session_state.key_selected])
            if len(st.session_state.change_log) > 0:
                st.session_state['first_in_change_log'] = st.session_state.change_log.loc[st.session_state.change_log.index[0], "key_prefix"]
            else:
                st.session_state['first_in_change_log'] = ''
        # st.write(f"164  →→→ change_log  wrk_rpt_fltr_col_df  ")
        # st.write(df)
        # st.write(st.session_state.change_log)
        # st.write(st.session_state['wrk_rpt_fltr_col_df'])
        # st.write(f"168")    
        # st.write(df)    
        dfx = dfx = st.session_state.change_log
        for _, row in dfx.iterrows():
            # st.write('172   -  ' + row["col_name"]  + ' - ' +row["key_prefix"]  + ' - ' + row["label"]  + ' - ' + row["key"])
            df.loc[df[row["col_name"]] == row["key"], row["key_prefix"]] = True  
        # st.write(df)
        
    # END  2025-10-26  3:36    Temp Moved from set-check_box
# END  2025-10-26  3:11    Temp Moved from set-check_box
        # chk_box_df.loc[idxx, "CHECKED"] = checkbox_status
        # # st.write(chk_box_df)
        # checked_map = chk_box_df.loc[chk_box_df['CHECKED'] == True, [col_name, 'CHECKED']].set_index(col_name)['CHECKED']


        if 'set_selected_value' in st.session_state and  st.session_state.set_selected_value != None:
            # st.write('Line 174   '+ set_selected_value + str(datetime.now()))
            st.session_state['wrk_rpt_fltr_col_df']['CHECKED'] = st.session_state['wrk_rpt_fltr_col_df']['VALUE'].map(checked_map).fillna(st.session_state['wrk_rpt_fltr_col_df'].get('CHECKED', False))
            st.session_state['wrk_rpt_fltr_col_df']['FILTER'] = st.session_state['wrk_rpt_fltr_col_df']['VALUE'].map(checked_map).fillna(st.session_state['wrk_rpt_fltr_col_df'].get('CHECKED', False))
            st.session_state['wrk_rpt_fltr_col_df']['FILTERED'] = st.session_state['wrk_rpt_fltr_col_df']['VALUE'].map(checked_map).fillna(st.session_state['wrk_rpt_fltr_col_df'].get('CHECKED', False))
            st.session_state['wrk_rpt_fltr_col_df'][st.session_state.curr_fltr_selected_kp] = st.session_state['wrk_rpt_fltr_col_df']['VALUE'].map(checked_map).fillna(st.session_state['wrk_rpt_fltr_col_df'].get('CHECKED', False))

        #     st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VALUE"]== st.session_state.set_selected_value,"DT_ADDED"] = datetime.now()
        if 'reset_selected_value' in st.session_state and st.session_state.reset_selected_value != None:
            # st.write('Line 181   '+ reset_selected_value + str(datetime.now()))    
            st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VALUE"]== st.session_state.reset_selected_value,"FILTER"] = False
            st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VALUE"]== st.session_state.reset_selected_value,"DT_REMOVED"] = datetime.now()
            st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VALUE"]== st.session_state.reset_selected_value,"FILTERED"] = False
            
            # st.session_state['wrk_rpt_fltr_col_df']['FILTERED'] = st.session_state['wrk_rpt_fltr_col_df']['VALUE'].map(checked_map).fillna(st.session_state['wrk_rpt_fltr_col_df'].get('CHECKED', False))

        # st.write(f"189  →→→ change_log  wrk_rpt_fltr_col_df  ")
        # st.write(st.session_state.change_log)
        # st.write(st.session_state['wrk_rpt_fltr_col_df']) 
        
            # st.write('177 cs')
            # st.write(st.session_state['wrk_rpt_fltr_col_df'])
        if 'first_in_change_log' in st.session_state and len(st.session_state.first_in_change_log) > 0 :
            # st.write('171  :  '  + st.session_state['first_in_change_log'])            
            # st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["SHOW"]== True] = False
            st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["SHOW"]== True,"SHOW"] = False
            st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["KEY_PREFIX"]== st.session_state.first_in_change_log,"SHOW"] = True

        if 'change_log' in st.session_state and 1==1:
            # Builds a Unique set of key_Prefix and Column Name
            
            unique_kp = (
                st.session_state.change_log.drop_duplicates(subset=["key_prefix"])  # keep first instance of each key_prefix
                .reset_index(drop=True)
                .assign(Seq=lambda x: range(1, len(x) + 1))  # add sequence column
            )[["Seq", "key_prefix", "col_name"]]

            #######  START TO DEBUG HERE   ----- SREERAJ
            # This is where KPXXXX Is Added to the DF and the matching NAME and Key Values are validateted and KPXXXX is set to TRUE 
            # df = filtered_df_001
            
            if checkbox_status == False:
                kp_to_flase = key_prefix
                df.loc[df[col_name] == cn, kp_to_flase] = False 
            
            df_col_wrk = pd.DataFrame({"a": [col_name],"b": [cn],"c": [checkbox_status]})
            # st.write(st.session_state.change_log)
            # if "UNCHECKED" in st.session_state.change_log.columns():
            
            
            # st.write(f"193")    
            # st.write(df)    
            dfx = dfx = st.session_state.change_log
            for _, row in dfx.iterrows():
                # st.write('235   -  ' + row["col_name"]  + ' - ' +row["key_prefix"]  + ' - ' + row["label"]  + ' - ' + row["key"])
                df.loc[df[row["col_name"]] == row["key"], row["key_prefix"]] = True  
            # st.write(df)
            #######  END   TO DEBUG HERE   ----- SREERAJ
            
        # This is where df is set to Filter Enable/Disable Specific Filter Keys
        #   COL_NAME, VALUE, SHOW,FILTER, FILTERED, CHECKED, KEY_PREFIX, DISABLED, DT_ADDED, DT_REMOVED
            # st.write( '258 cs ')
            # st.write(st.session_state.change_log)
            # st.write(unique_kp)
            # st.write(st.session_state['wrk_rpt_fltr_col_df'])
            # st.write(filtered_df_001)
            fltr_filtered = apply_fltr_to_filters(unique_kp,st.session_state['wrk_rpt_fltr_col_df'],filtered_df_001,df_col_wrk)
            # st.write(fltr_filtered)
            # st.write(st.session_state['fltr_wrk_df'])


        if 'change_log' in st.session_state and len(st.session_state.change_log) > 0:
            # st.write(st.session_state.change_log)
            if checkbox_status == False and 1 == 2:
                kp_to_flase = key_prefix
                df.loc[df[col_name] == cn, kp_to_flase] = False   
                
                # st.write(f"*** kp_to_flase ***  --> {kp_to_flase}")
                # col_name_to_false = col_name
                # key_value = cn
        # st.write(f"cs handle_change After")
        # st.write(chk_box_df)   
        # st.write(st.session_state['wrk_rpt_fltr_col_df'])   
        st.session_state.prev_fltr_selected_kp = key_prefix
    



def set_check_box(df,col_name,lbl_name,key_prefix):
    # with st.sidebar.expander("🔍 Filter", expanded=False):
    # st.write(col_name)
    # st.write(df)
    if "rpt_filters" not in st.session_state:
        st.session_state["rpt_filters"] = {}
    
    if 'change_log' not in st.session_state:
        st.session_state.change_log = pd.DataFrame(columns=["key_prefix","col_name", "label", "key", "value001", "filtered", "filter", "checked","disabled"])         
    # Account filter
    session_rpt_fltr_var = 'rpt_fltr_' + col_name
    # st.write(f" 281  ->   {session_rpt_fltr_var} -> {col_name} ")
    if session_rpt_fltr_var not in st.session_state:        
        st.session_state[session_rpt_fltr_var] = []
    if 'x' not in st.session_state:
        x = []

    chk_col = sorted(df[col_name].dropna().unique())
    chk_box_df = pd.DataFrame({col_name: chk_col})
    # st.write(f" cs 291")
    # st.write(chk_box_df)
    # if 'wrk_rpt_fltr_col_df' in st.session_state:
    #     st.write(f"307  cs set_check_box")
    #     st.write(st.session_state['wrk_rpt_fltr_col_df'])

    # st.write(st.session_state[session_rpt_fltr_var])
    # chk_box_df["CHECKED"] = chk_box_df[col_name].isin(st.session_state[session_rpt_fltr_var])
    if 'wrk_rpt_fltr_col_df' in st.session_state:
        # st.write(f"***  299  ***")
        rpt_utils.filter(st.session_state['rpt_data_df'],st.session_state['wrk_rpt_fltr_col_df'])    
    # else:
        # st.write(f"***  302  ***")
    # st.write(st.session_state['wrk_rpt_fltr_col_df'])        
    ficl = 0
    # st.write(st.session_state[session_rpt_fltr_var])
    if len(st.session_state[session_rpt_fltr_var]) > 0:
        # st.write(f"***  306  ***")
        chk_box_df["VISIBLE"] = False
        chk_box_df["CHECKED"] = chk_box_df[col_name].isin(st.session_state[session_rpt_fltr_var].loc[st.session_state[session_rpt_fltr_var]["CHECKED"], col_name])
        chk_box_df["SHOW"] = chk_box_df[col_name].isin(st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["SHOW"], "VALUE"])        
        chk_box_df["PREV_VISIBLE"] = chk_box_df[col_name].isin(st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["PREV_VISIBLE"], "VALUE"])        
        if 'VISIBLE' in st.session_state['wrk_rpt_fltr_col_df']: # 'wrk_rpt_fltr_col_df' in st.session_state and len(st.session_state['wrk_rpt_fltr_col_df']) > 0:
            # st.write(f"***  310  ***")
            chk_box_df["VISIBLE"] = chk_box_df[col_name].isin(st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VISIBLE"], "VALUE"])        
        if 'first_in_change_log' in st.session_state:
            ficl = len(st.session_state.first_in_change_log)
        # st.write(st.session_state[session_rpt_fltr_var])            
    else:
        # st.write(f"***  315  ***")
        if 'first_in_change_log' in st.session_state:
            ficl = len(st.session_state.first_in_change_log)
        else:
            ficl = 0
        # st.write(f" 297 first_in_change_log  -> {ficl}")
        chk_box_df["CHECKED"] = False
        chk_box_df["VISIBLE"] = False
        chk_box_df["SHOW"] = False
        chk_box_df["PREV_VISIBLE"] = False
        
    # st.write(chk_box_df)     
    
    filter_changed = False
    
    with st.expander(lbl_name, expanded=False):

        # select_all = st.checkbox( "Select / Unselect All", key=f"{key_prefix}_select_all",label_visibility="collapsed")     #,value=all_selected
        # if select_all:
        #     chk_box_df["CHECKED"] = True
        #     st.write(f" 299 select_all -> {select_all}")
        # else:
        #     chk_box_df["CHECKED"] = False
        #     # st.write(f" 356 select_all -> {select_all}")
        reset_selected_value = None
        set_selected_value = None
        
        st.session_state['chk_box_df'] = chk_box_df

        if 'fltr_wrk_df' in st.session_state:
            fltr_d_df = st.session_state['fltr_wrk_df']
            fltr_d_df.loc[fltr_d_df["DISABLED"].isna(), "DISABLED"] = False
            # st.write(fltr_filtered)
        # if 'wrk_rpt_fltr_col_df' in st.session_state:
        #     # st.write(f"***  310  ***")
        #     rpt_utils.filter(st.session_state['rpt_data_df'],st.session_state['wrk_rpt_fltr_col_df'])
        # if len(st.session_state[session_rpt_fltr_var]) > 0 and 1==2:
        #     if 'wrk_rpt_fltr_col_df' in st.session_state and len(st.session_state['wrk_rpt_fltr_col_df']) > 0:
        #         chk_box_df["VISIBLE"] = chk_box_df[col_name].isin(st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VISIBLE"], "VALUE"])        
            
        # st.write(st.session_state['wrk_rpt_fltr_col_df'])
            
        
        st.session_state[session_rpt_fltr_var] = chk_box_df
        # st.write(f"377  cs set_check_box")
        # st.write(f"378  cs set_check_box", chk_box_df)

        for idx, row in chk_box_df.iterrows():
            idxx = int(idx) if not pd.isna(idx) else -1
            # st.write(type(idx), idxx)
            cn = row[col_name]
            cb_status = row["CHECKED"]
            cb_visible = row["VISIBLE"]
            cb_show = row["SHOW"]
            cb_prev_visible = row["PREV_VISIBLE"]
            # st.write(f"ficl {ficl} -> {key_prefix}_{idxx}_{cn} -> {cb_status} -> {cb_visible}")

            disable = False
            # if 'fltr_wrk_df' in st.session_state and len(st.session_state['fltr_wrk_df']) > 0 and "DISABLED" in st.session_state['fltr_wrk_df'].columns:
            #     # fltr_d_df
            #     disabled_arr = fltr_d_df.loc[(fltr_d_df["COL_NAME"] == col_name) & (fltr_d_df["VALUE"] == cn), "DISABLED"].values
            #     disable = disabled_arr[0] if len(disabled_arr) > 0 else False
            #     # disabled=bool(df.loc[idx, "DISABLED"])
            #     disable=bool(disable)
            # checkbox_status = False
            if ficl == 0:
                # st.write(f"399 ")
                checkbox_status = st.checkbox(
                    cn,
                    key=f"{key_prefix}_{idxx}_{cn}",
                    value= False,           #row["CHECKED"],
                    on_change=handle_change, kwargs={"key_prefix": key_prefix, "label": lbl_name, "key": f"{key_prefix}_{idxx}_{cn}", "idxx": idxx, "value001": row["CHECKED"],"col_name": col_name, "cn":cn, "disable":disable}
                    ,disabled = disable
                )
                # Update checked status in dataframe
                selected_key=f"{key_prefix}_{idxx}_{cn}"
    
                chk_box_df.loc[idxx, "CHECKED"] = checkbox_status
    
            # the below 3 lines used by st.session_state["abcd"]: 2025-10-26  9:47pm
                if checkbox_status and cn not in st.session_state[session_rpt_fltr_var]:
                    x.append(cn)
                    filter_changed = True
                
            else:
                # st.write(f"418 ")
                if (cb_visible == True or cb_show == True or cb_prev_visible == True):
                    # st.write(f"363 ")
                    checkbox_status = st.checkbox(
                        cn,
                        key=f"{key_prefix}_{idxx}_{cn}",
                        value= row["CHECKED"],
                        on_change=handle_change, kwargs={"key_prefix": key_prefix, "label": lbl_name, "key": f"{key_prefix}_{idxx}_{cn}", "idxx": idxx, "value001": row["CHECKED"],"col_name": col_name, "cn":cn, "disable":disable}
                        ,disabled = False
                    )
                    # Update checked status in dataframe
                    selected_key=f"{key_prefix}_{idxx}_{cn}"
        
                    chk_box_df.loc[idxx, "CHECKED"] = checkbox_status
        
                # the below 3 lines used by st.session_state["abcd"]: 2025-10-26  9:47pm
                    if checkbox_status and cn not in st.session_state[session_rpt_fltr_var]:
                        x.append(cn)
                        filter_changed = True                    
                elif 1==2 : #
                #     st.write('Disable below')
                # else:
                    # st.write(f"372 ")                    
                    checkbox_status = st.checkbox(
                        cn,
                        key=f"{key_prefix}_{idxx}_{cn}",
                        value= row["CHECKED"],
                        on_change=handle_change, kwargs={"key_prefix": key_prefix, "label": lbl_name, "key": f"{key_prefix}_{idxx}_{cn}", "idxx": idxx, "value001": row["CHECKED"],"col_name": col_name, "cn":cn, "disable":disable}
                        ,disabled = False
                    )                    
                    
                    
            
        #     # Update checked status in dataframe
        #     selected_key=f"{key_prefix}_{idxx}_{cn}"

        #     chk_box_df.loc[idxx, "CHECKED"] = checkbox_status

        # # the below 3 lines used by st.session_state["abcd"]: 2025-10-26  9:47pm
        #     if checkbox_status and cn not in st.session_state[session_rpt_fltr_var]:
        #         x.append(cn)
        #         filter_changed = True
        chk_box_df["VISIBLE"] = chk_box_df[col_name].isin(st.session_state['wrk_rpt_fltr_col_df'].loc[st.session_state['wrk_rpt_fltr_col_df']["VISIBLE"], "VALUE"])            
        # st.write(chk_box_df)                
        st.session_state[session_rpt_fltr_var] = chk_box_df
        s_temp={session_rpt_fltr_var:x}
        if "abcd" not in st.session_state:
            st.session_state["abcd"] = {}
        checked_map = chk_box_df.loc[chk_box_df['CHECKED'] == True, [col_name, 'CHECKED']].set_index(col_name)['CHECKED']

        dfx = st.session_state.change_log

        #######  START TO DEBUG HERE   ----- SREERAJ
        # This is where KPXXXX Is Added to the DF and the matching NAME and Key Values are validateted and KPXXXX is set to TRUE 
        # for _, row in dfx.iterrows():
        #     # st.write('235   -  ' + row["col_name"]  + ' - ' +row["key_prefix"]  + ' - ' + row["label"]  + ' - ' + row["key"])
        #     df.loc[df[row["col_name"]] == row["key"], row["key_prefix"]] = True  
        # st.write(df)
        #######  END   TO DEBUG HERE   ----- SREERAJ
       
        for key, values in s_temp.items():
            # st.write('110  ' + key + ' -  ' + str(values))
            if key in st.session_state["abcd"]:
                for v in values:
                    # st.write('112  ' + key + ' -- ' + v)
                    if v not in st.session_state["abcd"][key]:
                        st.session_state["abcd"][key].append(v)
                    current_vals = st.session_state["abcd"][key]
                    to_remove = [v for v in current_vals if v not in values]
                    for r in to_remove:
                        st.session_state["abcd"][key].remove(r)
                        # st.write(f'🗑 Removed: {r}')
            else:
                # Create new key
                st.session_state["abcd"][key] = values.copy()   
    # st.write(st.session_state["abcd"])
        st.session_state['display_df'] = df    
    return st.session_state["abcd"]
    
def apply_fltr_to_filters(kp_unique_df,filter_df,data_df,df_col_wrk):
    # fltr_df,marked_fltr_df
    filter_df = st.session_state['wrk_rpt_fltr_col_df']
    if "DISABLED" not in filter_df.columns:
        filter_df["DISABLED"] = False

    # Builds a Unique set of key_Prefix and Column Name
    unique_fltered_df = (
        filter_df.drop_duplicates(subset=["KEY_PREFIX"])  # keep first instance of each key_prefix
        .reset_index(drop=True)
        .assign(Seq=lambda x: range(1, len(x) + 1))  # add sequence column
    )[["Seq", "KEY_PREFIX", "COL_NAME"]]
    # st.write(unique_fltered_df)
    # st.write('433  cs  ')

    # active_KP = kp_list
    active_KP = kp_unique_df["key_prefix"].unique().tolist()
    # st.write(' active_KP ' + active_KP + ' len(kp_unique_df) ' + str(len(kp_unique_df)))
    # st.write(f"**438 →  {active_KP} → {len(kp_unique_df)}**")
    # aaaa = [active_KP[0]] + [x for x in unique_fltered_df if x != active_KP[0]] if active_KP[0] in unique_fltered_df else unique_fltered_df.copy()
    # st.write(df_col_wrk)''

    if len(kp_unique_df) > 0 and 1==2:
        a =  unique_fltered_df["KEY_PREFIX"].unique().tolist()
        aaaa = [active_KP[0]] + [x for x in a if x != active_KP[0]]
        # st.write('439 cs : ' + str(aaaa) )
        # st.write(aaaa)
 

    # st.write(str('287')   +  ' - ' + str(len(active_KP)) + '  -  ' + str(active_KP))
    if len(kp_unique_df) > 0 and 1 == 1:
        a =  unique_fltered_df["KEY_PREFIX"].unique().tolist()
        aaaa = [active_KP[0]] + [x for x in a if x != active_KP[0]]
        
        # merged_df = pd.DataFrame()
        # for idx, key_prefix in enumerate(active_KP):
        for idx, key_prefix in enumerate(aaaa):            
            # st.write('461')
            # st.write(key_prefix)
            idxx = int(idx) if not pd.isna(idx) else -1
            # st.write(f"**456 →  {idxx} → {key_prefix}**")
            # st.write(data_df)
            if key_prefix in data_df.columns:
                aa = data_df[key_prefix] == True
        # col = kp_unique_df['col_name'][idxx]
                # target_rpt_fltr_var = 'rpt_fltr_' + col
                # target_df = st.session_state[target_rpt_fltr_var]
                # st.write('463')
                # st.write(target_df)
                # st.write(kp_unique_df)
                matches = kp_unique_df.index[kp_unique_df["key_prefix"] == key_prefix].tolist()
                idx = matches[0] if matches else None
                # st.write(idx)
                kp = key_prefix     #kp_unique_df['key_prefix'][idxx]
                # st.write('478 kp   ' + kp)
                # i = 0
                for idy, row in unique_fltered_df.iterrows():
                    if row["KEY_PREFIX"] != kp:
                        # st.write(row["KEY_PREFIX"])
                        col_a = unique_fltered_df['COL_NAME'][idy]
                        # st.write(f"**473   col_a  → {idy} → {col_a}**")
                        active_aa = data_df.loc[aa, col_a].dropna().unique()
                        
                        mask = filter_df["KEY_PREFIX"] == row["KEY_PREFIX"]
                        # st.write('col_a  : '+ str(col_a) + '   mask : '+ str(mask)   + '   --- filter_df.KEY_PREFIX:' + str(filter_df["KEY_PREFIX"]) + '  ---  row.KEY_PREFIX:   ' + row["KEY_PREFIX"])
                        # st.write('col_a  : '+ str(col_a) + '   mask : '+ str(mask)   + '  ---  row.KEY_PREFIX:   ' + row["KEY_PREFIX"])
                        # st.write('318 col_a  : '+ str(col_a) +  '  ---  row.KEY_PREFIX:   ' + row["KEY_PREFIX"])
        
                        filter_df.loc[mask & filter_df["VALUE"].isin(active_aa), "FILTERED"] = True
                        # FILTERED = TRUE
                        # filter_df.sort_values(by=["FILTERED", "FILTER", "DISABLED", "CHECKED"], ascending=False, inplace=True)                    
                        # st.write(filter_df)
                        filter_df.loc[mask & filter_df["VALUE"].isin(active_aa), "DISABLED"] = False                 
                        # DISABLED = FALSE
                        filter_df.sort_values(by=["FILTERED", "FILTER", "DISABLED", "CHECKED"], ascending=False, inplace=True)                    
                        # st.write(filter_df)
                        # DISABLED = TRUE
                        filter_df.loc[mask & ~filter_df["VALUE"].isin(active_aa), "DISABLED"] = True
    
                # filter_df.sort_values(by=["FILTERED", "FILTER", "DISABLED", "CHECKED"], ascending=False, inplace=True)                   
                # st.write(filter_df)              
                        # filter_df["DISABLED"].fillna(False, inplace=True)
                
             
        
            # st.write('cs  277')
            # st.write(filter_df)
        st.session_state['active_KP'] = active_KP
        filter_df = filter_df.drop_duplicates(subset=["COL_NAME", "VALUE"], keep="first")
        st.session_state['fltr_wrk_df'] = filter_df
        if "DISABLED" not in filter_df.columns:
            filter_df["DISABLED"] = False
        else:
            filter_df.loc[filter_df["DISABLED"].isna(), "DISABLED"] = False        
    
        filter_df.sort_values(by=["FILTERED", "FILTER", "DISABLED", "CHECKED"], ascending=False, inplace=True)
        # st.write('cs  273')
        # st.write(filter_df)
    return filter_df        #filtered_df

# def apply_filters(df, filters,col_name):
#     st.write('cs 399' + str(datetime.now()))
#     # st.write(st.session_state.change_log)
#     df1 = st.session_state.change_log
#     for _, row in df1.iterrows():
#         # st.write('232   -  ' + row["col_name"]  + ' - ' +row["key_prefix"]  + ' - ' + row["label"]  + ' - ' + row["key"])
#         df.loc[df[row["col_name"]] == row["key"], row["key_prefix"]] = True
        
#     filtered_df = df.copy()
#     rpt_fltr_type = 'rpt_fltr_' + col_name
    
#     st.write(df)
#     filtered_df = df
#     st.session_state['rpt_data_filtered_df'] = filtered_df
#         # st.write(df)
#         # st.write(datetime.now())
#     return filtered_df

def create_overview_dashboard(df):
    """Create comprehensive overview dashboard"""
    st.markdown('<h4 class="main-header">💻 Comprehensive Software Asset Dashboard</h4>', unsafe_allow_html=True)
    top_n = st.session_state['top_n']
    # Key Metrics
    # st.subheader("📊 Key Performance Indicators")
    if len(df) > 0:
    
    #     col1, col2, col3, col4, col5, col6 = st.columns(6)
        
    #     with col1:
    #         st.metric("Total Records", f"{len(df):,}")
    #     with col2:
    #         st.metric("Unique Accounts", f"{df['NAME'].nunique():,}")
    #     with col3:
    #         st.metric("Unique Assets", f"{df['ASSETUUID'].nunique():,}")
    #     with col4:
    #         st.metric("Unique Publishers", f"{df['PUBLISHER'].nunique():,}")
    #     with col5:
    #         st.metric("Unique Categories", f"{df['CATEGORY'].nunique():,}")
    #     with col6:
    #         st.metric("Unique Products", f"{df['PRODUCTNAME'].nunique():,}")
        
        # Advanced Analytics
        st.subheader("🔍 Advanced Analytics")
        
        # Initialize advanced reports
        advanced_reports = AdvancedSoftReports(df)
        
        # Publisher analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Publishers")
            publisher_analysis = advanced_reports.create_publisher_analysis()
            st.dataframe(publisher_analysis.head(top_n),hide_index=True)
        
        with col2:
            st.subheader("Top Categories")
            category_analysis = advanced_reports.create_category_analysis()
            st.dataframe(category_analysis.head(top_n),hide_index=True)
        
        # Advanced visualizations
        st.subheader("📈 Advanced Visualizations")
        visualizations = advanced_reports.create_advanced_visualizations()
        
        # Display visualizations in a grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(visualizations['publisher_pie'], use_container_width=True)
            st.plotly_chart(visualizations['account_heatmap'], use_container_width=True)
        
        with col2:
            st.plotly_chart(visualizations['category_treemap'], use_container_width=True)
            st.plotly_chart(visualizations['correlation_heatmap'], use_container_width=True)
        
        # Software type distribution
        st.plotly_chart(visualizations['software_type_bar'], use_container_width=True)
    else:
        st.write (f"***No Data To Display***")
        
def create_account_reports(df):
    """Create detailed account reports"""
    st.header("🏢 Account Analysis Reports")
    top_n = st.session_state['top_n']

    if len(df) > 0:    
        # Account summary
        account_summary = df.groupby('NAME').agg({
            'ASSETUUID': 'nunique',
            'PUBLISHER': 'nunique',
            'CATEGORY': 'nunique',
            'PRODUCTNAME': 'nunique',
            'SOFTWARETYPE': 'nunique'
        }).reset_index()
        
        account_summary.columns = ['NAME', 'ASSETUUID', 'Publishers', 'Categories', 'Products', 'Software_Types']
        
        # Account metrics visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(account_summary.head(top_n), x='NAME', y='ASSETUUID',
                         title='Assets per Account', color='ASSETUUID',
                         color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(account_summary.head(top_n), x='Publishers', y='Products',
                            size='ASSETUUID', color='NAME',
                            title='Account Software Distribution',
                            hover_data=['Categories', 'Software_Types'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Account comparison
        st.subheader("Account Comparison")
        st.dataframe(account_summary.head(top_n))
        
        # Account drill-down
        st.subheader("Account Drill-Down Analysis")
        selected_account = st.selectbox("Select Account for Detailed Analysis", df['NAME'].unique())
        
        if selected_account:
            account_data = df[df['NAME'] == selected_account]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Software", len(account_data))
                st.metric("Unique Assets", account_data['ASSETUUID'].nunique())
                st.metric("Unique Publishers", account_data['PUBLISHER'].nunique())
            
            with col2:
                st.metric("Unique Categories", account_data['CATEGORY'].nunique())
                st.metric("Unique Products", account_data['PRODUCTNAME'].nunique())
                st.metric("Software Types", account_data['SOFTWARETYPE'].nunique())
            
            # Top publishers for selected account
            top_publishers = account_data['PUBLISHER'].value_counts().head(25)
            fig = px.bar(x=top_publishers.index, y=top_publishers.values,
                         title=f'Top Publishers for {selected_account}')
            st.plotly_chart(fig, use_container_width=True)

def create_asset_reports(df):
    """Create detailed asset reports"""
    st.header("💻 Asset Analysis Reports")
    top_n = st.session_state['top_n']
    # Asset summary
    if len(df) > 0:
        asset_summary = df.groupby(['NAME', 'ASSETUUID']).agg({
            'PUBLISHER': 'nunique',
            'CATEGORY': 'nunique',
            'PRODUCTNAME': 'nunique',
            'SOFTWARETYPE': 'nunique'
        }).reset_index()
        
        asset_summary.columns = ['NAME', 'ASSETUUID', 'Publishers', 'Categories', 'Products', 'Software_Types']
        
        # Asset distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(asset_summary, x='Products', nbins=20,
                              title='Distribution of Software per Asset')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(asset_summary.head(top_n), x='Products', y='Publishers',
                            size='Categories', color='NAME',
                            title='Asset Software Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Top assets
        st.subheader("Top Assets by Software Count")
        top_assets = asset_summary.nlargest(top_n, 'Products')
        st.dataframe(top_assets)
        
        # Asset drill-down
        st.subheader("Asset Drill-Down Analysis")
        selected_asset = st.selectbox("Select Asset for Detailed Analysis", 
                                     df['ASSETUUID'].unique())
        
        if selected_asset:
            asset_data = df[df['ASSETUUID'] == selected_asset]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Software", len(asset_data))
                st.metric("Unique Publishers", asset_data['PUBLISHER'].nunique())
            
            with col2:
                st.metric("Unique Categories", asset_data['CATEGORY'].nunique())
                st.metric("Unique Products", asset_data['PRODUCTNAME'].nunique())
            
            with col3:
                st.metric("Software Types", asset_data['SOFTWARETYPE'].nunique())
                st.metric("Accounts", asset_data['NAME'].nunique())
            
            # Software distribution for selected asset
            software_dist = asset_data['SOFTWARETYPE'].value_counts()
            fig = px.pie(software_dist, values=software_dist.values, names=software_dist.index,
                         title=f'Software Type Distribution for Asset {selected_asset}')
            st.plotly_chart(fig, use_container_width=True)
    

def create_export_options(df):
    """Create data export options"""
    st.header("📤 Data Export Options")

    if len(df) > 0:
    
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("CSV Export")
            if st.button("Export to CSV"):
                df.to_csv('software_assets_export.csv', index=False)
                st.success("Data exported to CSV!")
        
        with col2:
            st.subheader("Excel Export")
            if st.button("Export to Excel"):
                with pd.ExcelWriter('software_assets_export.xlsx') as writer:
                    df.to_excel(writer, sheet_name='Software_Assets', index=False)
                st.success("Data exported to Excel!")
        
        with col3:
            st.subheader("JSON Export")
            if st.button("Export to JSON"):
                df.to_json('software_assets_export.json', orient='records', indent=2)
                st.success("Data exported to JSON!")
    
