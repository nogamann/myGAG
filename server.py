import tornado.ioloop
import tornado.web
import json
import os
from platform import system
import userLikes


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("main.html")
        self.render("main.html")

class sheetsHandler(tornado.web.RequestHandler):
    def get(self):
        print("sheets handler")
        self.redirect("https://docs.google.com/presentation/d/1FsLbbtWLhHNGdk60ctadGCanPxKEDlF2wC4mKFuo3Ck/present?slide=id.p")

class initialHandler(tornado.web.RequestHandler):
    def get(self):
        print("initial handler")
        result = userLikes.sendTrainingSet()
        result = json.dumps(result)
        self.finish(result)
        print('sent result')
        print(result)

class submitHandler(tornado.web.RequestHandler):
    def get(self):
        print("submit handler")

        arg = self.get_query_argument("selectedVal")
        likes = arg.split(';')
        print(likes)

        # FIND RELEVANT MEMES AND PUT IN RESULT VEC
        result = ["http://memesvault.com/wp-content/uploads/Funny-Meme-3.jpg", "http://memesvault.com/wp-content/uploads/Funny-Meme-13.jpg"]
        result = json.dumps(result)
        self.finish(result)
        print('sent result')
        print(result)

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static")
)


def make_app():
    print("make_app")
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/submit", submitHandler),
        (r"/initial", initialHandler),
        (r"/sheets", sheetsHandler),
    ], **settings)


if __name__ == "__main__":
    if system() == "Windows":
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
