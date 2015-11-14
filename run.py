# coding:utf-8

from tcc3sso import create_app

if __name__ == '__main__':
    app = create_app()
    app.run("0.0.0.0", 9001, debug=True)
