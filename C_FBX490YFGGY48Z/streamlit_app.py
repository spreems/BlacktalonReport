import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import datetime, date
import json
from snowflake.snowpark.context import get_active_session

import rpt_utils
import comprehensive_soft_dashboard

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Include your CSS file in the Streamlit app
load_css("bi_style.css")

# Set page config
st.set_page_config(
    page_title="Field Selector App",
    page_icon="📊",
    layout="wide"
)

########################################################################################################################

# Initialize session state
if "checked" not in st.session_state:
    st.session_state.checked = set()
if "expanded" not in st.session_state:
    st.session_state.expanded = set()
if "search" not in st.session_state:
    st.session_state.search = set()
if "disabled" not in st.session_state:
    st.session_state.disabled = {}

def handle_srch_change(fld=None):
    st.write(f"39 FieldName: {fld}")
    value = st.session_state.get(fld, "")
    st.write(f"40 sa --> {value} ")
    st.session_state[fld] = value
    st.write(st.session_state[fld])
    st.session_state['curr_fld_changed'] = fld
    
    
def searchForm(df):
    st.write(f"searchForm",df)
    with st.form("search_form"):
        # st.write("Enter search criteria:")
        search_inputs = {}

        srch_a, srch_b = st.columns([0.90,0.1])

        with srch_a:
            cols = st.columns(4)
            col_index = 0
        
            for _, row in df.iterrows():
                field_label = row["LABEL_NAME"]
                field_type = row["DATA_TYPE"]
                field_whr = row["COLUMN_NAME_WHR"]
        
                with cols[col_index]:
                    if field_type == "VARCHAR":
                        # For text fields
                        # search_inputs[field_whr] = st.text_input(field_label, key=field_whr, on_change=handle_srch_change, kwargs={"fld":field_whr}, label_visibility="collapsed", placeholder=f"Enter {field_label}")
                        search_inputs[field_whr] = st.text_input(field_label, key=field_whr, label_visibility="collapsed", placeholder=f"Enter {field_label}")
                    elif field_type == "NUMBER":
                        # For number fields (string-based entry to allow custom IDs)
                        search_inputs[field_whr] = st.text_input(field_label, key=field_whr,label_visibility="collapsed", placeholder=f"Enter {field_label}")
                    else:
                        search_inputs[field_whr] = st.text_input(field_label, key=field_whr,label_visibility="collapsed", placeholder=f"Enter {field_label}")
        
                col_index = (col_index + 1) % 4
            # if 'prev_values' not in st.session_state:
            #     changed = [k for k in search_inputs if st.session_state.get("prev_values", {}).get(k) != st.session_state[k]]
            #     st.session_state.prev_values = {k: st.session_state[k] for k in search_inputs}
            # if st.session_state.get("prev_values", {}):
            #     st.write('Empty')
        with srch_b:
            submitted = st.form_submit_button("🔍")
            
    
        # --- AFTER SUBMIT ---
        if submitted:
            db_Name = 'BLACK_TALON' 
            sch_Name= 'PROD'    
            sp_Name = 'ACCOUNT_ASSET_SOFTWARE'
            
            # Filter out only filled values
            filters = {k: v for k, v in search_inputs.items() if str(v).strip() not in ("", "0", "None")}
            st.session_state['search_arguments'] = (json.dumps(filters))
            # st.write(st.session_state['search_arguments'])
            df = getReportData(db_Name,sch_Name,sp_Name,st.session_state.limit)
          

    

def getReportFlds(sql_prod_id):
    strsql = "CALL ZERODB.CORE.SP_RPT_FLD_BY_SQL_PROC_ID_QRY("+ str(sql_prod_id) +");"  
    setSessionStates(strsql, 'rpt_fld', 'ZDB_ID', 'qry')
    
    return st.session_state['rpt_fld_df']

def getReportData(db_Name,sch_Name,sp_Name,limit):
    # Calling Functions    searchForm
    # st.write(sp_Name)
    if 'search_arguments' in st.session_state:
        # st.write(st.session_state.search_arguments)
        input_arg = '\'VARIANT\', \' '+ str(st.session_state.search_arguments)  +'\', \'T254_NAME ASC\' ,' + str(limit) +',1'  #T253_ASSETUUID
    else:
         input_arg = '\'VARIANT\', \'NONE\', \'\' ,' + str(limit) +',1'      
    strsql = "CALL " + str(db_Name) +"." + str(sch_Name) + "." + str(sp_Name) + "("+ input_arg +");"  
    # st.write(strsql)
    # st.session_state['wrk_rpt_fltr_col_df'] = []
    setSessionStates(strsql, 'rpt_data', 'ZDB_ID', 'qry')
    st.session_state['sp_Name'] = sp_Name
    st.session_state['new_query'] = True
    # st.write(st.session_state['rpt_data_df'])
    st.session_state['srch_call_date_time'] = datetime.now()
    # st.write(st.session_state['rpt_data_df'])
    st.session_state['srch_performed'] = 'New'
    # rpt_utils.filter(st.session_state['rpt_data_df'],st.session_state['wrk_rpt_fltr_col_df'])
    return st.session_state['rpt_data_df']
    

# Convert Snowflake collection to DataFrame
def collect_2_df(collection):
    data = [row.asDict() for row in collection]
    pandas_df = pd.DataFrame(data)
    return pandas_df

#e1e5e9
def style_dataframe(df):
    return df.style.apply(lambda x: ['background-color: #faf7fc' if x.name % 2 == 0 else '' for i in x], axis=1)\
               .set_properties(**{
                   'text-align': 'left',
                   'font-size': '12px',
                   'font-family': 'Arial, Helvetica, sans-serif'
               })\
               .set_table_styles([
                   {
                       'selector': 'td', 
                       'props': [
                           ('padding', '5px'),
                           ('font-size', '12px'),
                           ('font-family', 'Arial, Helvetica, sans-serif'),
                           ('border', '1px solid #a82a03')
                       ]
                   },
                   {
                       'selector': 'th', 
                       'props': [
                           ('padding', '5px'),
                           ('font-size', '13px'),
                           ('font-family', 'Arial, Helvetica, sans-serif'),
                           ('font-weight', 'bold'),
                           ('background-color', '#a82a03'),
                           ('color', 'white'),
                           ('text-align', 'center'),
                           ('border', '1px solid #a8032d')
                       ]
                   }
               ])


    
   
# Set session states
def setSessionStates(sql, obj, lstCol, objOp):
    # sslstVar = obj + '_list'
    ssdfVar = obj + '_df'
    ssdelVar = obj + '_' + objOp
    sswrkdfVar = 'wrk_' + obj + 'df'
    session = get_active_session()
    tblCollect = session.sql(sql).collect()
    st.session_state[ssdelVar] = False
    pandas_df = collect_2_df(tblCollect)
    if len(pandas_df) > 0:
        st.session_state[sswrkdfVar] = pandas_df
        # col2list = pandas_df[lstCol].tolist()
        # st.session_state[sslstVar] = col2list
        st.session_state[ssdfVar] = pandas_df
        st.session_state['rpt_df_col_list'] = list(pandas_df.columns)
        # st.write(st.session_state.rpt_df_col_list)        

# Function to build hierarchical data structure from fetched Database
def build_hierarchy(df):
    # Create a dictionary of nodes where the key is the folder ID
    node_dict = {row['ZDB_FOLDERS_ID']: {'id': str(row['ZDB_FOLDERS_ID']), 'name': row['NAME'], 'children': [], 'parent_id': row['ZDB_PARENT_ID']} for _, row in df.iterrows()}
    
    root_nodes = []
    # Loop through the DataFrame and assign children to their respective parent nodes
    for _, row in df.iterrows():
        node = node_dict[row['ZDB_FOLDERS_ID']]
        if row['ZDB_PARENT_ID'] == 0:
            # If the parent ID is 0, it's a root node
            root_nodes.append(node)
        else:
            # Otherwise, find the parent node and add this node to its children
            parent_node = node_dict.get(row['ZDB_PARENT_ID'])
            if parent_node:
                parent_node['children'].append(node)
    
    return root_nodes
    
def build_hierarchy_fdl(df):
    # Create a dictionary of nodes where the key is the folder ID
    node_dict = {row['PARENT_ID']: {'id': str(row['PARENT_ID']), 'name': row['LABEL_NAME'], 'children': [], 'parent_id': row['CHILD_ID']} for _, row in df.iterrows()}
    
    root_nodes = []
    # Loop through the DataFrame and assign children to their respective parent nodes
    for _, row in df.iterrows():
        node = node_dict[row['PARENT_ID']]
        if row['CHILD_ID'] == 0:
            # If the parent ID is 0, it's a root node
            root_nodes.append(node)
        else:
            # Otherwise, find the parent node and add this node to its children
            parent_node = node_dict.get(row['CHILD_ID'])
            if parent_node:
                parent_node['children'].append(node)
    st.session_state['root_nodes'] = root_nodes
    
    return root_nodes

# Callback functions
def toggle_checked(key, parent_id):
    if key in st.session_state.checked:
        st.session_state.checked.remove(key)
        # Enable siblings
        if parent_id in st.session_state.disabled:
            del st.session_state.disabled[parent_id]
    else:
        st.session_state.checked.add(key)
        # Disable siblings
        st.session_state.disabled[parent_id] = key

    # Debug: print the current state of checked and disabled
    st.write("Checked items:", list(st.session_state.checked))
    st.write("Disabled items:", st.session_state.disabled)

def toggle_expanded(key):
    # st.write('142  Key: ' + key)
    if key in st.session_state.expanded:
        st.session_state.expanded.remove(key)
    else:
        st.session_state.expanded.add(key)
    # st.write(st.session_state.expanded)

def toggle_search(key):
    # st.write('142  Key: ' + key)
    if key in st.session_state.search:
        st.session_state.search.remove(key)
    else:
        st.session_state.search.add(key)
    # st.write(st.session_state.search)

# Recursive function to collect checkboxes and labels
def collect_checkboxes(nodes, parent_id=None, level=0):
    # st.write(datetime.now())
    max_columns = 2  # Set a maximum number of columns based on your page width   10
    indent_width = max_columns // 1 # Adjust this to set the space per level to reduce increase count.  8
    indent_width = 1
    # st.write(nodes)
    elements = []
    for node in nodes:
        key = node['id']
        k1 = key+'-expanded'
        k2 = key+'-search'
        # st.write('162   :  ' + key+'-expanded')
        # st.write(st.session_state.checked)
        # st.write(st.session_state.expanded)
        # is_checked = key in st.session_state.checked
        is_checked = st.session_state.get(k1, False)
        is_expanded = st.session_state.get(k1, False)
        is_searchable = st.session_state.get(k2, False)
        # is_expanded = key in st.session_state.expanded
        is_disabled = parent_id in st.session_state.disabled and st.session_state.disabled[parent_id] != key
        
        # Calculate the number of columns to indent
        num_cols = min(level * indent_width, max_columns - 1)
        # elements.append((num_cols, key, node['name'], is_expanded, is_checked, 'children' in node, is_disabled, node['parent_id']))
        elements.append((num_cols, key, node['name'], is_expanded, is_checked, 'children' in node, is_disabled, node['parent_id'],is_searchable))
        
        if is_expanded and 'children' in node:
            elements.extend(collect_checkboxes(node['children'], key, level + 1))
    return elements

# Render the collected checkboxes and labels
def render_elements(elements):
    max_columns = 2  # Set a maximum number of columns based on your page width     10

    with st.sidebar.expander("📊 Field Selector", expanded=False):        

        for num_cols, key, label, is_expanded, is_checked, has_children, is_disabled, parent_id,is_searchable in elements:
            # st.write('num_cols:  ' +str(num_cols) +' - key ' + str(key) +' -label: ' + str(label) +' -is_expanded: ' + str(is_expanded) +' -is_checked: ' + str(is_checked) +' -has_children: ' + str(has_children) +' -is_disabled: ' + str(is_disabled) +' -parent_id: ' + str(parent_id))
            keyExpanded =f"{key}-expanded"
            keySearch =f"{key}-search"
            # st.write('300 : ' + keyExpanded  + '  - ' + keySearch)
            if num_cols == 0:
                # with st.sidebar:
                with st.container():
                    col1, col2,col3 = st.columns([0.90, 0.01,0.09], border=False)
        #col1 = st.sidebar.columns(1,border=True)
        #with cols[num_cols]: 
                    with col1:
                        if has_children:
                            # st.write('126')
                            st.checkbox(
                                label, 
                                key= keyExpanded, 
                                value=is_expanded,
                                on_change=toggle_expanded,
                                args=(keyExpanded,),
                                disabled=is_disabled
                            )
                    with col3:
                        st.write("⌕")
            if num_cols == 1:
                # with st.sidebar:
                with st.container():            
                    col11, col21, col31 = st.columns([0.02, 0.90,0.08],border=False)
                    with col21:    
                        if has_children:
                            # st.write('149')
                            st.checkbox(
                                label, 
                                key=keyExpanded, 
                                value=is_expanded,
                                on_change=toggle_expanded,
                                args=(keyExpanded,),
                                disabled=is_disabled
                            )
                    with col31:
                        st.checkbox(
                                '', 
                                key=keySearch, 
                                value=is_searchable,
                                on_change=toggle_search,
                                args=(keySearch,),
                                disabled=is_disabled
                            )



########################################################################################################################


def act_cat2(df):

    account_category2_summary = df.groupby(["NAME", "CATEGORY2"]).agg(
        ASSET_ID_Count=("ASSETUUID", "nunique"),
        SF_TYPE_Count=("SOFTWARETYPE", "nunique")
    ).reset_index()
    st.write(account_category2_summary)

def main():
    st.subheader("📊 Account Asset Software Report")

    # Sidebar
    # Fetch and process data from Snowflake
    # st.sidebar.subheader("📊 Field Selector")
    # folders_df = getFolders()
    
    # data = build_hierarchy(folders_df)
    # st.write("367 sa Main :     " +  str(datetime.now()))
# ---------     START    --------- FIELD SELECTOR BASED ON REPORT FIELDS ID  : ZERODB.CORE.SP_RPT_FLD_BY_SQL_PROC_ID_QRY  sql_prod_id
    if 'rpt_fld_df' not in st.session_state:
        rpt_fld_df = getReportFlds(5)
    else:
        rpt_fld_df = st.session_state.rpt_fld_df

    # st.write(rpt_fld_df)
    
    if 'root_nodes' not in st.session_state:
        data = build_hierarchy_fdl(rpt_fld_df)
    else:
        data = st.session_state['root_nodes']
    
    # Collect elements
    elements = collect_checkboxes(data)
    
    # st.write(elements)
    # Render elements
    render_elements(elements)
    # st.dataframe(elements)
    if len(elements) > 0 :
        elements_col = ['num_cols', 'key', 'label', 'is_expanded', 'is_checked', 'has_children', 'is_disabled', 'parent_id','is_searchable']
        x= pd.DataFrame(elements, columns=elements_col)
        filtered_x = x[x["parent_id"] != 0]
        # st.write(filtered_x)
        rpt_df_lst_unchkd = filtered_x[filtered_x["is_checked"] == False ]
        hidden_cols = [label.upper() for label in rpt_df_lst_unchkd["label"].tolist()]
        # st.write(hidden_cols)
# ---------     END    --------- FIELD SELECTOR BASED ON REPORT FIELDS ID  : ZERODB.CORE.SP_RPT_FLD_BY_SQL_PROC_ID_QRY  sql_prod_id

        
    # st.sidebar.title("📋 Navigation")
    with st.sidebar.expander("☸ Navigation", expanded=False):    
        page = st.selectbox(
            "Select Page",
            ["Overview Dashboard", "Account Reports", "Asset Reports", "Data Export"]
        )        


# ---------     START    ---------   Identifies the  Search Field Parent ID and Calls to Build Search Form
    lst_expanded = {item.replace("-expanded", "") for item in st.session_state.expanded}
    lst_search = {int(item.replace("-search", "")) for item in st.session_state.search}
    # st.write('lst_expanded ' + str(lst_expanded))
    # st.write('lst_search ' + str(lst_search))
    search_df = rpt_fld_df[rpt_fld_df["PARENT_ID"].isin(lst_search)]
    # st.write(search_df)
    # st.write(len(search_df))
    
    # Main body
    # st.header("📋 Field Types and Data")
    
    # Create expander for field types
    if len(search_df) > 0:
        with st.expander("🔍 Search", expanded=False):
            searchForm(search_df)
# ---------     END    ---------   Identifies the  Search Field Parent ID and Calls to Build Search Form

# --------- START  Commented, not sure if it's in use   --------- #
    # # Get selected fields
    # selected_fields = []
    # for data_type, fields in FIELD_TYPES.items():
    #     for field in fields:
    #         if st.session_state.get(f"field_{data_type}_{field}", False):
    #             selected_fields.append(field)
# --------- END    Commented not sure if it's in use   --------- #                
    
    db_Name = 'BLACK_TALON' 
    sch_Name= 'PROD'    
    sp_Name = 'ACCOUNT_ASSET_SOFTWARE'
    limit = st.sidebar.number_input("Limit:", min_value=1, max_value=1000000, value=500, step=1)
    st.session_state.limit = limit

# --------- START    Commented not sure if it's in use   --------- #     
    if 'rpt_data_df' not in st.session_state:
        #   Called On Load with a Default Search and default limit  st.session_state.limit  set as 1000
        st.session_state['first_call_date_time'] = datetime.now()
        # st.write('sa  _ 438')
        df = getReportData(db_Name,sch_Name,sp_Name,limit)
        # if 'wrk_rpt_fltr_col_df' in st.session_state:
        #     st.write(f" 446 sa ")
        #     st.write(st.session_state['wrk_rpt_fltr_col_df'])        
        # st.write(df)
    else:
        # df is set to active rpt_data_df  ( Existing / New Searched Data)
        # st.write('sa  _ 440')
        # st.write(st.session_state['srch_performed'])
        # st.write(st.session_state['rpt_data_df'])
        df = st.session_state['rpt_data_df']
        if st.session_state['srch_performed'] == 'New':
            st.session_state.filtered_df_001 = df
            st.session_state['srch_performed'] = 'Old'
        # st.write("459 sa Main :     " +  str(datetime.now()))
    # st.write('first_call_date_time   :  ' + str(st.session_state.first_call_date_time) + 'st.session_state.srch_call_date_time' + str(st.session_state.srch_call_date_time)  +  ' NOW ' + str(datetime.now()))
    # st.write(df)
    
# --------- END    Commented not sure if it's in use   --------- #     
           
    with st.sidebar.expander("🔍 Filter", expanded=False):
        # st.write("465 sa Main :     " +  str(datetime.now()))
        st.session_state.submitted = True
        if 'fltr_wrk_df' in st.session_state:
            st.session_state.submitted = False
        clear_fltr = st.button("↺  Reset Filter", disabled = st.session_state.submitted )

        
        # fltr001,fltr002 =st.columns([0.6,0.4])
        # with fltr001:
        #     st.write('abcd')
        # with fltr002:
            # with st.form("clear_form"):
            # clr_fltr = st.button("⟳ Clear Filter")
            #     # --- AFTER SUBMIT ---
            # if clr_fltr:
            #     st.write('Clear Fltr')
        # if st.session_state['new_query'] == True:        
        filter_df = rpt_utils.create_df()
        if clear_fltr:
            for _, row in filter_df.iterrows():
                key_prefix = str(row["KP"])            
                for key in st.session_state.keys():
                     if isinstance(key, str) and key.startswith(key_prefix+"_") and st.session_state[key]== True:
                         # st.write(key)
                         st.session_state[key] = False
                         # del st.session_state[key]    
            # CALL RESET FILTERS FUNCTION (filter_df)
            # st.write("489 Filters")
            # st.write(df)
            rpt_utils.resetFilter_reRenderData(filter_df)
            

# --------- START    PRE_SET wrk_rpt_fltr_col_df DF   --------- #
        # COLUMNS :- COL_NAME, VALUE, SHOW, FILTER,FILTERED,CHECKED,KEY_PREFIX, DISABLED,DT_ADDED
        # st.session_state['wrk_rpt_fltr_col_df'] Controls checkbox for filters to be enabled/disabled
        if 'new_query' in st.session_state and  st.session_state['new_query'] == True:
            if 'wrk_rpt_fltr_col_df' in st.session_state:
                del st.session_state['wrk_rpt_fltr_col_df']
                # UNIQUE_COL_NAMES = df['COL_NAME'].unique().tolist()
                for item in st.session_state['unique_fltr_col_name']:
                    session_rpt_fltr_var = 'rpt_fltr_' + item
                    del st.session_state[session_rpt_fltr_var]                
        for _, row in filter_df.iterrows():
            key_prefix = str(row["KP"])
            if 'new_query' in st.session_state and  st.session_state['new_query'] == True:
                # if 'wrk_rpt_fltr_col_df' in st.session_state:
                #     st.write(f" 484 sa ")
                #     st.write(st.session_state['wrk_rpt_fltr_col_df'])
                #     del st.session_state['wrk_rpt_fltr_col_df']
                # st.write('  482  : ' + str(datetime.now()))
                # st.write(df)
                # st.write("498 sa Main :     " +  str(datetime.now()))
                # st.write("514 new Query")
                # st.write(df)
                
                rpt_utils.filter_setup(df,row["COLUMN_NAME"],key_prefix)
        st.session_state['unique_fltr_col_name'] = st.session_state['wrk_rpt_fltr_col_df']['COL_NAME'].unique().tolist()
        # if 'new_query' in st.session_state and  st.session_state['new_query'] == True:

        # st.write('sa 494  :  - ')
        # st.write(st.session_state['unique_fltr_col_name'])
        # st.write(st.session_state['wrk_rpt_fltr_col_df'])
        st.session_state['new_query'] = False
# --------- End    PRE_SET wrk_rpt_fltr_col_df DF   --------- #        
        df1 = df        #.copy()
        # if 'wrk_rpt_fltr_col_df' in st.session_state:
        #     st.write(f" 494 sa ")
        #     st.write(st.session_state['wrk_rpt_fltr_col_df'])         
        for _, row in filter_df.iterrows():
            key_prefix = str(row["KP"])
            if 'filtered_df_001' in st.session_state:
                # st.write('sa - 475  ' + str(len(st.session_state.filtered_df_001)) + '  -  ' + str(datetime.now()))
                df1 = st.session_state.filtered_df_001 
            # st.write('sa  _ 517')
            # st.write(df1)
            # st.write(row["COLUMN_NAME"] + '  -- ' + row["LABEL_NAME"] + ' --- ' + key_prefix)
            # st.write("520 sa Main :     " +  str(datetime.now()))
            filtered_df_001 = rpt_utils.rpt_sidebar_filters(df1,row["COLUMN_NAME"], row["LABEL_NAME"], key_prefix)
            # st.write('sa  _ 461')
            # st.write(filtered_df_001)
            st.session_state.filtered_df_001 = filtered_df_001
            
        if 'filtered_df_001' in st.session_state:
            filtered_df_001 = st.session_state.filtered_df_001 


        st.subheader("Data Range")
        show_top_n = st.slider("Show Top N Results", 5, 50, 20)
        st.session_state['top_n'] = show_top_n

    if 'active_KP' in st.session_state:
        # st.write(st.session_state['active_KP'])
        active_KP = st.session_state['active_KP']
        # st.write(list(active_KP))
        
        # This step iterates and filters the data_set where each KP == True
        for col in active_KP:
            # filtered_df_001 = filtered_df_001[filtered_df_001[list(active_KP)].all(axis=1)]    DID not work properly
            if col in filtered_df_001.columns:
                filtered_df_001 = filtered_df_001[filtered_df_001[col] == True]
    
    # st.write('539')
    # # st.write(st.session_state.change_log)
    # st.write(filtered_df_001)

    # rpt_utils.filter(st.session_state['rpt_data_df'],st.session_state['wrk_rpt_fltr_col_df'])
    
    with st.expander("🔍 Data Analysis", expanded=True):        
        data,graph = st.columns([0.85,0.15])
        with data:
            # if 'fltr_wrk_df' in st.session_state:
            #     st.write(st.session_state['fltr_wrk_df'])
            if len(st.session_state.rpt_data_df) > 0:
                
                if 'rpt_data_df' in st.session_state:
                    styled_df = filtered_df_001             #filtered_df
            
                    column_config = {
                        col: None if col in hidden_cols else st.column_config.Column(label=col.replace("_", " "))
                        for col in styled_df.columns
                    }         
                    
                # Display dataframe with native column selection enabled
                    st. dataframe(
                        styled_df,
                        column_config=column_config,
                        use_container_width=True,
                        hide_index=True,
                        height=650        
                    )
    
                # comprehensive_soft_dashboard.load_data()
    
        with graph:
            if 'change_log' in st.session_state and len(st.session_state.change_log) > 0:
                with st.expander("📈 Applied Filter", expanded=False):
                    # clr_fltr = st.button("⟳ Clear Filter")
                        # --- AFTER SUBMIT ---
                    applied_fltr_df = st.session_state.change_log[["key_prefix","key"]].copy()
                    # st.write(st.session_state.change_log)
                    for idx, row in applied_fltr_df.iterrows():
                        kp = row["key_prefix"]
                        k  = row["key"]
                        # st.write(f"cf_{kp}_{idx}_{k}")
                        st.checkbox(row["key"], value=True, key=f"cf_{kp}_{idx}_{k}")
                        
                    if 1==2:
                        # st.write('Clear Fltr') 
                        # st.write("579 sa Main :     " +  str(datetime.now()))
                        if 'wrk_rpt_fltr_col_df' in st.session_state:
                            # st.write(filtered_df_001)
                            for _, row in filter_df.iterrows():
                                key_prefix = str(row["KP"])
                                rpt_utils.filter_setup(df,row["COLUMN_NAME"],key_prefix)
                                if key_prefix in filtered_df_001.columns:
                                    filtered_df_001.drop(columns=[key_prefix], inplace=True)
                                if key_prefix in st.session_state.rpt_data_df.columns:
                                    st.session_state.rpt_data_df.drop(columns=[key_prefix], inplace=True)
                                if key_prefix in st.session_state.wrk_rpt_fltr_col_df.columns:
                                    st.session_state.wrk_rpt_fltr_col_df.drop(columns=[key_prefix], inplace=True)
                                if key_prefix in st.session_state.fltr_wrk_df.columns:
                                    st.session_state.fltr_wrk_df.drop(columns=[key_prefix], inplace=True)
                                for key in st.session_state.keys():
                                     if isinstance(key, str) and key.startswith(key_prefix+"_") and st.session_state[key]== True:
                                         st.write(key)
                                         del st.session_state[key]
                                         # st.session_state[key] = False
                                            
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


                            st.rerun()
                        # df1 = st.session_state['rpt_data_df']                
                        # for _, row in filter_df.iterrows():
                        #     key_prefix = str(row["KP"])
                        #     if 'filtered_df_001' in st.session_state:
                        #         # st.write('sa - 475  ' + str(len(st.session_state.filtered_df_001)) + '  -  ' + str(datetime.now()))
                        #         df1 = st.session_state.filtered_df_001 
                        #     filtered_df_001 = rpt_utils.rpt_sidebar_filters(df1,row["COLUMN_NAME"], row["LABEL_NAME"], key_prefix)
                        #     st.session_state.filtered_df_001 = filtered_df_001
                
                        # if 'filtered_df_001' in st.session_state:
                        #     filtered_df_001 = st.session_state.filtered_df_001 
                    


            with st.expander("📈 Data Summary", expanded=False):        
            # # Display dataframe info
            # st.subheader("📈 Data Summary")
            
                # col1, col2, col3, col4 = st.columns(4)
            
                ds_count = 0
                ds_columns = 0
                ds_dataTypes = 0
                ds_memory = 0
            
                
                # act_cat2(st.session_state.rpt_data_df)
                # len(st.session_state.rpt_data_df)
                if 'rpt_data_df' in st.session_state:
                    ds_count = len(st.session_state.rpt_data_df)
                    ds_columns = len(st.session_state.rpt_data_df.columns)
                    ds_dataTypes = len(st.session_state.rpt_data_df.dtypes.unique())
                    ds_memory = f"{st.session_state.rpt_data_df.memory_usage(deep=True).sum() / 1024:.1f} KB"
    
                # with col1:
                    st.metric("Total Rows", ds_count)
                
                # with col2:
                    st.metric("Total Columns", ds_columns)
                
                # # with col3:
                #     st.metric("Data Types", ds_dataTypes)
                
                # with col4:
                    st.metric("Memory Usage", ds_memory)
    
    
            with st.expander("📊 KPI", expanded=True):        
                if len(filtered_df_001) > 0:
                # with col1:
                    st.metric("Total Records", f"{len(filtered_df_001):,}")
                # with col2:
                    st.metric("Unique Accounts", f"{filtered_df_001['NAME'].nunique():,}")
                # with col3:
                    st.metric("Unique Assets", f"{filtered_df_001['ASSETUUID'].nunique():,}")
                # with col4:
                    st.metric("Unique Publishers", f"{filtered_df_001['PUBLISHER'].nunique():,}")
                # with col5:
                    st.metric("Unique Categories", f"{filtered_df_001['CATEGORY'].nunique():,}")
                # with col6:
                    st.metric("Unique Products", f"{filtered_df_001['PRODUCTNAME'].nunique():,}")
    

# st.write(st.session_state.rpt_fld_df)
    # with graph:
    # filters = st.session_state["abcd"]    
    if page == "Overview Dashboard":
        comprehensive_soft_dashboard.create_overview_dashboard(filtered_df_001)
    elif page == "Account Reports":
        comprehensive_soft_dashboard.create_account_reports(filtered_df_001)
    elif page == "Asset Reports":
        comprehensive_soft_dashboard.create_asset_reports(filtered_df_001)
    # elif page == "Snowflake Integration":
    #     comprehensive_soft_dashboard.create_snowflake_integration()
    elif page == "Data Export":
        comprehensive_soft_dashboard.create_export_options(filtered_df_001)

if __name__ == "__main__":
    main()
