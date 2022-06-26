 if selected == "FAQ's":
    #  #8ef-blue, #faa-red, #afa-green, #fea-yellow
    annotated_text(("1) According to predictor when I am able to get admission ?",'Ques','#8ef'),'height=1000')
    annotated_text(("-> If your chances are more than 60% then you have to fill the form",'Ans','#afa'))
    annotated_text(("2) What is the accuracy of model ?",'Ques','#8ef'))
    annotated_text(("-> Our predictor model has 90% accuracy",'Ans','#afa'))
    # how do i know my form is submitted
    # If you have other doubts then send email to us from contact us section
    annotated_text(("If you face other problems then send gmail us from contact us section",' ','#fea'))


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