import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Preprocess the data
def preprocess_data(df, features):
    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=["Gender", "Race/Ethnicity", "Parental level of education", "Lunch", "Test preparation course"], drop_first=True)
    
    # Align user input features with encoded features
    features_encoded = pd.get_dummies(features, drop_first=True)
    features_aligned, _ = features_encoded.align(df_encoded, join='left', axis=1, fill_value=0)
    
    return features_aligned


# Train the model
def train_model(X_train, y_train, model_type):
    if model_type == "Linear Regression":
        model = LinearRegression()
    elif model_type == "Random Forest":
        model = RandomForestRegressor(n_estimators=100)
    
    model.fit(X_train, y_train)
    return model

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
        if make_hashes(password) == hashed_text:
                return hashed_text
        return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

def login_user(username,password):
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()
        return data


def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

def str2():
       st.title("Student Performance Prediction")
        # Load the data
       df = load_data()
       # User input features
       
       gender = st.selectbox("Gender", ["Male", "Female"])
       race_ethnicity = st.selectbox("Race/Ethnicity", ["Group A", "Group B", "Group C", "Group D", "Group E"])
       parental_education = st.selectbox("Parental Level of Education", ["Some high school", "High school", "Some college", "Associate's degree", "Bachelor's degree", "Master's degree"])
       lunch = st.selectbox("Lunch", ["Standard", "Free/reduced"])
       test_prep_course = st.selectbox("Test Preparation Course", ["None", "Completed"])
       math_score = st.slider("Math Score", 0, 100, 50)
       reading_score = st.slider("Reading Score", 0, 100, 50)
       writing_score = st.slider("Writing Score", 0, 100, 50)
       model_type = st.selectbox("Select Model", ["Linear Regression", "Random Forest","Hybrid"])
       data = {
              "Gender": [gender],
              "Race/Ethnicity": [race_ethnicity],
              "Parental level of education": [parental_education],
              "Lunch": [lunch],
              "Test preparation course": [test_prep_course],
              "Math score": [math_score],
              "Reading score": [reading_score],
              "Writing score": [writing_score]
        }
       features = pd.DataFrame(data)
       st.write(features)
       a=(reading_score+writing_score+math_score)/3
       if st.button("Predict"):
                if a > 70:
                     st.success('Performance Category : Great!', icon="✅")
                elif a >= 30:
                       st.warning("Performance Category : Good!")
                else:
                       st.error("Performance Category : Needs Improvement")

def main():

        st.markdown("<h1 style='text-align: center; color: green;'>Student Performance Prediction System</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: green;'>Intelligent Student Performance Prediction System using Machine Learning</h4>", unsafe_allow_html=True)

        menu = ["HOME","ADMIN LOGIN","USER LOGIN","SIGN UP"]
        choice = st.sidebar.selectbox("Menu",menu)

        if choice == "HOME":
                st.markdown("<h1 style='text-align: center;'>HOMEPAGE</h1>", unsafe_allow_html=True)
                image = Image.open(r"image.jpg")
                st.image(image, caption='',use_column_width=True)
                st.subheader(" ")
                st.write("     <p style='text-align: center;'> A Student Performance Prediction System utilizes machine learning to forecast academic achievement based on data like attendance, grades, and demographics. It preprocesses data, selects relevant features, and develops models using algorithms such as regression or neural networks. Models are evaluated for accuracy and deployed to generate predictions for new data. The system may include a feedback loop to refine models over time. Predictions aid educators in identifying at-risk students and optimizing interventions for better outcomes. It can be deployed standalone or integrated into existing educational platforms, providing valuable insights to support student success with data-driven decision-making.", unsafe_allow_html=True)
                time.sleep(3)
                st.warning("Goto Menu Section To Login !")

        elif choice == "ADMIN LOGIN":
                 st.markdown("<h1 style='text-align: center;'>Admin Login Section</h1>", unsafe_allow_html=True)
                 user = st.sidebar.text_input('Username')
                 passwd = st.sidebar.text_input('Password',type='password')
                 if st.sidebar.checkbox("LOGIN"):

                         if user == "Admin" and passwd == 'admin123':

                                                st.success("Logged In as {}".format(user))
                                                task = st.selectbox("Task",["Home","Profiles"])
                                                if task == "Profiles":
                                                        st.subheader("User Profiles")
                                                        user_result = view_all_users()
                                                        clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                                                        st.dataframe(clean_db)
                                                str2()
                                                
                         else:
                                st.warning("Incorrect Admin Username/Password")
          
        elif choice == "USER LOGIN":
                st.markdown("<h1 style='text-align: center;'>User Login Section</h1>", unsafe_allow_html=True)
                username = st.sidebar.text_input("User Name")
                password = st.sidebar.text_input("Password",type='password')
                if st.sidebar.checkbox("LOGIN"):
                        # if password == '12345':
                        create_usertable()
                        hashed_pswd = make_hashes(password)

                        result = login_user(username,check_hashes(password,hashed_pswd))
                        if result:

                                st.success("Logged In as {}".format(username))
                                str2()
                                         
                        else:
                                st.warning("Incorrect Username/Password")
                                st.warning("Please Create an Account if not Created")

        elif choice == "SIGN UP":
                st.subheader("Create New Account")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password",type='password')

                if st.button("SIGN UP"):
                        create_usertable()
                        add_userdata(new_user,make_hashes(new_password))
                        st.success("You have successfully created a valid Account")
                        st.info("Go to User Login Menu to login")

if __name__ == '__main__':
        main()