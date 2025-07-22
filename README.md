# Python 技能图谱可视化系统

这是一个基于 Flask + D3.js 的交互式 Python 技能图谱可视化系统，支持文件导入和实时交互。

## 功能特性

🎯 **核心功能**
- 交互式力导向图可视化
- 支持 Excel 和 JSON 文件导入
- 实时搜索和高亮显示
- 节点拖拽和缩放操作
- 响应式设计，支持移动端

🎨 **可视化特性**
- 多色彩节点分组显示
- 动态连接线和箭头指向
- 鼠标悬停工具提示
- 节点大小表示重要程度
- 平滑动画过渡效果

📊 **交互控制**
- 搜索节点功能
- 显示/隐藏标签和连线
- 调节力导向图强度
- 重置视图功能
- 统计信息显示

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

## 文件格式说明

### Excel 文件格式

Excel 文件需要包含两个工作表：

**nodes 工作表** (节点数据)：
| 列名 | 说明 | 示例 |
|------|------|------|
| id | 节点唯一标识 | Python |
| group | 节点分组 | core |
| size | 节点大小 | 40 |
| color | 节点颜色 | #dc3545 |

**links 工作表** (连接数据)：
| 列名 | 说明 | 示例 |
|------|------|------|
| source | 源节点ID | Python |
| target | 目标节点ID | 基础语法 |

### JSON 文件格式

```json
{
  "nodes": [
    {
      "id": "Python",
      "group": "core",
      "size": 40,
      "color": "#dc3545"
    }
  ],
  "links": [
    {
      "source": "Python",
      "target": "基础语法"
    }
  ]
}
```

## 使用说明

### 导入数据
1. 点击页面右上角的"📁 导入数据"按钮
2. 选择 Excel 或 JSON 文件
3. 点击"上传"按钮
4. 系统会自动解析文件并更新可视化

### 交互操作
- **拖拽节点**：鼠标按住节点可以拖拽移动
- **搜索节点**：在搜索框中输入关键词高亮匹配节点
- **悬停查看**：鼠标悬停在节点上查看详细信息
- **调节参数**：使用控制面板调节显示效果

### 下载示例
点击"📥 下载示例"按钮可以下载标准格式的 Excel 模板文件。

## 技术架构

### 后端技术栈
- **Flask**: Web 框架
- **Pandas**: 数据处理
- **OpenPyXL**: Excel 文件读写
- **Flask-CORS**: 跨域支持

### 前端技术栈
- **D3.js**: 数据可视化
- **Bootstrap 5**: UI 框架
- **原生 JavaScript**: 交互逻辑

### 项目结构
```
├── app.py                 # Flask 后端应用
├── requirements.txt       # Python 依赖
├── templates/
│   └── index.html        # 主页面模板
├── static/
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── visualization.js  # 可视化逻辑
└── uploads/              # 文件上传目录
```

## API 接口

### GET /api/data
获取默认的技能图谱数据

### POST /api/upload
上传并解析 Excel/JSON 文件

### GET /api/sample-excel
下载示例 Excel 文件

## 自定义扩展

### 添加新的节点类型
在 `app.py` 的 `DEFAULT_SKILL_DATA` 中添加新的节点和连接。

### 修改可视化样式
编辑 `static/css/style.css` 文件自定义颜色和动画效果。

### 扩展交互功能
在 `static/js/visualization.js` 中添加新的事件处理函数。

## 注意事项

1. 上传的文件大小限制为 16MB
2. Excel 文件必须包含 "nodes" 和 "links" 两个工作表
3. 节点 ID 必须唯一，连接的 source 和 target 必须存在对应的节点
4. 建议节点数量控制在 100 个以内以保证良好的性能

## 许可证

MIT License