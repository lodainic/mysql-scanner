import mysql.connector
import math
import re
import itertools
import datetime

class DatabaseManip:
    def __init__(self, host, user, passwd, db) -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def connect_db(self):
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.passwd,
            database = self.db
        )

    def disconnect_db(self):
        self.mydb.close()

    def norm_nullbt(self):
        tables =[]
        self.good_des = []
        self.bad_des = []
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('SHOW TABLES;')
        for x in mycursor:
           tables.append(str(x[0]))
        for table in tables:
            mycursor.execute('SELECT table_name, column_name, is_nullable, column_key \
                            FROM information_schema.columns \
                            WHERE table_schema = "'+self.db+'" and table_name = "'+table+'";')
            p=0
            tmp=[]
            for x in mycursor:
                if x[2] =='NO':
                    p=p+1
                else:
                    tmp.append([x[0],x[1],x[2]])
            if p>=2:
                self.good_des.append(tmp)
            else:
                self.bad_des.append(tmp)

        t = itertools.chain(*self.good_des)
        t1 = itertools.chain(*self.bad_des)
        self.good_des = [list(i) for i in set(map(tuple, t))]
        self.bad_des = [list(i) for i in set(map(tuple, t1))]

        return self.good_des, self.bad_des

    def save_norm_nullbt(self,b_sel):
        mycursor = self.mydb.cursor(buffered=True)
        dt = self.mydb.cursor(buffered=True)
        if len(b_sel) != 0:
            for s in b_sel:
                dt.execute('SELECT column_type \
                            FROM information_schema.columns \
                            WHERE table_schema= "'+self.db+'" and table_name = "'
                            +str((self.bad_des[s])[0])+'" and column_name = "'
                            +str((self.bad_des[s])[1])+'";')
                dtp = str(dt.fetchone()[0])
                dtp = dtp.replace("b'",'')
                dtp = dtp.replace("'",'')
                mycursor.execute('ALTER TABLE '+str((self.bad_des[s])[0])
                                +' MODIFY COLUMN '+str((self.bad_des[s])[1])
                                +' '+dtp+' NOT NULL ;')
           
    def norm_pr_key(self):
        tables =[]
        tables_pr_keys = []
        self.res =[]
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('SHOW TABLES;')
        for x in mycursor:
           tables.append(str(x[0]))
        for table in tables:
            mycursor.execute('SELECT table_name, column_name, column_key, extra\
                            FROM information_schema.columns \
                            WHERE table_schema = "'+self.db+'" and table_name = "'+table+'";')
            c=0
            n=0
            for x in mycursor:
                if x[2] == 'PRI' and x[3] != 'auto_increment':
                    c=c+1
                    tables_pr_keys.append([x[0],x[1],x[2]])
                if x[2] == 'PRI' and x[3] == 'auto_increment':
                    n=n+1
                    tables_pr_keys.append([x[0], x[1],x[2]])
            if (c==0 and n==0) or (n>1) or (c==1 and n==0) or (c>0):
                self.res.append([x[0],c+n])
        return self.res, tables_pr_keys

    def save_norm_pr_key(self):
        mycursor = self.mydb.cursor(buffered=True)
        
        for s in self.res:
            if s[1] == 0:
                mycursor.execute('ALTER TABLE '+str(s[0])+
                                ' add COLUMN id INT AUTO_INCREMENT PRIMARY KEY;')
            elif s[1] == 1:  
                temp = self.mydb.cursor(buffered=True)
                temp.execute('SELECT  table_name, column_name, referenced_column_name\
                                    FROM information_schema.key_column_usage\
                                    WHERE  table_schema = "'+self.db+'" and \
                                        referenced_table_name = "'+str(s[0])+'";')

                temp1 = self.mydb.cursor(buffered=True)
                temp1.execute('SELECT table_name, column_name, constraint_name\
                                        FROM information_schema.key_column_usage\
                                        WHERE  table_schema = "'+self.db+'" and \
                                            referenced_table_name = "'+str(s[0])+'";')
                for t in temp1:
                    mycursor.execute('ALTER TABLE '+str(t[0])+' DROP CONSTRAINT '+str(t[2]))
                
                mycursor.execute('ALTER TABLE '+str(s[0])+
                                ' DROP PRIMARY KEY;')
                mycursor.execute('ALTER TABLE '+str(s[0])+
                                ' add COLUMN id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY;')
                
                for x in temp:
                    mycursor.execute('ALTER TABLE '+str(x[0])+
                                    ' ADD id_'+str(s[0])+' SMALLINT UNSIGNED NOT NULL DEFAULT 0;')
                    mycursor.execute('UPDATE '+str(x[0])+' as t1, '+
                                    str(s[0])+' as t2 \
                                    SET t1.id_'+str(s[0])+'=t2.id\
                                    WHERE t1.'+str(x[1])+'=t2.'+str(x[2])+';')
                    mycursor.execute('ALTER TABLE '+str(x[0])+
                                    ' add CONSTRAINT FK_id_'+str(s[0])+
                                    ' FOREIGN KEY(id_'+str(s[0])+
                                    ') REFERENCES '+str(s[0])+'(id);') 
                    mycursor.execute('ALTER TABLE '+str(x[0])+
                                    ' DROP COLUMN '+str(x[1])+';')  

            elif s[1] == 2:
                temp = self.mydb.cursor(buffered=True)
                tables = self.mydb.cursor(buffered=True)
                tables.execute('SELECT  distinct(table_name)\
                            FROM information_schema.key_column_usage\
                            WHERE table_schema = "'+self.db+'" and \
                                referenced_table_name = "'+str(s[0])+'";') 
                if tables.fetchone() is None:
                    mycursor.execute('ALTER TABLE '+str(s[0])+
                                ' DROP PRIMARY KEY;')
                    mycursor.execute('ALTER TABLE '+str(s[0])+
                                ' add COLUMN id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY;')
                else:
                    tables.execute('SELECT  distinct(table_name)\
                            FROM information_schema.key_column_usage\
                            WHERE table_schema = "'+self.db+'" and \
                                referenced_table_name = "'+str(s[0])+'";') 
                    for x in tables:
                        mycursor.execute('ALTER TABLE '+str(x[0])+
                                    ' ADD id_'+str(s[0])+' SMALLINT UNSIGNED NOT NULL;')
                        temp.execute('SELECT column_name, referenced_column_name\
                                FROM information_schema.key_column_usage\
                                WHERE  table_schema = "'+self.db+'" and \
                                    referenced_table_name = "'+str(s[0])+'" and \
                                    table_name = "'+str(x[0])+'";')
                        fk = [x for x in temp]
                        temp1 = self.mydb.cursor(buffered=True)
                        temp1.execute('SELECT DISTINCT table_name, constraint_name\
                                    FROM information_schema.key_column_usage\
                                    WHERE  table_schema = "'+self.db+'" and \
                                                referenced_table_name = "'+str(s[0])+'";')
                        for t in temp1:
                            mycursor.execute('ALTER TABLE '+str(t[0])+' DROP CONSTRAINT '+str(t[1]))
                        mycursor.execute('ALTER TABLE '+str(s[0])+
                                    ' DROP PRIMARY KEY;')
                        mycursor.execute('ALTER TABLE '+str(s[0])+
                                    ' add COLUMN id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY;')
                        mycursor.execute('UPDATE '+str(x[0])+' as t1, '+
                                        str(s[0])+' as t2 \
                                        SET t1.id_'+str(s[0])+'=t2.id\
                                        WHERE t1.'+str(fk[0][0])+'=t2.'+str(fk[0][1])+
                                        ' and t1.'+str(fk[1][0])+'=t2.'+str(fk[1][1])+';')
                        temp.execute('ALTER TABLE '+str(x[0])+
                                    ' DROP COLUMN '+str(fk[0][0])+';')      
                        temp.execute('ALTER TABLE '+str(x[0])+
                                    ' DROP COLUMN '+str(fk[1][0])+';')
                        mycursor.execute('ALTER TABLE '+str(x[0])+
                            ' add CONSTRAINT FK_id_'+str(s[0])+
                            ' FOREIGN KEY(id_'+str(s[0])+
                            ') REFERENCES '+str(s[0])+'(id);') 
    def norm_domain(self):
        tables =[]
        self.results_char = []
        self.results_num = []
        self.results_date = []
        mycursor = self.mydb.cursor(buffered=True)
        temp = self.mydb.cursor(buffered=True)
        mycursor.execute('SHOW TABLES;')
        for x in mycursor:
           tables.append(str(x[0]))
        # char columns detection  
        for table in tables:
            mycursor.execute('SELECT table_name,column_name,CHARACTER_MAXIMUM_LENGTH \
                               FROM information_schema.columns \
                                WHERE table_schema = "'+self.db+'" and table_name = "'+table+'";')
            for x in mycursor:
                if x[2] != None :
                    temp.execute('SELECT MAX(LENGTH('+str(x[1])+')) FROM '+str(x[0])+';')
                    max_len = temp.fetchone()[0]
                    if max_len != None:
                        mul = int(math.pow(2,int(math.log(max_len,2))+1))
                        if x[2] != mul:
                            self.results_char.append([x[0],x[1],x[2],max_len,mul])
        # num columns detection 
        for table in tables:
            mycursor.execute('SELECT table_name,column_name,NUMERIC_PRECISION, column_key, data_type\
                            FROM information_schema.columns \
                            WHERE table_schema = "'+self.db+'" and table_name = "'+table+'";')
            for x in mycursor:
                if x[2] != None and x[3] == '' and x[4] in ('float', 'real', 'double','decimal','numeric'):
                    temp.execute('SELECT MAX(LENGTH('+str(x[1])+')) FROM '+str(x[0])+';')
                    max_len = temp.fetchone()[0]
                    mul = int(math.pow(2,int(math.log(max_len,2))+1))
                    if x[2] != mul:
                        self.results_num.append([x[0],x[1],x[2],mul,x[4]])
       
        check_clause = []
        mycursor.execute('SELECT check_clause\
                            FROM information_schema.check_constraints;')
        for x in mycursor:
            check_clause.append(str(x[0]))
        for table in tables:
            mycursor.execute('SELECT column_name, data_type \
                            FROM information_schema.columns as isc\
                            WHERE table_schema = "'+self.db+'" and table_name = "'+table+
                            '" and isc.data_type IN ("mediumint", "int", "bigint");')
            for x in mycursor:
                if not (any(str(x[0]) in string for string in check_clause)):
                    temp.execute('SELECT max('+str(x[0])+') FROM '+str(table))
                    max_int=temp.fetchone()[0]
                    temp.execute('SELECT min('+str(x[0])+') FROM '+str(table))
                    min_int=temp.fetchone()[0]
                    new_min_int = min_int
                    if min_int >= 0:
                        new_min_int = 0
                    elif min_int < 0:
                        new_min_int = min_int-10000
                    new_max_int = max_int + 10000
                    self.results_num.append([table,x[0],(min_int,max_int),(new_min_int,new_max_int),x[1]])
        # date columns detection 
        check_clause=[]
        mycursor.execute('SELECT check_clause\
                            FROM information_schema.check_constraints;')
        for x in mycursor:
            if '_utf8mb4' in str(x[0]) :
                check_clause.append(str(x[0]))

        for table in tables:
            mycursor.execute('SELECT column_name \
                            FROM information_schema.columns as isc\
                            WHERE table_schema = "'+self.db+'" and table_name = "'+table+
                            '" and isc.data_type IN ("date", "datetime", "timestamp");')
            if not check_clause:
                for x in mycursor:
                    if str(x[0]) not in check_clause:
                        temp.execute('SELECT DATE(max('+str(x[0])+')) FROM '+str(table))
                        max_date=str(temp.fetchone()[0])
                        max_date = re.search('((.*))',max_date)
                        max_date = max_date.group(1)
                        temp.execute('SELECT DATE(min('+str(x[0])+')) FROM '+str(table))
                        min_date=str(temp.fetchone()[0])
                        min_date = re.search('((.*))',min_date)
                        min_date = min_date.group(1)
                        new_max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d')+datetime.timedelta(days=1825)
                        new_max_date = datetime.datetime.date(new_max_date)
                        new_min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d')-datetime.timedelta(days=1825)
                        new_min_date = datetime.datetime.date(new_min_date)
                        self.results_date.append([table, x[0], min_date, max_date, new_min_date, new_max_date])

        return self.results_char, self.results_num, self.results_date

    def save_norm_domain(self):
        mycursor = self.mydb.cursor(buffered=True)
        dt = self.mydb.cursor(buffered=True)
        
        for s in self.results_char:
            mycursor.execute('ALTER TABLE '+str(s[0])
                                +' MODIFY COLUMN '+str(s[1])
                                +' '+'VARCHAR('+str(s[4])+') NOT NULL;')
        
        for s in self.results_num:
            dt.execute('SELECT data_type \
                        FROM information_schema.columns\
                        WHERE table_schema= "'+self.db+'" and\
                        table_name = "'+str(s[0])+
                        '" and column_name = "'+str(s[1])+'";')
            dtp = str(dt.fetchone()[0])
            dtp = dtp.replace("b'",'')
            dtp = dtp.replace("'",'')
            if dtp in ('float', 'real', 'double','decimal','numeric'):
                mycursor.execute('ALTER TABLE '+str(s[0])
                                +' MODIFY COLUMN '+str(s[1])+' '
                                +dtp+'('+str(s[3])+',2) NOT NULL;')
            if dtp in ('smallint', 'int', 'bigint'):
                mycursor.execute('ALTER TABLE '+str(s[0])
                            +' ADD CHECK('+str(s[1])+'>='+str(s[3][0])
                            +' AND '+str(s[1])+'<='+str(s[3][1])+');')
        for s in self.results_date:
            mycursor.execute('ALTER TABLE '+str(s[0])
                                +' ADD CHECK('+str(s[1])+'>="'+str(s[4])
                                +'" AND '+str(s[1])+'<="'+str(s[5])+'");')
                

    def drop_fk_constr(self,b):
        mycursor = self.mydb.cursor(buffered=True)
        if b :
            mycursor.execute('SET foreign_key_checks = 0;')
        else:
            mycursor.execute('SET foreign_key_checks = 1;')