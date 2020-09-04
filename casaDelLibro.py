import scrapy 
import pandas as pd
# Import the CrawlerProcess: for running the spider
from scrapy.crawler import CrawlerProcess

class ScrapyLibros (scrapy.Spider):
    name="casalibro"
    paginas=8
    def start_requests(self):
        urls=['https://www.casadellibro.com/libros/cocina/106000000']
        for url in urls :
            yield scrapy.Request(url=url,callback=self.aux)

    def aux(self,response):
        urls=[]
        for n in range(self.paginas) :
            urls.append('https://www.casadellibro.com/libros/cocina/106000000/p'+str(n)) 

        for url in urls : 
           yield  response.follow(url=url,callback =self.extraer)

    def extraer (self,response) : 
        titulo=response.xpath('//a[@class="title"]/text()') # Sacamos los titulos de los libros .
        autor=response.css('a.author.text-underline-over::text') # Sacamos los autores de los libros .
        sinopsi=response.xpath('//div[@class="short"]/text()')
        titulos=[t.strip() for t in titulo.extract()] # Limpiamos los libros y los introduciomos en una lista .
        autores =[t.strip() for t in autor.extract()] # Limpiamos los autores y los introduciomos en una lista .
        sinopsiss=[t.strip() for t in sinopsi.extract()]
        print(sinopsis)
        # Guardamos ambos en la lista dic para así poder acceder a ellos posteriormente . (1 y 2)
        for i in titulos:
          dc_dict.append(i) # 1
        for i in autores:
          dc_dict1.append(i) # 2
        for i in sinopsiss:
          sinopsis.append(i) # 2

#Creamos la variable que guardará los datos :

dc_dict =[]
dc_dict1 =[]
sinopsis=[]
#Creamos e iniciamos la futura red que obtendrá los datos

process = CrawlerProcess()
process.crawl (ScrapyLibros)
process.start()
 
for i in range(len(dc_dict)) :
    print("Libro : "+str(dc_dict[i]))
    print("Autor : "+str(dc_dict1[i]))
    print('Sinopsis : '+str(sinopsis[i]))
    print("Id : "+str(i))



print(len(dc_dict))
print(len(dc_dict1))
print(len(sinopsis))
data = {'Libro':dc_dict[0:419],
        'Autor':dc_dict1[0:419],
        'Sinopsis':sinopsis[0:419]} 

df = pd.DataFrame(data, columns = ['Libro','Autor','Sinopsis'])
df.to_csv('libros.csv')
