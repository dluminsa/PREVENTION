import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import time
import gspread
import traceback
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
from datetime import datetime, date

st.set_page_config(
     page_title= 'ACTIVITY TRACKER'
)
# st.write('BEING UPDATED, WILL RETURN AFTER THE NEW BUDGETS')
# st.stop()

CLUSTER = {
    "KALANGALA": ["KALANGALA"],
    "KYOTERA": ["KYOTERA", "RAKAI"],
     "LYANTONDE": ["LYANTONDE", "LWENGO"],
    "MASAKA": ['BUKOMANSIMBI', "KALUNGU",'MASAKA CITY', 'MASAKA DISTRICT','SEMBABULE'],
    "MPIGI": ['BUTAMBALA', 'GOMBA', 'MPIGI'],
    "WAKISO": ['WAKISO']
}

FACILITIES ={  
                "BUKOMANSIMBI":["BIGASA HC III","BUTENGA HC IV","KAGOGGO HC II","KIGANGAZZI HC II",
                              "KISOJJO HC II","KITANDA HC III","MIRAMBI HC III","ST. MARY'S MATERNITY HOME"],
                "BUTAMBALA" : ["BULO HC III","BUTAAKA HC III","EPI-CENTRESENGE HC III","GOMBE GENERAL HOSPITAL", 
                             "KALAMBA COMMUNITY HC II", "KIBUGGA HC II","KITIMBA HC III", "KIZIIKO HC II","KYABADAZA HC III",
                             "NGANDO HC III"],
                "GOMBA"  : ["BULWADDA HC II", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III"],
               "KALANGALA": ["BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II"],
                "KALUNGU" : ["AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II"
                               "KIGAJU HC II","KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II"],
                "KYOTERA" : ["KABIRA (KYOTERA) HC III""KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC"],
                "LWENGO" : ["KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO KINONI GOVT HC III","NANYWA HC III"], 
                "LYANTONDE" :["KABATEMA HC II","KABAYANDA HC II","KALIIRO HC III","KASAGAMA HC III",
                                "KINUUKA HC III","KYEMAMBA HC II","LYAKAJURA HC III","LYANTONDE HOSPITAL","MPUMUDDE HC III"],
                "MASAKA CITY": ["BUGABIRA HC II","BUKOTO HC III","KITABAAZI HC III","KIYUMBA HC IV","KYABAKUZA HC II",
                                        "MASAKA MUNICIPAL CLINIC","MASAKA POLICE HC III","MPUGWE HC III","NYENDO HC III","TASO MASAKA"],
                "MASAKA DISTRICT": ["BUKAKATA HC III","BUKEERI HC III","BUWUNGA HC III","BUYAGA HC II","KAMULEGU HC III","KYANAMUKAAKA HC IV"],
                "MPIGI" : ["BUJUUKO HC III","BUKASA HC II","BUNJAKO HC III",
                            "BUTOOLO HC III","BUWAMA HC III","BUYIGA HC III","DONA MEDICAL CENTRE","FIDUGA MEDICAL CENTRE","GGOLO HC III",
                            "KAMPIRINGISA HC III","KIRINGENTE EPI HC II","KITUNTU HC III","MPIGI HC IV","MUDUUMA HC III",
                            "NABYEWANGA HC II","NINDYE HC III","NSAMU/KYALI HC III","SEKIWUNGA HC III","ST. ELIZABETH KIBANGA IHU HC III"],
                "RAKAI" : ["BUGONA HC II","BUTITI HC II","BUYAMBA HC III","BYAKABANDA HC III",
                                    "KACHEERA HC III","KASANKALA HC II","KAYONZA KACHEERA HC II","KIBAALE HC II","KIBANDA HC III","KIBUUKA HC II",
                                    "KIFAMBA HC III","KIMULI HC III","KYABIGONDO HC II","KYALULANGIRA HC III","LWABAKOOBA HC II","LWAKALOLO HC II",
                                    "LWAMAGGWA GOVT HC III","LWANDA HC III","LWEMBAJJO HC II","MAGABI HC II","RAKAI HOSPITAL","RAKAI KIZIBA HC III",],
                "SEMBABULE":["BUSHEKA HC III","KABUNDI HC II","KAYUNGA HC II",
                                        "KYABI HC III","KYEERA HC II","LUGUSULU HC III","LWEBITAKULI HC III","LWEMIYAGA HC III","MAKOOLE HC II","MATEETE HC III",
                                        "MITIMA HC II","NTETE HC II","NTUUSI HC IV","SEMBABULE KABAALE HC II","SSEMBABULE HC IV"],
                                            
                "WAKISO" : ["BULONDO HC III","BUNAMWAYA HC II","BUSAWAMANZE HC III","BUSSI HC III","BUWAMBO HC IV","BWEYOGERERE HC III","COMMUNITY HEALTH PLAN UGANDA",
                        "GGWATIRO NURSING HOME HOSPITAL","GOMBE (WAKISO) HC II","JOINT CLINICAL RESEARCH CENTER (JCRC) HC IV",
                        "KABUBBU HC IV","KAJJANSI HC IV","KAKIRI HC III","KASANGATI HC IV","KASANJE HC III","KASENGE HC II",
                        "KASOOZO HC III","KATABI HC III","KAWANDA HC III","KIGUNGU HC III","KIMWANYI HC II","KIRA HC III",
                        "KIREKA HC II","KIRINYA (BWEYOGERERE) HC II","KITALA HC II","KIZIBA HC III","KYENGERA HC III",
                        "KYENGEZA HC II","LUBBE HC II","LUFUKA VALLEY HC III","MAGANJO HC II","MAGOGGO HC II","MATUGA HC II",
                        "MENDE HC III","MIGADDE HC II","MILDMAY UGANDA HOSPITAL","MUTUNDWE HC II","MUTUNGO HC II","NABUTITI HC III",
                        "NABWERU HC III","NAKAWUKA HC III","NAKITOKOLO NAMAYUMBA HC III","NALUGALA HC II","NAMAYUMBA EPI HC III",
                        "NAMAYUMBA HC IV","NAMUGONGO FUND FOR SPECIAL CHILDREN CLINIC","NAMULONGE HC III","NANSANA HC II",
                        "NASSOLO WAMALA HC III","NDEJJE HC IV","NSAGGU HC II","NSANGI HC III","NURTURE AFRICA II SPECIAL CLINIC",
                        "SEGUKU HC II","TASO ENTEBBE SPECIAL CLINIC","TRIAM MEDICAL CENTRE HC II","TTIKALU HC III","WAGAGAI HC IV",
                        "WAKISO BANDA HC II","WAKISO EPI HC III","WAKISO HC IV","WAKISO KASOZI HC III","WATUBBA HC III","ZZINGA HC II"]
                    
                                        }



ALL =[ "BIGASA HC III","BUTENGA HC IV","KAGOGGO HC II","KIGANGAZZI HC II",
                              "KISOJJO HC II","KITANDA HC III","MIRAMBI HC III","ST. MARY'S MATERNITY HOME",
                "BULO HC III","BUTAAKA HC III","EPI-CENTRESENGE HC III","GOMBE GENERAL HOSPITAL", 
                             "KALAMBA COMMUNITY HC II", "KIBUGGA HC II","KITIMBA HC III", "KIZIIKO HC II","KYABADAZA HC III",
                             "NGANDO HC III",
                "BULWADDA HC II", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III",
               "BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II",
                "AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II"
                               "KIGAJU HC II","KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II",
                "KABIRA (KYOTERA) HC III""KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC",
                "KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO KINONI GOVT HC III","NANYWA HC III", 
                "KABATEMA HC II","KABAYANDA HC II","KALIIRO HC III","KASAGAMA HC III",
                                "KINUUKA HC III","KYEMAMBA HC II","LYAKAJURA HC III","LYANTONDE HOSPITAL","MPUMUDDE HC III",
                "BUGABIRA HC II","BUKOTO HC III","KITABAAZI HC III","KIYUMBA HC IV","KYABAKUZA HC II",
                                        "MASAKA MUNICIPAL CLINIC","MASAKA POLICE HC III","MPUGWE HC III","NYENDO HC III","TASO MASAKA",
                "BUKAKATA HC III","BUKEERI HC III","BUWUNGA HC III","BUYAGA HC II","KAMULEGU HC III","KYANAMUKAAKA HC IV",
      "BUJUUKO HC III","BUKASA HC II","BUNJAKO HC III",
                            "BUTOOLO HC III","BUWAMA HC III","BUYIGA HC III","DONA MEDICAL CENTRE","FIDUGA MEDICAL CENTRE","GGOLO HC III",
                            "KAMPIRINGISA HC III","KIRINGENTE EPI HC II","KITUNTU HC III","MPIGI HC IV","MUDUUMA HC III",
                            "NABYEWANGA HC II","NINDYE HC III","NSAMU/KYALI HC III","SEKIWUNGA HC III","ST. ELIZABETH KIBANGA IHU HC III",
                "BUGONA HC II","BUTITI HC II","BUYAMBA HC III","BYAKABANDA HC III",
                                    "KACHEERA HC III","KASANKALA HC II","KAYONZA KACHEERA HC II","KIBAALE HC II","KIBANDA HC III","KIBUUKA HC II",
                                    "KIFAMBA HC III","KIMULI HC III","KYABIGONDO HC II","KYALULANGIRA HC III","LWABAKOOBA HC II","LWAKALOLO HC II",
                                    "LWAMAGGWA GOVT HC III","LWANDA HC III","LWEMBAJJO HC II","MAGABI HC II","RAKAI HOSPITAL","RAKAI KIZIBA HC III",
                "BUSHEKA HC III","KABUNDI HC II","KAYUNGA HC II",
                                        "KYABI HC III","KYEERA HC II","LUGUSULU HC III","LWEBITAKULI HC III","LWEMIYAGA HC III","MAKOOLE HC II","MATEETE HC III",
                                        "MITIMA HC II","NTETE HC II","NTUUSI HC IV","SEMBABULE KABAALE HC II","SSEMBABULE HC IV",
                                            
                "BULONDO HC III","BUNAMWAYA HC II","BUSAWAMANZE HC III","BUSSI HC III","BUWAMBO HC IV","BWEYOGERERE HC III","COMMUNITY HEALTH PLAN UGANDA",
                        "GGWATIRO NURSING HOME HOSPITAL","GOMBE (WAKISO) HC II","JOINT CLINICAL RESEARCH CENTER (JCRC) HC IV",
                        "KABUBBU HC IV","KAJJANSI HC IV","KAKIRI HC III","KASANGATI HC IV","KASANJE HC III","KASENGE HC II",
                        "KASOOZO HC III","KATABI HC III","KAWANDA HC III","KIGUNGU HC III","KIMWANYI HC II","KIRA HC III",
                        "KIREKA HC II","KIRINYA (BWEYOGERERE) HC II","KITALA HC II","KIZIBA HC III","KYENGERA HC III",
                        "KYENGEZA HC II","LUBBE HC II","LUFUKA VALLEY HC III","MAGANJO HC II","MAGOGGO HC II","MATUGA HC II",
                        "MENDE HC III","MIGADDE HC II","MILDMAY UGANDA HOSPITAL","MUTUNDWE HC II","MUTUNGO HC II","NABUTITI HC III",
                        "NABWERU HC III","NAKAWUKA HC III","NAKITOKOLO NAMAYUMBA HC III","NALUGALA HC II","NAMAYUMBA EPI HC III",
                        "NAMAYUMBA HC IV","NAMUGONGO FUND FOR SPECIAL CHILDREN CLINIC","NAMULONGE HC III","NANSANA HC II",
                        "NASSOLO WAMALA HC III","NDEJJE HC IV","NSAGGU HC II","NSANGI HC III","NURTURE AFRICA II SPECIAL CLINIC",
                        "SEGUKU HC II","TASO ENTEBBE SPECIAL CLINIC","TRIAM MEDICAL CENTRE HC II","TTIKALU HC III","WAGAGAI HC IV",
                        "WAKISO BANDA HC II","WAKISO EPI HC III","WAKISO HC IV","WAKISO KASOZI HC III","WATUBBA HC III","ZZINGA HC II"]
                    
ididistricts = ['BUKOMANSIMBI','BUTAMBALA', 'GOMBA','KALANGALA','KYOTERA', 'LYANTONDE', 'LWENGO', 'MASAKA CITY', 
                'MASAKA DISTRICT', 'MPIGI','RAKAI', 'SEMBABULE', 'WAKISO']                                                     

# file = r'PLANNED.csv'
# dis = pd.read_excel(file)
# dis1 = dis[dis['ORG'] == 'OTHERS'].copy()
# alldistricts = dis1['DISTRICT'].unique()
# alldistrictsidi = dis['DISTRICT'].unique()

# Title of the Streamlit app

st.markdown("<h4><b>PREVENTION   ACTIVITIES   TRACKER</b></h4>", unsafe_allow_html=True)
st.markdown('***ALL ENTRIES ARE REQUIRED**')
#sss
done = ''
district = ''

#theme = ['CARE', 'TB', 'PMTCT', 'CQI']
# Radio button to select a district

cluster = st.radio("**Choose a cluster:**", list(CLUSTER.keys()),horizontal=True, index=None)

# Show the facilities for the selected district and allow selection
if cluster is not None:
    districts = CLUSTER[cluster]
    district = st.radio(f"**Choose a district in {cluster} cluster:**", districts, horizontal=True, index=None)

cola, colb = st.columns([1,1])
with cola:
    if not district:
            st.stop()
    else:        
        facilities = FACILITIES[district]
        facility = st.selectbox(f"**Name of implementing facility in {district} district:***", facilities, index=None)


def generate_unique_number():
    f = dt.datetime.now()  # Get the current datetime
    g = f.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format datetime as a string including microseconds
    h = g.split('.')[1]  # Extract the microseconds part of the formatted string
    j = h[1:5]  # Get the second through fifth digits of the microseconds part
    return int(j)  # Convert the sliced string to an integer

# Initialize the unique number in session state if it doesn't exist
if 'unique_number' not in st.session_state:
    st.session_state['unique_number'] = generate_unique_number()

# Display the unique number


#Display the selection
with colb:
    st.write('**You selected:**')
    st.write(f"**{district} district, and {facility}**")
if not facility:
     st.stop()
else:
     pass
#area = st.radio('**CHOOSE A THEMATIC AREA**', theme, horizontal=True, index=None)

planned = r'PLANNED.csv'

dfa = pd.read_csv(planned)

# if not area:
#      st.stop()
# else:
#      pass

#activity = dfa[dfa['AREA']== area].copy()
activities = dfa['ACTIVITY'].unique()
col1,col2 = st.columns([2,1])
#if area:
done = col1.selectbox(f'**SELECT THE ACTIVITY YOU ARE PAYING FOR**', activities, index=None)
#else:
#     st.stop()


if not done:
     st.stop()
elif done:
     state = dfa[dfa['ACTIVITY']==done]
     statea = state[state['CLUSTER']== cluster].copy()
     statement = statea['STATEMENT'].unique()
     counts = statea['COUNT'].unique()
     try:
        statement = statement[0]
     except:
          st.write('THIS ACTIVITY MAY NOT HAVE BEEN PLANNED FOR THIS DISTRICT')
          st.write('CONTACT YOUR TEAM LEAD FOR SUPPORT')
          st.stop()
     #statement = statement[0]
     counts = counts[0]
     st.markdown(f'**NOTE: {statement}**')
     colt,coly,colx = st.columns([1,1,1])
     number = colt.number_input(label=f'**{counts}**', value=None, max_value=None, min_value=None,step=1, format="%d")
     start = coly.date_input(label='**ACTIVITY START DATE**', value=None)
     end = colx.date_input(label='**END DATE**',value=None)
     # Get the current date and time
current_datetime = datetime.now()
#today = current_datetime.strftime('%y/%m/%d')
today = date.today()

if number and start and end:
     if start > end:
          st.warning("IMPOSSIBLE, ACTIVITY START DATE CAN'T BE GREATER THAN END DATE")
          st.stop()
     elif end>today:
          st.warning("IMPOSSIBLE, CHECK END DATE, IT'S GREATER THAN TODAY")
          st.stop()
     else:
          pass
else:
     st.stop()
     
money = colt.number_input(label='**HOW MUCH ARE YOU PAYING?**', value=None, max_value=None, min_value=None,step=1, format="%d")
if not money:
     st.stop()
else:
     pass

st.write(f"UNIQUE ID: {st.session_state['unique_number']}")
unique = st.session_state['unique_number']
col1,col2, col3 = st.columns([1,1,2])
col2.write('**SUMMARY**')

cola,colb = st.columns(2)
cola.write(f"**UNIQUE ID: {st.session_state['unique_number']}**")
cola.markdown(f'**DISTRICT: {district}**')
cola.markdown(f'**FACILITY: {facility}**')
cola.markdown(f'**AMOUNT: {money}**')


colb.write(f'**ACTIVITY: {done}**')
colb.markdown(f'**{counts}: {number}**')
colb.markdown(f'**START DATE: {start}**')
colb.markdown(f'**END DATE: {end}**')

date = datetime.now().date()
formatted = date.strftime("%d-%m-%Y")
cola,colb = st.columns(2)
submit = cola.button('SUBMIT')
current_time = time.localtime()
week = time.strftime("%V", current_time)
week = int(week)-39
if submit:
     df = pd.DataFrame([{ 'DATE OF SUBMISSION': formatted,
                         'CLUSTER': cluster,
                         'DISTRICT':district,
                         'FACILITY' : facility,
                         'ACTIVITY': done,
                         'DONE': number,
                         'START DATE': start,
                         'END DATE': end,
                         'ID' : unique,
                         'WEEK': week
                         }]) 


secrets = st.secrets["connections"]["gsheets"]
formatted = str(formatted)
start = str(start)
end = str(end)
row1 =[ formatted, cluster,district, facility, done, number, start, end, unique, week]
row2 =[ formatted, cluster,district, money]
               
    # Prepare the credentials dictionary
credentials_info = {
        "type": secrets["type"],
        "project_id": secrets["project_id"],
        "private_key_id": secrets["private_key_id"],
        "private_key": secrets["private_key"],
        "client_email": secrets["client_email"],
        "client_id": secrets["client_id"],
        "auth_uri": secrets["auth_uri"],
        "token_uri": secrets["token_uri"],
        "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": secrets["client_x509_cert_url"]
    }
        
try:
    # Define the scopes needed for your application
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
    
     
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        
        # Authorize and access Google Sheets
    client = gspread.authorize(credentials)
        
        # Open the Google Sheet by URL
    spreadsheetu = "https://docs.google.com/spreadsheets/d/1DJHYJIw8cKZJEZX9VQO25wuXP8ROzcxY2lqT-EvHnjU/edit?gid=1527303903"     
    spreadsheet = client.open_by_url(spreadsheetu)
except Exception as e:
        # Log the error message
    st.write(f"CHECK: {e}")
    st.write(traceback.format_exc())
    st.write("COULDN'T CONNECT TO GOOGLE SHEET, TRY AGAIN")
    st.stop()
if submit:
        try:
            sheet1 = spreadsheet.worksheet("PREV")
            sheet2 = spreadsheet.worksheet("AMOUNT")
            sheet1.append_row(row1, value_input_option='RAW')
            sheet2.append_row(row2, value_input_option='RAW')
            st.success('Your data above has been submitted')
            time.sleep(2)
            st.write('RELOADING PAGE')
            time.sleep(3)
            st.markdown("""
               <meta http-equiv="refresh" content="0">
                    """, unsafe_allow_html=True)
        except Exception as e:
            # Print the error message
            st.write(f"ERROR: {e}")
            st.stop()  # Stop the Streamlit app here to let the user manually retry     
else:
     pass 















     
     # try:
     #      st. write('SUBMITING')
     #      conn = st.connection('gsheets', type=GSheetsConnection)
     #      exist = conn.read(worksheet= 'PREV', usecols=list(range(11)),ttl=5)
     #      existing= exist.dropna(how='all')
     #      updated = pd.concat([existing, df], ignore_index =True)
     #      conn.update(worksheet = 'PREV', data = updated)         
     #      st.success('Your data above has been submitted')
     #      st.write('RELOADING PAGE')
     #      time.sleep(3)
     #      st.markdown("""
     #      <meta http-equiv="refresh" content="0">
     #           """, unsafe_allow_html=True)

     # except:
     #      st.write("Couldn't submit, poor network") 
     #      st.write('Click the submit button again')











