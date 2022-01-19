# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 13:43:58 2022

@author: Dell
"""



from selenium import webdriver
from selenium.webdriver.support.select import Select
#import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import datetime

today_date=date.today().strftime("%d %m %Y")
today_date=pd.to_datetime(today_date,dayfirst=True)
path='C:/Users/Dell/Downloads/chromedriver_win32/chromedriver'
driver= webdriver.Chrome(path)
procedure = []
categorie = []
type_of_work = []
posting_time = []
reference = []
programmme = []
objet = []
acheteur_public = []
lieu_d_execution = []
date_close = []
time_close = []
action = []
industry = []
type_of_work = []

l = ['1.23','1.15','1.21','1.10','1.12','1.13','1.16','1.17','1.14','1.22','1.18','1.19','1.11','1.20','2.22','2.23','2.20','2.70','2.17','2.21','2.15','2.10','2.18','2.19','2.80','2.14','2.16','2.24','2.16','2.11','2.12','2.90','2.13','3.17','3.10','3.11','3.16','3.18','3.22','3.15','3.14','3.12','3.13','3.19','3.21','3.20']
url_list = []
for i in l:
    url_list.append(f"https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&AllCons&EnCours&domaineActivite={i}")

url_list+=['https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&AllCons&EnCours&searchAnnCons']

for url in url_list:
    try:
        driver.get(url)
        driver.maximize_window()
        drop_dwn=driver.find_element_by_id("ctl0_CONTENU_PAGE_resultSearch_listePageSizeTop")
        size=Select(drop_dwn)
        size.select_by_visible_text('500')
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        no_of_pages = soup.find('div','ctl0_CONTENU_PAGE_resultSearch_nombrePageTop',class_='nb-total').text.split('/ ')[-1]
        
        col_1 = soup.find_all( 'td',class_ = 'col-90')
        col_2 = soup.find_all( 'td',class_ = 'col-450')
        col_4 = soup.find_all( 'div',class_ = 'cloture-line')
        col_5 = soup.find_all( 'td',class_ = 'actions col-panier')
        
        for i in range(0,len(col_1),2):
            aoo = col_1[i].text.split('\n')[2].split('\t')[-1].rstrip()
            aooo = col_1[i].text.split('\n')[9].split('\t')[-1].rstrip()
            ao = col_1[i].text.split('\n')[13].split('\t')[-1].rstrip()
            time = col_1[i].text.split('\n')[16].split('\t')[-1].lstrip()
            time=pd.to_datetime(time,dayfirst=True)
            procedure.append(aoo)
            categorie.append(aooo)
            type_of_work.append(ao)
            posting_time.append(time)

        for i in range(0,len(col_2)):
            q = col_2[i].text.split('\n')[3].rstrip()
            qq = col_2[i].text.split('\n')[13].split('\t')[-1].rstrip()
            qqq = col_2[i].text.split('\n')[17].split('\t')[-1].rstrip()
            qqqq = col_2[i].text.split('\n')[23].split('\t')[-1].rstrip()
            reference.append(q)
            programmme.append(qq)
            objet.append(qqq)
            acheteur_public.append(qqqq)

        for i in range(1,len(col_1),2):
            place = col_1[i].text.split('\n')[13].rstrip()
            lieu_d_execution.append(place)

        for i in range(0,len(col_4),2):
            date = col_4[i].text.split('\t')[9].split('\n')[0][:-5]
            date=pd.to_datetime(date,dayfirst=True)
            time = col_4[i].text.split('\t')[9].split('\n')[0][-5:]
            date_close.append(date)
            time_close.append(time)

        for i in range(0,len(col_2)):
            link = str(col_5[i]).split('span')[2].split('"')[1].replace("&amp;","&")
            action.append(link)
            industry.append(url[-4:])
        
        if int(no_of_pages) > 1:
            for i in range(1,int(no_of_pages)):
                nxt= driver.find_element_by_xpath('//a[@href="javascript:;//ctl0_CONTENU_PAGE_resultSearch_PagerTop_ctl2"]')
                nxt.click()
                html_1 = driver.page_source
                soup_1 = BeautifulSoup(html_1,'html.parser')
                
                col_1 = soup.find_all( 'td',class_ = 'col-90')
                col_2 = soup.find_all( 'td',class_ = 'col-450')
                col_4 = soup.find_all( 'div',class_ = 'cloture-line')
                col_5 = soup.find_all( 'td',class_ = 'actions col-panier')
                
                for i in range(0,len(col_1),2):
                    aoo = col_1[i].text.split('\n')[2].split('\t')[-1].rstrip()
                    aooo = col_1[i].text.split('\n')[9].split('\t')[-1].rstrip()
                    ao = col_1[i].text.split('\n')[13].split('\t')[-1].rstrip()
                    time = col_1[i].text.split('\n')[16].split('\t')[-1].lstrip()
                    time=pd.to_datetime(time,dayfirst=True)
                    procedure.append(aoo)
                    categorie.append(aooo)
                    type_of_work.append(ao)
                    posting_time.append(time)

                for i in range(0,len(col_2)):
                    q = col_2[i].text.split('\n')[3].rstrip()
                    qq = col_2[i].text.split('\n')[13].split('\t')[-1].rstrip()
                    qqq = col_2[i].text.split('\n')[17].split('\t')[-1].rstrip()
                    qqqq = col_2[i].text.split('\n')[23].split('\t')[-1].rstrip()
                    reference.append(q)
                    programmme.append(qq)
                    objet.append(qqq)
                    acheteur_public.append(qqqq)

                for i in range(1,len(col_1),2):
                    place = col_1[i].text.split('\n')[13].rstrip()
                    lieu_d_execution.append(place)

                for i in range(0,len(col_4),2):
                    date = col_4[i].text.split('\t')[9].split('\n')[0][:-5]
                    date=pd.to_datetime(date,dayfirst=True)
                    time = col_4[i].text.split('\t')[9].split('\n')[0][-5:]
                    date_close.append(date)
                    time_close.append(time)

                for i in range(0,len(col_2)):
                    link = str(col_5[i]).split('span')[2].split('"')[1].replace("&amp;","&")
                    action.append(link)
                    industry.append(url[-4:])

    except NoSuchElementException:
        pass

    industry = [i.replace('1.23','Travaux Forestiers') for i in industry]
    industry = [i.replace('1.15','Travaux de construction et d’aménagement') for i in industry]
    industry = [i.replace('1.21','Travaux hydrauliques, maritimes et fluviaux') for i in industry]
    industry = [i.replace('1.10','Terrassements') for i in industry]
    industry = [i.replace('1.12','Travaux de voiries, chemins et pistes') for i in industry]
    industry = [i.replace('1.13','Travaux d’assainissement, d’eau potable et de réseaux divers') for i in industry]
    industry = [i.replace('1.16','Travaux d’installation') for i in industry]
    industry = [i.replace('1.17','Travaux d’électricité') for i in industry]
    industry = [i.replace('1.14',"Construction d'ouvrages d'art") for i in industry]
    industry = [i.replace('1.22',"Aménagement de jardins, d'espaces verts") for i in industry]
    industry = [i.replace('1.18','Travaux d’étanchéité, isolation, plomberie et menuiserie') for i in industry]
    industry = [i.replace('1.19','Travaux de revêtement, platerie et peinture') for i in industry]
    industry = [i.replace('1.11','Fondations, injections, parois moulées, sondages et forages') for i in industry]
    industry = [i.replace('1.2','Travaux de décoration d’intérieur') for i in industry]
    industry = [i.replace('2.22','Engins de chantier, matériel de manutention et de levage') for i in industry]
    industry = [i.replace('2.23','Matériel de transport, pièces de rechange et pneumatiques') for i in industry]
    industry = [i.replace('2.20','Matériel et fournitures électriques, électronique, électromécanique et pièces de rechange') for i in industry]
    industry = [i.replace('2.70','Produits alimentaires, d’élevage, de la pêche, d’agriculture, d’horticulture et pépinière') for i in industry]
    industry = [i.replace('2.17','Documentation, manuels, fournitures scolaires et d’enseignement') for i in industry]
    industry = [i.replace('2.21','Matériel technique, de lutte contre l’incendie et pièces de rechange') for i in industry]
    industry = [i.replace('2.15','Equipements et produits médicaux, pharmaceutiques et de laboratoire') for i in industry]
    industry = [i.replace('2.10','Matières premières et produits de textile, cuir, caoutchouc et plastique') for i in industry]
    industry = [i.replace('2.18','Matériel informatique, logiciels et pièces de rechanges') for i in industry]
    industry = [i.replace('2.19','Matériel, mobilier et fournitures de bureau') for i in industry]
    industry = [i.replace('2.80','Produits pétroliers, carburants, lubrifiants et produits de chauffage') for i in industry]
    industry = [i.replace('2.14','Imprimés, produits d’impression, de reproduction, et de photographie') for i in industry]
    industry = [i.replace('2.16','Location avec option d’achat de biens, d’équipements de matériel et d’outillage') for i in industry]
    industry = [i.replace('2.24','Matériel et articles de literie, de couchage, de cuisine et de buanderie') for i in industry]
    industry = [i.replace('2.16','Matériaux de construction, plomberie, quincaillerie et outillages') for i in industry]
    industry = [i.replace('2.11','Effets d’habillement et accessoires') for i in industry]
    industry = [i.replace('2.12','Matériel et articles de sport, médailles, effigies et drapeaux') for i in industry]
    industry = [i.replace('2.90','Produits chimiques, de nettoyage, insecticides') for i in industry]
    industry = [i.replace('2.13','Objets d’art, articles artistiques, de divertissement et de médiathèque') for i in industry]
    industry = [i.replace('3.17','Services architecturales et topographiques') for i in industry]
    industry = [i.replace('3.10','Etudes d’ingénierie') for i in industry]
    industry = [i.replace('3.11','Conseil, audit et assistance à maitrise d’ouvrage (à l’exception du domaine des nouvelles technologies)') for i in industry]
    industry = [i.replace('3.16','Prestations d’essais, de contrôle et de laboratoire') for i in industry]
    industry = [i.replace('3.18','Services d’hôtellerie, hébergement, restauration, événementiel et marketing') for i in industry]
    industry = [i.replace('3.22','Services de santé, vétérinaire') for i in industry]
    industry = [i.replace('3.15','Nettoyage, gardiennage, entretien et maintenance') for i in industry]
    industry = [i.replace('3.14','Transport, collecte et services connexes') for i in industry]
    industry = [i.replace('3.12','Services courants') for i in industry]
    industry = [i.replace('3.13','Services de location sans option d’achat') for i in industry]
    industry = [i.replace('3.19',"Services de technologies de l'information et télécommunications") for i in industry]
    industry = [i.replace('3.21','Services agricoles, d’élevage, de pêche') for i in industry]
    industry = [i.replace('3.20','Services d’assurance') for i in industry]

    df = pd.DataFrame({'procedure':procedure,'categorie':categorie,'type_of_work':type_of_work,'posting_time':posting_time,'reference':reference,'programmme':programmme,'objet':objet,'acheteur_public':acheteur_public,'lieu_d_execution':lieu_d_execution,'date_close':date_close,'time_close':time_close,'action':action,'industry':industry})
    df.to_csv("C:/Users/Dell/Desktop/DataDump/data1.csv")
driver.quit()

df_type1=df.drop_duplicates(subset="action")
cleaned_out_df=df_type1["date_close"]>= today_date
notification_df=cleaned_out_df["posting_time"]== today_date

##test if last saved