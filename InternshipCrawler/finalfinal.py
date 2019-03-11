import wx
import wx.grid
import sqlite3 as sqlite
import wx,string
import requests
from pyquery import PyQuery as pq
from selenium import webdriver

class q2(wx.Frame):
    def __init__(self,parent,db):
        wx.Frame.__init__(self,parent=None,title=u"尋找實習",size=(1000,600))
        self.panel = wx.Panel(self)
        wx.StaticText(parent=self.panel,label=u"選擇類別：",pos=(10,12))
        self.a = wx.ComboBox(parent = self.panel,pos = (100,10),size = (100,-1),choices = ("行銷","藝術","科技","服務"),style =wx.CB_DROPDOWN )
        

        self.grid = wx.grid.Grid(parent=self.panel,pos=(10,100),size=(1000,500))
        self.grid.CreateGrid(1000, 2)
        
        self.btn1 = wx.Button(parent=self.panel,label=u"瀏覽",pos=(500,10))
        self.btn2 = wx.Button(parent=self.panel,label=u"清除",pos=(500,50))

        self.db = db
        self.cur = self.db.con.cursor()
        #新增 BtnClick 事件 -- 開始 --
        self.Bind(wx.EVT_BUTTON,self.BtnClick1,self.btn1)
        self.Bind(wx.EVT_BUTTON,self.BtnClick2,self.btn2)
        #新增 BtnClick 事件 -- 結束 --
        self.message = wx.StaticText(parent=self.panel,pos=(10,160))
        self.message2 = wx.StaticText(parent=self.panel,pos=(10,190))
        #撰寫 BtnClick 事件函式 -- 開始 --
    def BtnClick1(self,event):
        driver = webdriver.Chrome('/Users/USER/Desktop/程式設計概論/chromedriver_win32/chromedriver.exe')

        def inputvalue(name, url):
            driver.get(url) 
            page = 1
            while True:
                if page == 1:
                    try:
                        html = driver.find_element_by_css_selector('*').get_attribute('outerHTML')
                        doc = pq(html)
                        for eachLv1Doc in doc('.joblist_cont').items():
                            t = eachLv1Doc('a').text()
                            u = 'https://www.104.com.tw/' + eachLv1Doc('a').attr('href')
                            box = []
                            box.append(t)
                            box.append(u)
                            sql = "INSERT OR IGNORE INTO " + name + "(NAME, URL) VALUES (?, ?)"
                            self.cur.execute(sql,(t,u))
                            self.db.con.commit()
    #                           
                        driver.find_element_by_css_selector('#s_form > div > div.job_box > div.next_page > span > a').click()
                        page = 2
                    except:
                        break
                else:
                    try:
                        html = driver.find_element_by_css_selector('*').get_attribute('outerHTML')
                        doc = pq(html)
                        for eachLv1Doc in doc('.joblist_cont').items():
                            t = eachLv1Doc('a').text()
                            u = 'https://www.104.com.tw/' + eachLv1Doc('a').attr('href')
                            box = []
                            box.append(t)
                            box.append(u)
                            sql = "INSERT OR IGNORE INTO " + name + "(NAME, URL) VALUES (?, ?)"
                            self.cur.execute(sql,(t,u))
                            self.db.con.commit()
                        driver.find_element_by_css_selector('#s_form > div > div.job_box > div.next_page > span > a:nth-child(2)').click()
                    except:
                        break
            driver.quit()  
        
        a=self.a.GetValue()
        if str(a) == "行銷":
            b = "market"
            inputvalue(b, 'https://www.104.com.tw/area/intern/search.cfm?&indus=0&jobcat=2004000000&addr=0')
        elif str(a) == "藝術":
            b = "art"
            inputvalue(b, 'https://www.104.com.tw/area/intern/search.cfm?keyword=&indus=0&jobcat=2013000000&addr=0')
        elif str(a) == "科技":
            b = "tech"
            inputvalue(b, 'https://www.104.com.tw/area/intern/search.cfm?keyword=&indus=0&jobcat=2007000000&addr=0')
        elif str(a) == "服務":
            b = "serve"
            inputvalue(b, 'https://www.104.com.tw/area/intern/search.cfm?keyword=&indus=0&jobcat=2006000000%2C2005000000&addr=0')
            
        for i in range(22):
            response = requests.get("https://www.blink.com.tw/board/1/?page="+str(i))
            doc = pq(response.text)
            doc.make_links_absolute(base_url=response.url)
            for eachCate in doc("body > div > div > div > div > div > div:nth-child(n+2) > h4 > a ").items():
                t = eachCate.text()
                u = eachCate('a').attr('href')
                if t.find("行銷") != -1:
                    box = []
                    box.append(t)
                    box.append(u)
                    sql = "INSERT OR IGNORE INTO market(NAME, URL) VALUES (?, ?)"
                    self.cur.execute(sql,(t,u))
                    self.db.con.commit()
                elif t.find("藝術") != -1:
                    box = []
                    box.append(t)
                    box.append(u)
                    sql = "INSERT OR IGNORE INTO art(NAME, URL) VALUES (?, ?)"
                    self.cur.execute(sql,(t,u))
                    self.db.con.commit()
                elif t.find("多媒體") != -1:
                    box = []
                    box.append(t)
                    box.append(u)
                    sql = "INSERT OR IGNORE INTO tech(NAME, URL) VALUES (?, ?)"
                    self.cur.execute(sql,(t,u))
                    self.db.con.commit()
                elif t.find("餐廳") != -1:
                    box = []
                    box.append(t)
                    box.append(u)
                    sql = "INSERT OR IGNORE INTO serve(NAME, URL) VALUES (?, ?)"
                    self.cur.execute(sql,(t,u))
                    self.db.con.commit()
                elif a.find("設計") != -1:
                    box = []
                    box.append(t)
                    box.append(u)
                    sql = "INSERT OR IGNORE INTO tech(NAME, URL) VALUES (?, ?)"
                    self.cur.execute(sql,(t,u))
                    self.db.con.commit()      
        
        
        if self.db.exists:
            meta = self.cur.execute("SELECT * from %s"%b)
            labels = []
            for i in meta.description:
                labels.append(i[0])
                print(i[0])
            num_columns = len(labels)
            for i in range(num_columns):
                self.grid.SetColLabelValue(i, labels[i])
            count = 0
            for i in meta:
                for j in range(num_columns):
                    self.grid.SetCellValue(count, j, str(i[j]))
                count += 1

                
        


    def BtnClick2(self,event):
        self.a.ChangeValue('')
        for child in self.grid.GetChildren():
            child.Destroy()
        self.grid = wx.grid.Grid(parent=self.panel,pos=(10,100),size=(450,450))
        self.grid.CreateGrid(1000, 1)
        
        #撰寫 BtnClick 事件函式 -- 結束 --
class GetDatabase():
    def __init__(self, f):
        # check db file exists
        try:
            file = open(f)
            file.close()
        except IOError:
            # database doesn't exist - create file & populate it
            self.exists = 0
        else:
            # database already exists - need integrity check here
            self.exists = 1
        self.con = sqlite.connect(f)

if __name__ == '__main__':
    db = GetDatabase("/Users/USER/Desktop/pytest/code/code/intern.db")
    app = wx.App(0)
    frame = q2(None, db)
    frame.Show(True)
    app.MainLoop()