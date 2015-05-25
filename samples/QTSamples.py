#


import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView


page = '''
<!--  -->

<!DOCTYPE html>

<html>
	<head>
		<meta encoding='UTF-8'>
		<meta lang='en-GB'>
		<meta name='author' content='Jonatan H Sundqvist'>
		<meta>
		<link rel='stylesheet' href='stylesheet.css'>
		<!-- <script src='https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>  -->
		<!-- <script src='script.js'></script> -->
		<title>title</title>

		<style>
			p:hover {
				background-color: #E12DE3;
				-webkit-transition: background-color 0.8s;
			}
		</style>
	</head>

	<body>
		<h1>HTML Views in Python</h1>
		<p>I'm a dashing violet</p>
		<p>I'm a sparkling dandelion</p>
	</body>
</html>
'''



class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)
        self.setHtml(page)
        self.show()

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        # print((frame.toHtml()).encode('utf-8'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = Browser()
    app.exec_()