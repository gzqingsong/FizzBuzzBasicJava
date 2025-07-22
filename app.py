from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'json'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 默认的Python技能图谱数据
DEFAULT_SKILL_DATA = {
    "nodes": [
        {"id": "Python", "group": "core", "size": 40, "color": "#dc3545"},
        {"id": "基础语法", "group": "basic", "size": 25, "color": "#17a2b8"},
        {"id": "数据库操作", "group": "database", "size": 25, "color": "#17a2b8"},
        {"id": "网络编程", "group": "network", "size": 25, "color": "#17a2b8"},
        {"id": "GUI编程", "group": "gui", "size": 20, "color": "#ffc107"},
        {"id": "并发编程", "group": "concurrent", "size": 20, "color": "#ffc107"},
        {"id": "面向对象编程", "group": "oop", "size": 25, "color": "#6c757d"},
        {"id": "数据结构和算法", "group": "algorithm", "size": 25, "color": "#6c757d"},
        
        # 基础语法相关
        {"id": "Flask 框架与 RESTful API开发", "group": "web", "size": 15, "color": "#28a745"},
        {"id": "HTTP 协议与 requests 库使用", "group": "web", "size": 15, "color": "#28a745"},
        {"id": "TCP/UDP 协议与 socket 编程", "group": "network", "size": 15, "color": "#28a745"},
        {"id": "ORM 框架与 SQLAlchemy 库使用", "group": "database", "size": 15, "color": "#28a745"},
        {"id": "连接数据库与执行 SQL 语句", "group": "database", "size": 15, "color": "#28a745"},
        {"id": "SQL 基本语法", "group": "database", "size": 15, "color": "#28a745"},
        {"id": "PyQT 库使用", "group": "gui", "size": 15, "color": "#28a745"},
        {"id": "自定义控件和事件处理函数", "group": "gui", "size": 15, "color": "#28a745"},
        {"id": "多线程和线程同步", "group": "concurrent", "size": 15, "color": "#28a745"},
        {"id": "多进程和进程间通信", "group": "concurrent", "size": 15, "color": "#28a745"},
        {"id": "协程和异步编程", "group": "concurrent", "size": 15, "color": "#28a745"},
        {"id": "条件语句", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "循环语句", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "函数定义和调用", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "变量定义和运算", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "安全、数据类型与运算符", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "异常处理和错误调试", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "文件读写和序列化算法", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "算法方法与属性装饰器", "group": "oop", "size": 15, "color": "#28a745"},
        {"id": "类与对象", "group": "oop", "size": 15, "color": "#28a745"},
        {"id": "继承和多态", "group": "oop", "size": 15, "color": "#28a745"},
        {"id": "通用算法和数据结构算法", "group": "algorithm", "size": 15, "color": "#28a745"},
        {"id": "排序算法和查找算法", "group": "algorithm", "size": 15, "color": "#28a745"},
        {"id": "功能性库使用方法和技巧", "group": "algorithm", "size": 15, "color": "#28a745"},
        {"id": "字符串处理方法", "group": "algorithm", "size": 15, "color": "#28a745"},
        {"id": "模块导入与管理", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "函数定义与调用", "group": "basic", "size": 15, "color": "#28a745"},
        {"id": "界面处理与编程调试", "group": "gui", "size": 15, "color": "#28a745"},
        {"id": "异常和错误处理", "group": "basic", "size": 15, "color": "#28a745"}
    ],
    "links": [
        {"source": "Python", "target": "基础语法"},
        {"source": "Python", "target": "数据库操作"},
        {"source": "Python", "target": "网络编程"},
        {"source": "Python", "target": "GUI编程"},
        {"source": "Python", "target": "并发编程"},
        {"source": "Python", "target": "面向对象编程"},
        {"source": "Python", "target": "数据结构和算法"},
        
        {"source": "网络编程", "target": "Flask 框架与 RESTful API开发"},
        {"source": "网络编程", "target": "HTTP 协议与 requests 库使用"},
        {"source": "网络编程", "target": "TCP/UDP 协议与 socket 编程"},
        
        {"source": "数据库操作", "target": "ORM 框架与 SQLAlchemy 库使用"},
        {"source": "数据库操作", "target": "连接数据库与执行 SQL 语句"},
        {"source": "数据库操作", "target": "SQL 基本语法"},
        
        {"source": "GUI编程", "target": "PyQT 库使用"},
        {"source": "GUI编程", "target": "自定义控件和事件处理函数"},
        {"source": "GUI编程", "target": "界面处理与编程调试"},
        
        {"source": "并发编程", "target": "多线程和线程同步"},
        {"source": "并发编程", "target": "多进程和进程间通信"},
        {"source": "并发编程", "target": "协程和异步编程"},
        
        {"source": "基础语法", "target": "条件语句"},
        {"source": "基础语法", "target": "循环语句"},
        {"source": "基础语法", "target": "函数定义和调用"},
        {"source": "基础语法", "target": "变量定义和运算"},
        {"source": "基础语法", "target": "安全、数据类型与运算符"},
        {"source": "基础语法", "target": "异常处理和错误调试"},
        {"source": "基础语法", "target": "文件读写和序列化算法"},
        {"source": "基础语法", "target": "模块导入与管理"},
        {"source": "基础语法", "target": "函数定义与调用"},
        {"source": "基础语法", "target": "异常和错误处理"},
        
        {"source": "面向对象编程", "target": "算法方法与属性装饰器"},
        {"source": "面向对象编程", "target": "类与对象"},
        {"source": "面向对象编程", "target": "继承和多态"},
        
        {"source": "数据结构和算法", "target": "通用算法和数据结构算法"},
        {"source": "数据结构和算法", "target": "排序算法和查找算法"},
        {"source": "数据结构和算法", "target": "功能性库使用方法和技巧"},
        {"source": "数据结构和算法", "target": "字符串处理方法"}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """获取图谱数据"""
    return jsonify(DEFAULT_SKILL_DATA)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # 解析文件
            data = parse_uploaded_file(filepath)
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': f'文件解析错误: {str(e)}'}), 400
    
    return jsonify({'error': '不支持的文件类型'}), 400

def parse_uploaded_file(filepath):
    """解析上传的文件"""
    file_extension = filepath.rsplit('.', 1)[1].lower()
    
    if file_extension == 'json':
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    elif file_extension in ['xlsx', 'xls']:
        # 读取Excel文件
        df_nodes = pd.read_excel(filepath, sheet_name='nodes')
        df_links = pd.read_excel(filepath, sheet_name='links')
        
        nodes = []
        for _, row in df_nodes.iterrows():
            node = {
                'id': row['id'],
                'group': row.get('group', 'default'),
                'size': row.get('size', 15),
                'color': row.get('color', '#28a745')
            }
            nodes.append(node)
        
        links = []
        for _, row in df_links.iterrows():
            link = {
                'source': row['source'],
                'target': row['target']
            }
            links.append(link)
        
        return {'nodes': nodes, 'links': links}

@app.route('/api/sample-excel')
def download_sample_excel():
    """下载示例Excel文件"""
    sample_data = {
        'nodes': [
            {'id': 'Python', 'group': 'core', 'size': 40, 'color': '#dc3545'},
            {'id': '基础语法', 'group': 'basic', 'size': 25, 'color': '#17a2b8'},
            {'id': '变量和数据类型', 'group': 'basic', 'size': 15, 'color': '#28a745'},
        ],
        'links': [
            {'source': 'Python', 'target': '基础语法'},
            {'source': '基础语法', 'target': '变量和数据类型'},
        ]
    }
    
    # 创建示例Excel文件
    sample_file = os.path.join(app.config['UPLOAD_FOLDER'], 'sample.xlsx')
    with pd.ExcelWriter(sample_file, engine='openpyxl') as writer:
        pd.DataFrame(sample_data['nodes']).to_excel(writer, sheet_name='nodes', index=False)
        pd.DataFrame(sample_data['links']).to_excel(writer, sheet_name='links', index=False)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'sample.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)