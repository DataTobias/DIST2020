import os

#basic framework to run web application inside a docker container

#when the web application is started it is accessed on 192.168.99.100:<PORT> , 192.168.99.100:80 by default
                     
class DockerFramework:

    #give the path to source code and the name of the image
    def __init__(self, path, imageName):
        self.path = path
        self.imageName = imageName

    #prints the path of the source code
    def say_path(self):
        print("The web application path is", self.path)

    #make default config file
    def makeConfigFile(self):
        completeName = os.path.join(self.path, 'nginx.conf')
        file = open(completeName, "w") 
        file.write("server {\n	listen 80;\n	server_name _;\n	root /var/www/;\n	index index.html;\n}") 
        file.close()
        print("Config file created")

    #make default dockerfile
    def makeDockerfile(self):
        completeName = os.path.join(self.path, 'Dockerfile.txt')
        file = open(completeName, "w") 
        file.write("FROM nginx:stable \n \nCOPY -- ./dist /var/www \n \nCOPY ./nginx.conf /etc/nginx/conf.d/default.conf") 
        file.close()
        print("Dockerfile created")

    #builds image in docker
    def dockerBuild(self):
        print("Entered building mode")
        os.chdir(self.path)
        buildString = 'cmd /c "docker build -t '+self.imageName+':latest -f Dockerfile.txt ."'
        print(buildString)
        os.system(buildString)
        print("Image built")

    #runs the image to start container, detached mode
    def dockerRunD(self, port):
        runString = 'cmd /c "docker run -d -p '+port+':80 --name '+self.imageName+' --rm '+self.imageName+'"'
        os.system(runString)
        print("Container started")

    def dockerRunD(self):
        runString = 'cmd /c "docker run -d -p 80:80 --name '+self.imageName+' --rm '+self.imageName+'"'
        os.system(runString)
        print("Container started")

    #runs the image to start container, interactive mode
    def dockerRunIT(self, port):
        runString = 'cmd /c "docker run -d -it '+port+':80 --name '+self.imageName+' --rm '+self.imageName+'"'
        os.system(runString)
        print("Container started")

    def dockerRunIT(self, port):
        runString = 'cmd /c "docker run -d -it 80:80 --name '+self.imageName+' --rm '+self.imageName+'"'
        os.system(runString)
        print("Container started")

    #stops the container
    def dockerStop(self):
        stopString = 'cmd /c "docker stop '+self.imageName+'"'
        os.system(stopString)

    #removes image from docker
    def dockerRemove(self):
        self.dockerStop()
        killString = 'cmd /c "docker image rm '+self.imageName+'"'
        os.system(killString)
        print("Image removed")

    #quickstart: build and run the image with default dockerfile and config, runs in detatched mode
    def dockerizeDefault(self):
        self.makeConfigFile()
        self.makeDockerfile()
        self.dockerBuild()
        self.dockerRunD()

    #Creates a selenium test frame 
    @staticmethod
    def createTest(name):
        f = open(name+".py", "w")
        toWrite = ('''import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument("--headless")

#This is a frame for a selenium test based on unittest.
class SeleniumTest(unittest.TestCase):

    #Under setUp the browser is selected and the path to the driver .exe file is given
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:/docker/chromedriver.exe', options=chrome_options)
        #self.driver = webdriver.Chrome(executable_path='PATH TO CHROME DRIVER')
        #self.driver = webdriver.Firefox(executable_path='PATH TO FIREFOX DRIVER')
        #self.driver = webdriver.Edge(executable_path='PATH TO EDGE DRIVER')

    #The custom tests are defined here. Unittest reports on the success of each test individually.
    def testOne(self):
        driver = self.driver
        
        #Enter the addres, 192.168.99.100:PORT, Default port = 80
        driver.get("http://192.168.99.100")

        #Checks if "Marko Starter" is in the website title
        self.assertIn("Marko Starter", driver.title)
    
    def testTwo(self):
        driver = self.driver
        driver.get("http://192.168.99.100")
        driver.find_element_by_xpath("/html/body/header/nav/a[2]").click()
        self.assertIn("Phontastic", driver.title)

    #def testThree(self):
        #Test three body

    #def testFour(self):
        #Test four body

    def tearDown(self):
        self.driver.close()

#If all test succeed unittest reports OK, otherwise unittest reports FAILED.
if __name__ == "__main__":
    unittest.main()
    ''')
    
        f.write(toWrite)
        f.close()



                    #root to source code                   #name of image
p = DockerFramework('C:/docker/gitrepo/frontend.kickstart','exjobbfem')
p.dockerizeDefault()

