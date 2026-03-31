import streamlit as st
import json
import random
import string
from pathlib import Path

database = 'data1.json'

if Path(database).exists():
    try:
     with open(database,'r') as f:
        data = json.load(f)
    except:
        data=[]
else:
    data = []   
   
def save_data():
    with open(database,'w') as f:
        json.dump(data,f)


   
def accNOgenerated():
    alpha = random.choices(string.ascii_letters,k=4)
    num = random.choices(string.digits,k=4)
    id = alpha+num
    random.shuffle(id)
    return "".join(id)
    

def login_user(accNO,pin):
    user = [i for i in data if i['accountnum']==accNO and i['pin']==int(pin)]
    return user[0] if user else None


st.title("Bank System")

menu = st.sidebar.radio("Menu",[
    "Create Account",
    "Login",
    "Deposit",
    "Withdraw",
    "Transaction History",
    "Check balance",
    "Account Details",
    "Update Details",
    "Delete Account"
])

if menu =="Create Account":
    st.subheader("Create Account")

    name = st.text_input("Enter your name")
    age = int(st.number_input("Enter your age ", min_value=0))
    email = st.text_input("Enter your email")
    pin = st.text_input("Enter 4 digit pin", type = "password")
    
    if st.button("create Account"): 
      if age<=18 or len(pin)!=4 :
            st.error("invalid details")
      else:
        acc_no = accNOgenerated()
        user = {
            "name": name,
            "age" : age, 
            "email": email,
            "pin" : int(pin),
            "accountnum" : acc_no,
            "balance" : 0,
            "transaction" : []
              }
        
        data.append(user)
        save_data()
    
        st.success("Account created successfully")
        st.write("Your Account number :",acc_no)


elif menu=="Login":
    st.subheader("login")
    accNO = st.text_input("Enter your account number:")
    pin = st.text_input("Enter your pin:",type = "password")

    if st.button("Login"):
        user = login_user(accNO,pin)
        if not user:
            st.error("Invalid Details")
        else:
            st.success(f"Welcome{user['name']}")


elif menu == "Deposit":
    st.subheader("Deposit Money")

    accNO = st.text_input("Enter your account number:")
    pin = st.text_input("Enter your pin:",type = "password")
    amount = st.number_input("Enter Amount",min_value=0)

    if st.button("Deposit"):
        user = login_user(accNO,pin)
        
        if not user:
            st.error("Invalid Details")
        else:
            user['balance'] += amount
            user['transaction'].append({
                "type" : "Deposit",
                "amount" : amount
            })
            save_data()
            st.success("Money Deposited")
            st.write("update Balance:",user['balance'])


elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    accNO = st.text_input("Enter your account number:")
    pin = st.text_input("Enter your pin:",type = "password")
    amount = st.number_input("Enter Ammount",min_value=0)
     
    if st.button("Withdraw"):
        user = login_user(accNO,pin)

        if not user:
            st.error("Invalid Details")
        elif amount>user['balance']:
            st.error("Insufficient balance")
        else:
            user['balance'] -= amount
            user['transaction'].append({
                "type" : "Withdraw",
                "amount" : amount
            })
            save_data()
            st.success(f"Money debited from your account : {amount}" )
            st.write(f"Updated balnce:{user['balance']}")


elif menu == "Transaction History":
    st.subheader("Transaction History")
    accNO = st.text_input("Enter your account num.")
    pin = st.text_input("Enter pin",type="password")

    if st.button("Show History"):
        user = login_user(accNO,pin)

        if not user:
            st.error("Invalid Details")
        else:
            transaction = user.get('transaction', [])

            if not transaction:
                st.info("NO Transaction Yet")
            else:
                for t in transaction[-5:]:
                     st.write(f"{t.get('type')} → {t.get('amount' ,  0)}")


elif menu == "Check balance":
    st.subheader("Check balance")
    accNO = st.text_input("Enter your account num.")
    pin = st.text_input("Enter pin",type="password")

    if st.button("Check balance"):
        user = login_user(accNO,pin)

        if not user:
            st.error("Invalid Details")
        else:
            st.success(f"Balance :{user['balance']}")


elif menu == "Account Details":
    st.subheader("Account Details")

    accNO = st.text_input("Enter your account number :")
    pin = st.text_input("Enter pin",type="password")

    if st.button("Account Details"):
        user = login_user(accNO,pin)

        if not user: 
           st.error("Invalid Details")
        else:
            for key,value in user.items():
                st.write(f"{key} : {value}")

elif menu == "Update Details":
    st.subheader("Update Details")  

    accNO = st.text_input("Enter your account number :")
    pin = st.text_input("Enter pin",type="password")

    new_name = st.text_input("Enter your new name or press enter for skip")
    new_email = st.text_input("Enter your new email or press enter for skip")
    new_pin = st.text_input("Enter your new pin or press enter for skip")
    
    if st.button("Update Details"):
        user = login_user(accNO,pin)       
        
        if not user:
            st.error("Invalid Details")
        
        else:
          if new_name != "":
            user['name'] = new_name

          if new_email != "":
            user['email'] = new_email

          if new_pin != "":
            user['pin'] = int(new_pin)

          save_data()
          st.success("Details Updated Successfully")
          for key,value in user.items():
                st.write(f"{key} : {value}")

elif menu == "Delete Account":
    st.subheader("Delete Account")
    accNO = st.text_input("Enter your account number :")
    pin = st.text_input("Enter your pin ",type = "password")

    confirm_pin = st.text_input("confirm your pin ",type = "password")

    if st.button("Delete"):
        user = login_user(accNO,pin)

        if not user :
            st.error("Invalid Details")
        
        elif confirm_pin == "":
                st.error("please confirm your pin")
        
        elif int(confirm_pin)!=user['pin']:
                st.error("wrong pin")

        else:
            data.remove(user)
            save_data()
            st.success("Account Deleted successfully")