import sqlite3
conn=sqlite3.connect("chatbot.db")
cursor=conn.cursor()
# to create a faculty table
sql="""CREATE TABLE faculty3( 'id' INTEGER PRIMARY KEY,'name' VARCHAR(50), 'email' VARCHAR(30),'designation' VARCHAR(50));"""
cursor.execute(sql)
conn.commit()

#faculty values
sql='''INSERT INTO faculty3(name,email,designation) values
('dr.akila.v','akila@pec.edu','assistant professor'),
('dr.amuthan.a','amuthan@pec.edu','professor'),
('dr.jayabharathy.j','bharathyraja@pec.edu','associate professor'),
('dr.saruladha.k','charuladha@pec.edu','associate professor'),
('dr.loganathan.d','drloganathan@pec.edu','professor'),
('dr.ilavarasan.e','eilavarasan@pec.edu','professor'),
('dr.karunakaran.e','ekaruna@pec.edu','associate professor'),
('dr.sagayaraj francis.f','fsfrancis@pec.edu','professor'),
('dr.zayaraz.g','gzayaraz@pec.edu','professor'),
('dr.vivekanandan.k','k.vivekanandan@pec.edu','professor'),
('dr.kumaran@Kumar.j','kumaran@pec.edu','assistant professor'),
('dr.lakshmana pandian.s','lpandian72@pec.edu','associate professor'),
('dr.sreenath.n','nsreenath@pec.edu','professor'),
('dr.thambidurai.p','ptdurai@pec.edu','professor'),
('dr.kalpana.r', 'rkalpana@pec.edu','professor'),
('dr.kavitha kumar','rkavithakumar@pec.edu','assistant professor'),
('dr.manoharan.r','rmanoharan@pec.edu','professor and head'),
('dr.salini.p','salini@pec.edu','assistant professor'),
('dr.sarala.r','sarala@pec.edu','assistant professor'),
('dr.sathyamurthy.k','sathiyamurthyk@pec.edu','associate professor'),
('dr.selvaradjou.ka','selvaraj@pec.edu','professor'),
('dr.sheeba.j.i','sheeba@pec.edu','assistant professor'),
('dr.sugumaran.m','sugu@pec.edu','professor');'''
cursor.execute(sql)
conn.commit()
sql="select * from faculty3"
cursor.execute(sql)
print(cursor.fetchall())

sql='''INSERT INTO faculty3(name,email,designation) values('dr.sivakumar.n','sivakumar11@pec.edu','assistant professor');'''
cursor.execute(sql)
conn.commit()

sql= " alter table faculty3 add column department varchar(4)"
cursor.execute(sql)
conn.commit()

sql="update faculty3 set department='cse'"
cursor.execute(sql)
conn.commit()

