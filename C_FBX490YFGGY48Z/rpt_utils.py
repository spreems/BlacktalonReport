import streamlit as st
import pandas as pd
from collections import defaultdict

import comprehensive_soft_dashboard

def session_start():
    st.session_state['wrk_rpt_fltr_col_df'] = pd.DataFrame(columns=['COL_NAME','VALUE','SHOW','FILTER','FILTERED','CHECKED','KEY_PREFIX','DT_ADDED','DT_REMOVED'])
    st.session_state['wrk_rpt_fltr_df'] = pd.DataFrame(columns=['COLUMN_NAME','VALUE','SHOWHIDE', 'CHECKED'])


def rpt_sidebar_filters(df,col_name,lbl_name,key_prefix):
    #  Once Filter is selected KPXXX*X is Appended to df and rows are marked True based on selection in set_check_box
    fltr = comprehensive_soft_dashboard.set_check_box(df,col_name,lbl_name,key_prefix)
    st.session_state.filtered_df_001 = df
    filtered_df_001 = df
    return filtered_df_001


def filter_setup(df,col_name,key_prefix):
    if 'wrk_rpt_fltr_col_df' is st.session_state:
        wrk_df = st.session_state['wrk_rpt_fltr_col_df']
    else:
        wrk_df = pd.DataFrame()
    # col_name = 'NAME'
    chk_col = sorted(df[col_name].dropna().unique())
    # if 'curr_fltr_selected' in st.session_state:
    #     key_prefix = st.session_state['curr_fltr_selected']
    df_unique = pd.DataFrame({
        'COL_NAME': col_name,  #['NAME'] * len(chk_col),
        'VALUE': chk_col,
        'SHOW': False,
        'FILTER': False,
        'FILTERED': False,
        'CHECKED': False,
        "KEY_PREFIX":key_prefix,
        "PREV_VISIBLE": False
        
    })
    
    if 'wrk_rpt_fltr_col_df' not in st.session_state:
        st.session_state['wrk_rpt_fltr_col_df'] = wrk_df
    st.session_state['wrk_rpt_fltr_col_df']  = pd.concat([st.session_state['wrk_rpt_fltr_col_df'], df_unique], ignore_index=True)



def filter(df001,df002):       #col_name = None, value = None, change_log_df = None):
    """
    Filter function that maintains filter context across iterations.
    
    Filter Logic:
    - OR within each col_name: Multiple values for the same column are combined with OR
      Example: PUBLISHER in [Malwarebytes, Microsoft] means either value
    - AND across different col_name sets: Different columns are combined with AND
      Example: (PUBLISHER in [Malwarebytes, Microsoft]) AND (SOFTWARETYPE in [WindowsApps, Application])
    
    This ensures that:
    - Each column filter acts as a set with OR logic internally
    - Different column filters are combined with AND logic
    """
    UNIQUE_COL_NAMES = df002['COL_NAME'].unique().tolist()
    UNIQUE_KEY_PREFIX = df002['KEY_PREFIX'].unique().tolist()
    distinct_pairs = df002[['COL_NAME', 'KEY_PREFIX']].drop_duplicates().reset_index(drop=True)

    # Reset all key_prefix columns to False before applying filters
    # This ensures clean state for each filter iteration
    for key_prefix in UNIQUE_KEY_PREFIX:
        df002[key_prefix] = False
    
    # Collect all active filters from change_log, grouped by col_name
    # Each col_name represents a set with OR logic (multiple values within same column)
    # Different col_name sets are combined with AND logic
    
    # Group filters by col_name: {col_name: [list of values]}
    filters_by_column = defaultdict(list)
    
    for _, row in st.session_state.change_log.iterrows():
        col_name = row["col_name"]
        col_value = row["key"]
        filter_value = row.get("filter", False)
        
        # Only process filters that are active (filter == True)
        if filter_value:
            filter_row = df002[(df002['COL_NAME'] == col_name) & 
                               (df002['VALUE'] == col_value) & 
                               (df002['FILTER'] == True)]
            if not filter_row.empty:
                # Group by col_name - same column values will be combined with OR
                filters_by_column[col_name].append(col_value)
    #         st.write(filter_row)
    # st.write(filters_by_column)
    # st.write(f"Filters by Column (OR within column, AND across columns): {dict(filters_by_column)}")
    
    # Step 1: Apply all filters to df001
    # Logic: OR within each col_name set, AND across different col_name sets
    # Example: (PUBLISHER in [Malwarebytes, Microsoft]) AND (SOFTWARETYPE in [WindowsApps, Application])
    filtered_df001 = df001.copy()
    
    if filters_by_column:
        # Apply each column filter set with AND logic
        # Each col_name filter uses OR logic (isin) for its values
        for col_name, filter_values in filters_by_column.items():
            # Validate that the column exists in df001
            if col_name in df001.columns:
                # Apply OR logic: filter where column value is in the list of filter values
                # This means: PUBLISHER in [Malwarebytes, Microsoft] (OR)
                filtered_df001 = filtered_df001[filtered_df001[col_name].isin(filter_values)]
                # st.write(f"Applied filter: {col_name} IN {filter_values} -> {len(filtered_df001)} rows remaining")
            # else:
            #     st.warning(f"Column '{col_name}' not found in df001. Skipping filter.")
        
        # st.write(f"Final filtered df001 rows after applying all filters: {len(filtered_df001)}")
    # else:
    #     # No active filters - show all options
    #     st.write("No active filters - showing all options")

    # st.write(filtered_df001)
    
    # Step 2: For each column, find values that exist in the filtered df001
    # This maintains the filter context by showing only valid options
    if not filtered_df001.empty:
        for _, row1 in distinct_pairs.iterrows():
            col_name1 = row1["COL_NAME"]
            key_prefix1 = row1["KEY_PREFIX"]
            # st.write(f"316 -> {col_name1}  -> {key_prefix1}")
            # Validate that the column exists in df001
            if col_name1 in filtered_df001.columns:
                # Get unique values from the filtered df001 for the current column
                # FIXED: Extract just the values, not tuples
                fltr_vals = filtered_df001[col_name1].dropna().unique().tolist()
                
                if fltr_vals:
                    # st.write(f"329 Column: {col_name1} -> Valid values: {fltr_vals}")
                    # Update df002: set key_prefix1 to True for matching values
                    # This maintains the filter context by marking visible options
                    mask = (df002['COL_NAME'] == col_name1) & (df002['VALUE'].isin(fltr_vals))
                    df002.loc[mask, key_prefix1] = True
                    # st.write(df002)
            # else:
            #     st.warning(f"Column '{col_name1}' not found in df001. Skipping.")

    # Calculate VISIBLE column based on any active key_prefix
    # This uses OR logic: visible if any key_prefix column is True
    df002['VISIBLE'] = df002[UNIQUE_KEY_PREFIX].any(axis=1)
    df002['VISIBLE'] = df002['VISIBLE'].fillna(False)
   
#     # st.write("Final df002:")
#     # st.write(df002)


def resetFilter_reRenderData(filter_df):
        # df = st.session_state.rpt_data_df
        filtered_df_001 = st.session_state.filtered_df_001
        if 'wrk_rpt_fltr_col_df' in st.session_state:
            # st.write(filtered_df_001)
            for _, row in filter_df.iterrows():
                key_prefix = str(row["KP"])
                if key_prefix in filtered_df_001.columns:
                    filtered_df_001.drop(columns=[key_prefix], inplace=True)
                if key_prefix in st.session_state.rpt_data_df.columns:
                    st.session_state.rpt_data_df.drop(columns=[key_prefix], inplace=True)
                if key_prefix in st.session_state.wrk_rpt_fltr_col_df.columns:
                    st.session_state.wrk_rpt_fltr_col_df.drop(columns=[key_prefix], inplace=True)
                if key_prefix in st.session_state.fltr_wrk_df.columns:
                    st.session_state.fltr_wrk_df.drop(columns=[key_prefix], inplace=True)
                filter_setup(st.session_state.rpt_data_df,row["COLUMN_NAME"],key_prefix)

            
            st.session_state.wrk_rpt_fltr_col_df[["SHOW", "FILTER", "FILTERED","CHECKED","PREV_VISIBLE","VISIBLE", "DISABLED"]] = False
            st.session_state.fltr_wrk_df[["SHOW", "FILTER", "FILTERED","CHECKED","PREV_VISIBLE","VISIBLE", "DISABLED"]] = False
            # del st.session_state['wrk_rpt_fltr_col_df']
            # UNIQUE_COL_NAMES = df['COL_NAME'].unique().tolist()
            del st.session_state.first_in_change_log
            if 'active_KP' in st.session_state:
                del st.session_state['active_KP']
            # st.write(filtered_df_001)
            for item in st.session_state['unique_fltr_col_name']:
                session_rpt_fltr_var = 'rpt_fltr_' + item
                # st.write(session_rpt_fltr_var)
                del st.session_state[session_rpt_fltr_var] 
                
            del st.session_state.change_log
            # st.write(st.session_state.rpt_data_df)    
    
def create_df():
    data = [    {   
                    "id": 1,
                    "Level": 0,
                    "Name": "Account Asset Report", 
                    "reportId": "R101",
                    "CATALOG_ID": "BLACKTALON", 
                    "SCHEMA_ID": "SALESFORCE",
                    "TABLE_ID": "ACCOUNT",
                    "COLUMN_ID": "2574",
                    "COLUMN_NAME": "NAME",
                    "LABEL_ID": "LBL001", 
                    "LABEL_NAME": "Account Name",
                    "DIST": True,
                    "SUM": False,
                    "AVG": False,
                    "KP": "KPACT"
                },
                {
                    "id": 2,
                    "Level": 1,
                    "Name": "Account Asset Report",
                    "reportId": "R101",
                    "CATALOG_ID": "BLACKTALON",
                    "SCHEMA_ID": "SALESFORCE",
                    "TABLE_ID": "SOFTWARETABLE",
                    "COLUMN_ID": "2683",
                    "COLUMN_NAME": "PUBLISHER",
                    "LABEL_ID": "LBL002",
                    "LABEL_NAME": "Publisher",
                    "DIST": True,
                    "SUM": False,
                    "AVG": False,
                    "KP": "KPPUB"
                },
                {
                    "id": 3,
                    "Level": 2,
                    "Name": "Account Asset Report",
                    "reportId": "R101",
                    "CATALOG_ID": "BLACKTALON",
                    "SCHEMA_ID": "SALESFORCE",
                    "TABLE_ID": "SOFTWARETABLE",
                    "COLUMN_ID": "2683",
                    "COLUMN_NAME": "CATEGORY",
                    "LABEL_ID": "LBL003",
                    "LABEL_NAME": "Category",
                    "DIST": True,
                    "SUM": False,
                    "AVG": False,
                    "KP": "KPCAT"
                },
                {
                    "id": 4,
                    "Level": 3,
                    "Name": "Account Asset Report",
                    "reportId": "R101",
                    "CATALOG_ID": "BLACKTALON",
                    "SCHEMA_ID": "SALESFORCE",
                    "TABLE_ID": "SOFTWARETABLE",
                    "COLUMN_ID": "2687",
                    "COLUMN_NAME": "CATEGORY2",
                    "LABEL_ID": "LBL003",
                    "LABEL_NAME": "Category2",
                    "DIST": True,
                    "SUM": False,
                    "AVG": False,
                    "KP": "KPCATTWO"
                },
                {
                    "id": 5,
                    "Level": 4,
                    "Name": "Account Asset Report",
                    "reportId": "R101",
                    "CATALOG_ID": "BLACKTALON",
                    "SCHEMA_ID": "SALESFORCE",
                    "TABLE_ID": "SOFTWARETABLE",
                    "COLUMN_ID": "2688",
                    "COLUMN_NAME": "SOFTWARETYPE",
                    "LABEL_ID": "LBL002",
                    "LABEL_NAME": "Software Type",
                    "DIST": True,
                    "SUM": False,
                    "AVG": False,
                    "KP": "KPSWT"
                },
                {
                    "id": 6,
                    "Level": 5,
                    "Name": "Account Asset Report",
                    "reportId": "R101",
                    "CATALOG_ID": "BLACKTALON",
                    "SCHEMA_ID": "SALESFORCE",
                    "TABLE_ID": "SOFTWARETABLE",
                    "COLUMN_ID": "2688",
                    "COLUMN_NAME": "CATEGORY1",
                    "LABEL_ID": "LBL002",
                    "LABEL_NAME": "Category1",
                    "DIST": False,
                    "SUM": False,
                    "AVG": False,
                    "KP": "KPCATONE"
                }
            
            ]
    df = pd.DataFrame(data)
    return df
