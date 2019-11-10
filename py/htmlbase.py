from webbrowser import open as webopen
from os.path import expanduser

def report_path():
    return expanduser('~/Documents/PIEthon/reports')

def figure_path():
    return expanduser('~/Documents/PIEthon/figures')

class htmlbase:
    def __init__(self, title, header, tablelist, picturelist):

        #checks for correct folders
        self.title = title
        self.header = header
        self.toppart =\
        """
        <html>
            <head>
              <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
            </head>
            <body>
              <div class="page-wrapper">
                <div class="container">
                  <div class="row">
                    <div class="col-lg-12">
                      <div class="card">
                        <div class="card-body">
        """
        self.endpart =\
        """
            </div>
              </div>
            </body>
            </head>
        """
        self.tablelist = tablelist
        self.picturelist = picturelist

    def setTablelist(self, newtable):
        self.tablelist = newtable

    def getTablelist(self):
        return self.tablelist

    def setPicturelist(self, newpict):
        self.picturelist = newpict

    def buildall(self):
        mechastring = self.toppart
        self.fixtables()
        for tablemaybe in self.tablelist:
            mechastring = mechastring + tablemaybe
        self.makePictures()
        for picture in self.picturelist:
            mechastring = mechastring + picture
        mechastring = mechastring + self.endpart
        return mechastring

    def fixtables(self):
        newlist = []
        for indtable in self.tablelist:
            htmlstring = indtable[36:]

            htmlstring = '<table class="table table-hover table-striped">' + htmlstring

            newlist.append(htmlstring)
        newlist.append(
            """
                  </div>
                </div>
                  </div>
                  </div>
                  <br>
            """
        )
        self.setTablelist(newlist)

    def makePictures(self):
        newlisto = []
        for picture in self.picturelist:
            tempstring =\
            """
                    <div class="col-lg-12">
                      <div class="card">
                        <div class="card-body">
                          <h5 class="card-title">Graph</h5>
                          <img src="%s" class="img-fluid w-100">
                        </div>
                      </div>
                    </div>
                    <br>
            """ % (picture)
            newlisto.append(tempstring)
        self.setPicturelist(newlisto)

    def makeHTML(self, filename):
        superstring = self.buildall()
        print(expanduser('~/Documents/PIEthon/reports/'))
        print(expanduser('~/Documents/PIEthon/reports/') + str(filename) + ".html")
        fh = open(expanduser('~/Documents/PIEthon/reports/') + str(filename) + ".html", "w")
        print(fh)
        fh.write(superstring)
        fh.close()

        webopen('file://' + expanduser('~\\Documents\\PIEthon\\reports\\') + filename + ".html")