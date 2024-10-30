import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import numpy as np
import time
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

numbers = []
dates = []
weeks = []
areas = []
starts= []
ends = []
activit = []
clusters = []
uniques = []
facilitiesy = []

st.markdown("<h4><b>PLANNED    ACTIVITIES   TRACKER</b></h4>", unsafe_allow_html=True)
st.markdown("<h6><b>USE THIS IF ONE ACTIVITY WAS DONEBY 2 OR MORE FACILITIES</b></h6>", unsafe_allow_html=True)
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

def generate_unique_number():
    f = dt.datetime.now()  # Get the current datetime
    g = f.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format datetime as a string including microseconds
    h = g.split('.')[1]  # Extract the microseconds part of the formatted string
    j = h[1:5]  # Get the second through fifth digits of the microseconds part
    return int(j)  # Convert the sliced string to an integer

# Initialize the unique number in session state if it doesn't exist
if 'unique_number' not in st.session_state:
    st.session_state['unique_number'] = generate_unique_number()
    unique = st.session_state['unique_number'] 

else:
     pass

if district:
     pass
else:
     st.stop()

planned = r'PLANNED.csv'

dfa = pd.read_csv(planned)

facilities = FACILITIES[district]

today = date.today()
activity = dfa[dfa['CLUSTER']== cluster].copy()
activities = activity['ACTIVITY'].unique()
col1,col2 = st.columns([2,1])
if district:
       done = col1.selectbox('**SELECT THE ACTIVITY YOU ARE PAYING FOR**', activities, index=None)
#       #doned = done
else:
      st.stop()

if not done:
     st.stop()
elif done:
     pass
current_time = time.localtime()
week = time.strftime("%V", current_time)
week = int(week)-39
datey = datetime.now().date()
formatted = datey.strftime("%d-%m-%Y")

if done: 
    state = activity[activity['ACTIVITY']==done]
#      # statea = state[state['DISTRICT']== district].copy()
    statement = state['STATEMENT'].unique()
    counts = state['COUNT'].unique()
    statement = statement[0]
#      # try:
#      #    statement = statement[0]
#      # except:
#      #      st.write('THIS ACTIVITY MAY NOT HAVE BEEN PLANNED FOR THIS DISTRICT')
#      #      st.write('CONTACT YOUR TEAM LEAD FOR SUPPORT')
#      #      st.stop()
    counts = counts[0]
    cola, colb = st.columns(2)
    num = cola.number_input('**HOW MANY FACILITIES CONDUCTED THIS ACTIVITY?**',value=None, step=1)

    if not num:
          st.stop()
    elif num>10:
          st.warning('Maximum can be 10')
          st.stop()
    elif num == 0:
          st.warning("CAN'T BE ZERO")
          st.stop()
    else:
          st.markdown(f'**NOTE: {statement}**')

     
    for i in range(num):
          colt,coly,colx = st.columns([1,1,1])
          colt.write(f'**FACILITY {i+1}**')
          
          coly,colz = st.columns(2)
          facility = coly.selectbox(f"**Name of facility {i+1}:**", facilities, index=None, key=f'y{i}')
          if not facility:
               st.stop()
          else:
               pass
          colt,coly,colx = st.columns([1,1,1])
          number = colt.number_input(label=f'**{counts}**', value=None, max_value=None, min_value=None,step=1, format="%d", key=i)
          start = coly.date_input(label='**ACTIVITY START DATE**', value=None, key=f'a{i}')
          end = colx.date_input(label='**END DATE**',value=None, key= f'b{i}')
          clustery = cluster
          clusters.append(clustery)
          districty = district
          districts.append(districty)
          weeky = week
          uniquey = st.session_state['unique_number'] 
          areay = area
          doney = done
          formattedy = formatted
          weeks.append(weeky)
          uniques.append(uniquey)
          areas.append(areay)
          activit.append(doney)
          dates.append(formattedy)

#           if number and start and end:
#                if start > end:
#                     st.warning("IMPOSSIBLE, ACTIVITY START DATE CAN'T BE GREATER THAN END DATE")
#                     st.stop()
#                elif end>today:
#                     st.warning("IMPOSSIBLE, CHECK END DATE, IT'S GREATER THAN TODAY")
#                     st.stop()
#                else:
#                     numbers.append(number)
#                     facilitiesy.append(facility)
#                     starts.append(start)
#                     ends.append(end)
#           else:
#                st.stop()
               
#      if area == 'PMTCT':
#           money = colt.number_input(label='**HOW MUCH ARE YOU PAYING?**', value=None, max_value=None, min_value=None,step=1, format="%d")
#      else:
#           pass
#      if area == 'PMTCT':
#           if not money:
#              st.stop()
#           elif money <10000:
#                st.warning('**CHECK WHETHER THE MONEY IS LESS THAN 10,000**')

# if num==1:
#      districts = [districts[0]]
#      weeks = [weeks[0]]
#      uniques = [uniques[0]]
#      areas = [areas[0]]
#      activit = [activit[0]]
#      dates = [dates[0]]
# elif num>1:
#      districts = districts[0:num]
#      weeks = weeks[0:num]
#      uniques = uniques[0:num]
#      areas = areas[0:num]
#      activit = activit[0:num]
#      dates = dates[0:num]

# df = pd.DataFrame({
#           'DATE OF SUBMISSION': dates,
#           'CLUSTER': clusters,
#           'DISTRICT': districts,
#           'FACILITY': facilitiesy,
#           'AREA': areas,
#           'ACTIVITY': activit,
#           'DONE': numbers,
#           'START DATE': starts,
#           'END DATE': ends,
#           'ID': uniques,
#           'WEEK': weeks
#           })
# if area =='PMTCT':
#      df2 = pd.DataFrame([money], columns = ['AMOUNT'])
#      district = districts[0]
#      df2['DISTRICT'] = np.nan
#      df2['DISTRICT'] = df2['DISTRICT'].fillna(district)
#      df2['ACTIVITY'] = np.nan
#      df2['ACTIVITY'] = df2['ACTIVITY'].fillna(doned)
#      df2 = df2[['DISTRICT', 'ACTIVITY', 'AMOUNT']].copy()
# else:
#      pass

                                         
                                         
# dfd = df[df.duplicated(subset='FACILITY')]
# check = dfd.shape[0]

# if check>0:
#      dfd['FACILITY'] = dfd['FACILITY'].astype(str)
#      disa = ', '.join(dfd['FACILITY'].unique())
#      st.warning(f'**You repeated {disa}**')
#      st.write("**ADD ALL THEIR TOTALS DONE AND SUBMIT THEM AT ONCE**")
#      st.stop()
# else:
#      pass

# st.write(f"UNIQUE ID: {st.session_state['unique_number']}")
# col1,col2, col3 = st.columns([1,1,2])
# col2.write('**SUMMARY**')

# cola,colb = st.columns(2)
# cola.write(f"**UNIQUE ID: {st.session_state['unique_number']}**")
# cola.markdown(f'**DISTRICT: {district}**')
# colb.markdown(f'**FACILITY: {facility}**')
# colb.markdown(f'**THEMATIC AREA: {area}**')
# cola,colb,colc = st.columns(3)
# colb.write(f'**ACTIVITY: {done}**')
# if area == 'PMTCT':
#      cola.markdown(f'**AMOUNT: {money}**')
# else:
#      pass

# dfa = df[['FACILITY', 'DONE', 'START DATE', 'END DATE']].copy()

# uniques = df['FACILITY']
# cola,colb = st.columns([3,1])
# cola.write(dfa) 
# submit = colb.button('**SUBMIT**')


# if submit:
#      try:
#           st. write('SUBMITING')
#           conn = st.connection('gsheets', type=GSheetsConnection)
#           exist = conn.read(worksheet= 'DONE', usecols=list(range(11)),ttl=5)
#           existing= exist.dropna(how='all')
#           updated = pd.concat([existing, df], ignore_index =True)
#           conn.update(worksheet = 'DONE', data = updated)  
#           if area == 'PMTCT':
#                exist2 = conn.read(worksheet= 'PMTCT', usecols=list(range(11)),ttl=5)
#                existing2= exist2.dropna(how='all')
#                updated = pd.concat([existing2, df2], ignore_index =True)
#                conn.update(worksheet = 'PMTCT', data = updated)
#           else:
#                pass
#           st.success('Your data above has been submitted')
#           st.write('RELOADING PAGE')
#           time.sleep(3)
#           st.markdown("""
#           <meta http-equiv="refresh" content="0">
#                """, unsafe_allow_html=True)

#      except:
#                st.write("Couldn't submit, poor network") 
#                st.write('Click the submit button again')











