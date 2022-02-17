import mysql.connector

mydb = mysql.connector.connect(
    host="", user="", password=""
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE testdb")

mydb = mysql.connector.connect(
    host="", user="", password="", database=""
)

mycursor = mydb.cursor()

mycursor.execute(
    "CREATE TABLE patients(\
                    idnr VARCHAR(255),\
                    phone VARCHAR(255), \
                    name VARCHAR(255), \
                    PRIMARY KEY(idnr, phone)\
                )"
)
mycursor.execute(
    "CREATE TABLE temp(\
                    ids varchar(23),\
                    phone VARCHAR(255), \
                    name VARCHAR(255), \
                    country VARCHAR(25),\
                    PRIMARY KEY(ids)\
                )"
)
mycursor.execute(
    "CREATE TABLE doctors(\
                    idnr VARCHAR(255),\
                    name VARCHAR(255), \
                    emp_date DATE, \
                    salary FLOAT,\
                    idcard INT,\
                    PRIMARY KEY(idnr)\
                )"
)
mycursor.execute(
    "CREATE TABLE appointments(\
                    date DATETIME,\
                    patient VARCHAR(255),\
                    tel_pat VARCHAR(255),\
                    doctor VARCHAR(255),\
                    cabinet VARCHAR(255),\
                    CONSTRAINT FK_pacient FOREIGN KEY(patient,tel_pat) REFERENCES patients(idnr,phone),\
                    CONSTRAINT FK_doctor FOREIGN KEY(doctor) REFERENCES doctors(idnr)\
                )"
)

mycursor.execute(
    'INSERT INTO doctors VALUES("9830475930489","name1","2010-04-22",4335.23,23);'
)
mycursor.execute(
    'INSERT INTO doctors VALUES("4560413230489","name2","2012-04-22",3350.43,34);'
)
mycursor.execute(
    'INSERT INTO doctors VALUES("8830475219889","name3","2011-10-20",3885.00,35);'
)
mycursor.execute(
    'INSERT INTO doctors VALUES("9730123430489","name4","2010-02-09",4030,45);'
)
mycursor.execute(
    'INSERT INTO doctors VALUES("5630475930480","name5","2010-11-15",4005,56);'
)

mycursor.execute('INSERT INTO patients VALUES("9830475930489","2354678956","pname1");')
mycursor.execute('INSERT INTO patients VALUES("3430475964689","3454678234","pname2");')
mycursor.execute('INSERT INTO patients VALUES("3573047590489","2353467346","pname3");')
mycursor.execute('INSERT INTO patients VALUES("9830475575048","2235467346","pname4");')
mycursor.execute('INSERT INTO patients VALUES("9830475936859","2365878966","pname5");')
mycursor.execute('INSERT INTO patients VALUES("3830475930568","2354675686","pname6");')
mycursor.execute('INSERT INTO patients VALUES("4573047593045","3554672346","pname7");')

mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-19 12:15:00","9830475930489","2354678956","9830475930489","P03");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-22 10:15:00","3430475964689","3454678234","4560413230489","P10");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-23 09:00:00","3573047590489","2353467346","8830475219889","P03");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-23 09:30:00","9830475575048","2235467346","9730123430489","P03");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-24 10:15:00","9830475936859","2365878966","5630475930480","E13");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-25 11:15:00","3830475930568","2354675686","9830475930489","E14");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-02-26 12:45:00","4573047593045","3554672346","4560413230489","P05");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-01-27 10:15:00","9830475930489","2354678956","8830475219889","P03");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-01-20 11:10:00","3430475964689","3454678234","9730123430489","P05");'
)
mycursor.execute(
    'INSERT INTO appointments VALUES("2021-01-22 09:30:00","3573047590489","2353467346","5630475930480","P10");'
)

mydb.commit()
