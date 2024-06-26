from tools import dataentering
from client import redeemcode
from client import depositmoney
from client import withdrawmoney
from client import loan_od
from client import transfermoney
from client import cashinhand
import maskpass
import base64
def cp(conn,cur):
    print("\n------------------Client Panel------------------")
    print("Welcome client!!")
    acc_no=dataentering.primary_key_no("acc_no")
    cur.execute("select first_name,last_name,pass,type from clients where acc_no = {}".format(acc_no))
    result=cur.fetchall()
    if result == []:
        print("No account holder with this account number.")
    else:
        acc_type=result[0][3]
        if acc_type == 'S': acc_type="savings"
        if acc_type == 'C': acc_type="current"
        while True:
            print("\nInput ~ to quit")
            passwd=maskpass.askpass(prompt="Enter password to continue: ",mask='*')
            decoded_password=base64.b64decode(result[0][2].encode('utf-8'))
            decoded_password=decoded_password.decode('utf-8')
            if passwd == "~":   
                break
            elif passwd == decoded_password:
                print("\n--------------------Welcome {} {}-------------------".format(result[0][0],result[0][1]))
                cmenu(conn,cur,acc_no,acc_type)
            else:
                print("Wrong password")
            
def cmenu(conn,cur,acc_no,acc_type):
    cash_in_hand=dataentering.handcash(conn,cur,acc_no)
    print("\n Your Cash_In_Hand is {} currency".format(cash_in_hand))
    print()
    print("1.Show Balance")
    print("2.Deposit money")
    print("3.Withdraw money")
    print("4.Redeem Code")
    if acc_type=='savings':
        print("5.Ask for loan / Check loan status")
    else:
        print("5.Check overdraft status")
    print("6.Transfer money to other account")
    print("7.Increase your Cash_in_hand")
    print("~ to quit")
    choice=input("Enter your choice: ")
    match choice:
        case "~":
            pass
        case "1":
            cur.execute("select balance from {} where acc_no={}".format(acc_type,acc_no))
            balance=cur.fetchall()
            print("Your balance is: ",balance[0][0])
            print()
        case "2":
            depositmoney.cp2(conn,cur,acc_type,acc_no)
        case "3":
            withdrawmoney.cp3(conn,cur,acc_type,acc_no)
        case "4":
            redeemcode.cp4(conn,cur,acc_type,acc_no)
        case "5":
            loan_od.cp5(cur,acc_type,acc_no)
        case "6":
            cur.execute("select balance from {} where acc_no={}".format(acc_type,acc_no))
            balance=cur.fetchall()
            balance=balance[0][0]
            transfermoney.cp6(conn,cur,acc_type,acc_no,balance)
        case "7":
            cashinhand.cp7(conn,cur,acc_no)
        case _:
            print("Wrong input!!!!\n")