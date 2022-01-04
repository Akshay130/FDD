import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
import pyrebase

firebaseConfig={
        "apiKey": "AIzaSyCubRvqZ_hE_2AYIUQoSiGFXO0O0YvBgZE",
        "authDomain": "fir-rn-app-1.firebaseapp.com",
        "databaseURL": "https://fir-rn-app-1-default-rtdb.firebaseio.com",
        "projectId": "fir-rn-app-1",
        "storageBucket": "fir-rn-app-1.appspot.com",
        "messagingSenderId": "512427544249",
        "appId": "1:512427544249:web:3bd6ca9ad0168484a4d568"
    }

firebase=pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        
        self.invalid.setVisible(False)

    def loginfunction(self):
        email=self.email.text()
        password=self.password.text()
        try:
            auth.sign_in_with_email_and_password(email,password)
            self.loginbutton.clicked.connect(self.gotomain)
        except:
            self.invalid.setVisible(True)
            
    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotomain(self):
        mainpage=Mainpage()
        widget.addWidget(mainpage)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gotologin.clicked.connect(self.gotolog)
        self.invalid.setVisible(False)

    def createaccfunction(self):
        email = self.email.text()
        if self.password.text()==self.confirmpass.text():
            password=self.password.text()
            try:
                auth.create_user_with_email_and_password(email,password)
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            except:
                self.invalid.setVisible(True)
    def gotolog(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Mainpage(QMainWindow):
    def __init__(self):
        super(Mainpage,self).__init__()
        loadUi("mainpage.ui",self)
        self.status.setVisible(False)
        self.generateb.clicked.connect(self.getdata)
        self.gotologin.clicked.connect(self.gotolog)
    def gotolog(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def getdata(self):
        import pyrebase
        import qrcode # Import QR Code library with pip install qrcode[pil]
        import sys #To exit the program if QR data is not given
        import os #To create the save folder if not already there
        import csv #CSV file support
        import random 
        import csv

        config = {
            "apiKey": "AIzaSyCubRvqZ_hE_2AYIUQoSiGFXO0O0YvBgZE",
            "authDomain": "fir-rn-app-1.firebaseapp.com",
            "databaseURL": "https://fir-rn-app-1-default-rtdb.firebaseio.com",
            "projectId": "fir-rn-app-1",
            "storageBucket": "fir-rn-app-1.appspot.com",
            "messagingSenderId": "512427544249",
            "appId": "1:512427544249:web:3bd6ca9ad0168484a4d568"
        }
        
        
        firebase = pyrebase.initialize_app(config)
        database = firebase.database()
        # Output.insert(END, 'Generating keys......\nUploading keys to database......\nOpening keys.csv......\nCodes saved in a directory named "Codes/QRC/"......\nDone!!!')
        #generating random keys
        with open('keys.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                n = int(self.keysno.text())
                for i in range(n):
                    key = random.randint(10000000000000,99999999999999)
                    writer.writerow([key])
                    #uploading to database
                    database.child("keys").push(key)
            
        qrName = 'qr'
        # print('Generating keys......')
        # print('Uploading keys to database........')
        # csvFile = input('opening keys.csv......')
        # qrFolder = input('Creating folder to store the codes.......')
        # boxPixels = input('Generating QR codes of 10*10 px.......')
        imageType = 'png'
        csvFile = 'keys.csv'
        qrFolder = 'QRC'
        boxPixels = 10
        #Set the image type:
        imageExt = '.png'
        #Make a sub folder for saved QRcodes from this run:
        if not os.path.exists(csvFile):
            print('Could not locate any data file named ' + str(csvFile) + '.  Exiting Program...')
            sys.exit()

        if len(str(qrFolder)) == 0:
            print('You did not pick a folder name.  Using "QRC" as the folder name.')
            qrFolder = 'Codes/QRC/'
        else:
            qrFolder = 'Codes/' + qrFolder + '/'

        if len(str(boxPixels)) == 0:
            boxPixels = 10
        #Make a folder for saved QRcodes
        if not os.path.exists('Codes'):
            os.makedirs('Codes')
            print('Creating folder: "Codes"')

        #Make a sub folder for saved QRcodes from this run:
        if not os.path.exists(qrFolder):
            os.makedirs(qrFolder)
            print('Creating folder: ' + qrFolder)

        #Open the CSV file, loop through each line and create a QR code:
        lineCount = 0
        with open(csvFile) as f:
            lines = csv.reader(f)
            for line in lines:
                lineCount += 1
                qrFilename = qrName + str(lineCount)

                #Check to see if we already have a previously created file with the same name:
                if os.path.exists(qrFolder + str(qrFilename) + imageExt):
                    print('You already have a code named ' + qrFilename + '. I am renaming it ' + qrFilename + '-COPY')
                    qrFilename = qrFilename + '-COPY'

                # Create qr code instance
                qr = qrcode.QRCode()

                # Add data
                qr.box_size = int(boxPixels)
                qr.add_data(line[0]) #Add the data from column 1 of the CSV
                qr.make(fit=True)

                # Create an image from the QR Code instance
                img = qr.make_image()

                # Save it somewhere, change the extension as needed:
                img.save(qrFolder + qrFilename + imageExt)
                print('QR Code successfully save as ' + qrFolder + qrFilename + imageExt)

        print('===============================================')
        print('Done!')
        print('You successfully created ' + str(lineCount) + ' QR codes!')
        print('===============================================')
        self.status.setVisible(True)
            

app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()
