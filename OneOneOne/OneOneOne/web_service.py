from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.web
from lxml import etree
import xml.etree.ElementTree as ET
from utilities.file_utilities import FileUtilities
from definitions import XML_PATH
from OneOneOne.OneOneOne.message_handler import MessageHandler

response = FileUtilities.get_file_string(XML_PATH / 'basic_success_response.xml')

class MessageReceiver(tornado.web.RequestHandler):
    def initialize(self, servicesDict):
        pass

    def post(self):
        mh = MessageHandler(self.request.body)
        # parser = etree.XMLParser(remove_blank_text=True)
        # root = etree.fromstring(self.request.body, parser)
        # print(etree.tostring(root, pretty_print=True).decode())

        status_code, message_response = mh.evaluate_message()
        self.set_status(status_code)
        self.write(message_response)
        # self.finish()
        # self.flush(True)
        # self.finish(message_response)
        print("Responded")

    def get(self):
        print("Test get method")


if __name__ == "__main__":
    servicesDict = {}
    application = tornado.web.Application([(r"/syncsoap", MessageReceiver, dict(servicesDict=servicesDict))],
                                          debug=True)

    httpsServer = HTTPServer(application)
    httpsServer.listen(4848)
    tornado.ioloop.IOLoop.instance().start()