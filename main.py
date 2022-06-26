import streamlit as st
import streamlit_authenticator as stac
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import plotly.express as px
from annotated_text import annotated_text


df = pd.read_csv('fybscit_ruparel.csv')
df.dropna(inplace=True)
df['cutoff'] = df['cutoff'].astype(int)

def graph_plot(df,year):
    new_df = df[df['year'] == year]
    new_df.dropna(inplace=True)
    new_df['cutoff'] = new_df['cutoff'].astype(int)
    graph_df = new_df.groupby(['caste', 'list']).max()['cutoff'].reset_index()
    return graph_df

names = ['Rahul', 'Pratik', 'Sahil', 'Hitesh']
usernames = ['rpha', 'pkan', 'skinj', 'hban']
passwords = ['abc123', 'def123', 'ghi123', 'jkl123']
hashed_passwords = stac.Hasher(passwords).generate()

authenticator = stac.Authenticate(names, usernames, hashed_passwords, 'Predictor', 'abcdefg', cookie_expiry_days=2)
name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status == False:
    st.error("Username/Password is incorrect")
if authentication_status == None:
    st.warning("Please enter your username and password")
if authentication_status:
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")
    with st.sidebar:
        selected = option_menu(menu_title="Main Menu", options=['Home','Admission form','Previous Year Cutoffs',
                                                                "FAQ's",'Contact us'])

    if selected == "Home":
        pipe1 = pickle.load(open('pipe1.pkl', 'rb'))
        pipe2 = pickle.load(open('pipe2.pkl', 'rb'))
        pipe3 = pickle.load(open('pipe3.pkl', 'rb'))

        castes = ['NT-D', 'NT-C', 'VJ-A', 'SBC', 'SC', 'Open', 'NT-B', 'ST', 'OBC', 'SEBC', 'EBC']

        st.title("Admission Predictor")
        given_marks = st.number_input('Mathematics Marks')
        selected_caste = st.selectbox("Select Caste", castes)
        input_df = pd.DataFrame({'marks': [given_marks], 'caste': [selected_caste]})

        if st.button('Predict'):
            proba1 = pipe1.predict_proba(input_df)
            proba2 = pipe2.predict_proba(input_df)
            proba3 = pipe3.predict_proba(input_df)
            get_per1 = proba1[0][1]
            get_per2 = proba2[0][1]
            get_per3 = proba3[0][1]
            if get_per1 >= 0.85:
                st.success('Chances for getting admission in 1st cut-off is {} %'.format(round(get_per1 * 100,2)))
            elif get_per1 <=0.85 and get_per1>=0.60:
                st.warning('Chances for getting admission in 1st cut-off is {} %'.format(round(get_per1 * 100,2)))
            else:
                st.error('Chances for getting admission in 1st cut-off is {} %'.format(round(get_per1 * 100,2)))
            if get_per2 >= 0.85:
                st.success('Chances for getting admission in 2nd cut-off is {} %'.format(round(get_per2 * 100,2)))
            elif get_per2 <=0.85 and get_per2>=0.60:
                st.warning('Chances for getting admission in 2nd cut-off is {} %'.format(round(get_per2 * 100,2)))
            else:
                st.error('Chances for getting admission in 2nd cut-off is {} %'.format(round(get_per2 * 100,2)))
            if get_per3 >= 0.85:
                st.success('Chances for getting admission in 3rd cut-off is {} %'.format(round(get_per3 * 100,2)))
            elif get_per3 <=0.85 and get_per3>=0.60:
                st.warning('Chances for getting admission in 3rd cut-off is {} %'.format(round(get_per3 * 100,2)))
            else:
                st.error('Chances for getting admission in 3rd cut-off is {} %'.format(round(get_per3 * 100,2)))

    if selected == "Previous Year Cutoffs":
        list = ['1st','2nd','3rd']
        st.title("FYBSc-IT previous cut-offs")
        selected_year = st.selectbox("Choose Year",[2021,2020,2019])
        selected_list = st.multiselect("Which list would you like to see?",list,['1st','2nd','3rd'])
        df = df[df['list'].isin(selected_list)]
        graph_df = graph_plot(df,selected_year)
        fig = px.bar(graph_df,x='caste',y='cutoff',color='list',barmode="group")
        st.plotly_chart(fig)

    if selected == "FAQ's":
        #  #8ef-blue, #faa-red, #afa-green, #fea-yellow
        annotated_text(("1) According to predictor when I am able to get admission ?",'Ques','#000000'))
        annotated_text(("-> If your chances are more than 60% then you have to fill the form",'Ans','#8F00FF'))
        annotated_text(("2) What is the accuracy of model ?",'Ques','#000000'))
        annotated_text(("-> Our predictor model has 90% accuracy",'Ans','#8F00FF'))
        # how do i know my form is submitted
        # If you have other doubts then send email to us from contact us section
        annotated_text(("If you face other problems then send gmail us from contact us section",' ','#808080'))

    if selected == "Contact us":

        contact_form = """
        <form action="https://formsubmit.co/ramchandrasunilparab2002@gmail.com" method="POST">
             <input type="hidden" name="_captcha" value="false">
             <input type="text" name="name" placeholder="Your name" required>
             <input type="email" name="email" placeholder="Your email" required>
             <textarea name="message" placeholder="Your message here"></textarea>
             <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
        # Use Local CSS File
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        local_css("style/style.css")

    if selected == "Admission form":

        castes = ['NT-D', 'NT-C', 'VJ-A', 'SBC', 'SC', 'Open', 'NT-B', 'ST', 'OBC', 'SEBC', 'EBC']

        st.title("Our College Admission Form")

        first,middle,last = st.columns(3)
        fname = first.text_input("First Name")
        mname = middle.text_input("Middle Name")
        lname = last.text_input("Last Name")

        email,mobile = st.columns(2)
        emailad = email.text_input("Email")
        phone = mobile.text_input("Mobile No.")

        adress = st.text_area("Adress")

        username,password,repassword = st.columns(3)
        username.text_input("Username")
        password.text_input("Password",type='password')
        repassword.text_input("Re-type your Password",type='password')

        caste = st.selectbox("Cast",castes)

        selected_subject = st.selectbox("Select Subject for F.Y.B.Sc",["Bsc-IT","Bsc(PCM)","Bsc(PMS)"])

        if selected_subject == "Bsc-IT":
            math_marks,total_per,result_id = st.columns(3)
            mmarks = math_marks.number_input("Maths Marks",min_value=35,max_value=100,value=60,step=1)
            percentage = total_per.number_input("Total Percentage",min_value=35,max_value=100,value=56,step=1)
            rid = result_id.text_input("Enter Result id",max_chars=10)
        else:
            total_per, result_id = st.columns(2)
            percentage = total_per.number_input("Total Percentage", min_value=35, max_value=100, value=56, step=1)
            rid = result_id.text_input("Enter Result id",max_chars=10)

        img1 = st.file_uploader("Upload 12th marksheet")
        if caste != "Open":
            st.file_uploader("Upload caste Certificate")

        if st.button("Check Info"):
            st.write("Name:-", "[", fname, mname, lname, "]")
            st.write("Adress:-", "[", adress, "]")
            st.write("Email:-", "[", emailad, "]")
            st.write("Phone no:-", "[", phone, "]")
            st.write("Result id:-", "[", rid, "]")
            st.write("Total Percentage:-","[",percentage,"]")
            st.image(img1)


        box = st.checkbox("I filled correct information in this form")
        if box == True:
            if st.button("Submit"):
                progress = st.progress(0)
                st.balloons()
                st.success("Your form was submitted")



# total students applied
# student marks graph