from flask import Flask,render_template,request
import pickle
import numpy as np


top_50 = pickle.load(open('TOP50.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
final_data = pickle.load(open('final_data.pkl','rb'))
Similarity_Score = pickle.load(open('sscore.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           subject_name = list(top_50['subject'].values),
                           course_name = list(top_50['course name'].values),
                           image = list(top_50['image'].values),
                           platform = list(top_50['platform'].values),
                           rating = list(top_50['rating'].values),
                           refer = list(top_50['link'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_course',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(Similarity_Score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = final_data[final_data['subject'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('subject')['subject'].values))
        item.extend(list(temp_df.drop_duplicates('subject')['course name'].values))
        item.extend(list(temp_df.drop_duplicates('subject')['platform'].values))
        item.extend(list(temp_df.drop_duplicates('subject')['image'].values))
        item.extend(list(temp_df.drop_duplicates('subject')['link'].values))
        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)