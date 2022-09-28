from pymongo import MongoClient
# from bson.objectid import ObjectId

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://infinity:mslee0702@localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['POST'])
def save_memo():
    #메모 받기
    title_receive = request.form['title_give']  #메모 제목 받음
    contents_receive = request.form['contents_give']  #메모 내용 받음
    title4edit = title_receive
    contents4edit = contents_receive

    #title/contents/titleedit/contentsedit/likes
    memo = {'title': title_receive, 'contents': contents_receive, 'title_edit' : title4edit, 'contents_edit' : contents4edit, 'likes': 0}

    #mongdoDB 저장
    db.memos.insert_one(memo)

    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def read_memos():
    result = list(db.memos.find({},{'_id': 0}))
    return jsonify({'result': 'success', 'memos': result})

@app.route('/api/like', methods=['POST'])
def like_memo():
    title_receive = request.form['title_give']
    memo = db.memos.find_one({'title': title_receive})
    new_like = memo['likes'] + 1
    db.memos.update_one({'title': title_receive}, {'$set': {'likes': new_like}})
    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_memo():
    title_receive = request.form['title_give']
    db.memos.delete_one({'title': title_receive})
    return jsonify({'result': 'success'})

@app.route('/api/edit', methods=['POST'])
def update_memo():
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']
    new_title = request.form['title_edit']
    new_contents = request.form['contents_edit']

    db.memos.update_one({'title': title_receive}, {'$set': {'title': new_title}})
    db.memos.update_one({'contents': contents_receive}, {'$set': {'contents': new_contents}})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)