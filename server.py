from flask import *
from flask_cors import CORS
from encoder import *
from painter import *
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
fox=Fox(8,25)


@app.route('/translate', methods=['POST'])
def translate():
    response={}
    json_data=request.json
    try:
        string=str(json_data.get("str"))
        line=int(json_data.get("line"))
        char=int(json_data.get("char"))
    except:
        response['message']="Invalid Argument"
        return jsonify(response),400
    
    if line < 1 or line > 20 or char < 5 or char > 50:
        response['message']="Invalid Argument"
        return jsonify(response),400

    try:
        rune_list=[]
        str_list=string.split("\n")
        for str_line in str_list:
            rune_list.extend(translate_string(str_line))

        fox.refresh(line,char)
        fox.draw(rune_list)
        code=fox.to_base64()
    except Exception as e:
        response['message']=str(e)
        return jsonify(response),400

    response['message']="Successfully generated Runes!"
    response['code']=code
    return jsonify(response),200

app.run(debug=True,host='0.0.0.0', port=8080)