import os
from yzgscript import create_app

env=os.environ.get("FLASK_ENV") or 'default'
app=create_app(env)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)