from webbrowser import open as webopen
from os.path import expanduser

report_path = expanduser('~/Documents/PIEthon/reports')
figure_path = expanduser('~/Documents/PIEthon/figures')

class htmlbase:
    def __init__(self):
        #checks for correct folders
        self.title = ''
        self.header = ''
        self.items = []
        self.html =\
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

    def add(self, type, title, info):
        newitem = item(type,title,info)
        self.items.append(newitem)

    def build(self):
        for item in self.items:
            self.html = self.html + \
                        """
                        <h3>
                        %s
                        </h3>
                        <br>
                        """ % item.title
            if item.type == 'table':
                item.info = item.info.to_html(index=False)[36:]
                self.html = self.html + '<table class="table table-hover table-striped">' + item.info + \
                            """
                                  </div>
                                </div>
                                  </div>
                                  </div>
                                  <br>
                            """
            elif item.type == 'graph':
                tempstring =\
                """
                        <div class="col-lg-12">
                          <div class="card">
                            <div class="card-body">
                              <img src="%s" class="img-fluid w-100">
                            </div>
                          </div>
                        </div>
                        <br>
                """ % (figure_path + item.info)
                self.html = self.html + tempstring
            else:
                print('invalid type: ' + str(item.type))
        self.html = self.html + \
                """
                    </div>
                      </div>
                    </body>
                    </head>
                """

    def makeHTML(self, filename):
        self.build()
        fh = open(expanduser('~/Documents/PIEthon/reports/') + str(filename) + ".html", "w", encoding='utf-8')
        fh.write(self.html)
        fh.close()

        webopen('file://' + expanduser('~\\Documents\\PIEthon\\reports\\') + filename + ".html")

class item:
    def __init__(self, type, title, info):
        self.type = type
        self.title = title
        self.info = info