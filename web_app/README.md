# Mortal AI 本地跑谱网站

基于您自己训练的 Mortal AI 模型的本地牌谱分析网站。

## 功能特点

- ✅ 使用自定义模型路径（例如：`D:\vscode\Mortal\model\Corn.pth`）
- ✅ 上传 mjai 格式牌谱
- ✅ 实时 AI 分析每一巡的最佳打牌选择
- ✅ 显示 Q 值和决策元数据
- ✅ 支持选择不同玩家视角进行分析
- ✅ 美观的 Web 界面

## 快速开始

### 1. 安装依赖

确保您已经安装了 Mortal 的基本依赖，然后安装 Flask:

```bash
pip install flask
```

### 2. 启动服务器

#### 方法 1: 命令行指定模型路径

```bash
python app.py --model "D:\vscode\Mortal\model\Corn.pth"
```

#### 方法 2: 启动后在网页中加载

```bash
python app.py
```

然后在浏览器中打开 http://127.0.0.1:5000，在网页界面中输入模型路径并加载。

### 3. 使用步骤

1. **加载模型**
   - 在"加载模型"区域输入您的模型文件路径
   - 例如: `D:\vscode\Mortal\model\Corn.pth`
   - 点击"加载模型"按钮

2. **上传牌谱**
   - 选择要分析的玩家（0-3）
   - 粘贴 mjai 格式的牌谱数据
   - 点击"开始分析"

3. **查看结果**
   - 查看每一巡的事件
   - 查看 AI 的打牌建议
   - 查看 Q 值和决策置信度

## 命令行参数

```bash
python app.py [选项]

选项:
  --model, -m PATH    模型文件路径 (可选)
  --port, -p PORT     服务器端口 (默认: 5000)
  --host HOST         服务器地址 (默认: 127.0.0.1)
```

## 示例

### 启动示例

```bash
# 使用默认设置
python app.py

# 指定模型和端口
python app.py --model "D:\vscode\Mortal\model\Corn.pth" --port 8080

# 允许外部访问
python app.py --host 0.0.0.0 --port 5000
```

### mjai 格式牌谱示例

```json
{"type":"start_game","names":["player0","player1","player2","player3"],"seed":[0,0]}
{"type":"start_kyoku","bakaze":"E","dora_marker":"3s","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"scores":[25000,25000,25000,25000],"tehais":[["1m","2m","3m","4m","5m","6m","7m","8m","9m","1p","2p","3p","4p"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"]]}
{"type":"tsumo","actor":0,"pai":"5p"}
{"type":"dahai","actor":0,"pai":"1m","tsumogiri":false}
...
```

## API 接口

### GET /api/status
获取当前模型状态

**响应:**
```json
{
  "model_loaded": true,
  "model_path": "D:\\vscode\\Mortal\\model\\Corn.pth",
  "device": "cpu"
}
```

### POST /api/load_model
加载模型

**请求:**
```json
{
  "model_path": "D:\\vscode\\Mortal\\model\\Corn.pth"
}
```

**响应:**
```json
{
  "success": true,
  "message": "模型加载成功: mortal4-b40c192-t26010400",
  "tag": "mortal4-b40c192-t26010400"
}
```

### POST /api/analyze
分析牌谱

**请求:**
```json
{
  "mjai_log": "{"type":"start_game"}...",
  "player_id": 0
}
```

**响应:**
```json
{
  "success": true,
  "player_id": 0,
  "total_events": 150,
  "events": [
    {
      "input": {"type": "tsumo", "actor": 0, "pai": "5p"},
      "reaction": {
        "type": "dahai",
        "pai": "1m",
        "meta": {
          "q_values": [-1.23, 0.45, ...],
          "is_greedy": true
        }
      }
    },
    ...
  ]
}
```

## 目录结构

```
web_app/
├── app.py                 # Flask 应用主文件
├── templates/
│   └── index.html        # 网页界面
├── static/
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── app.js        # 前端 JavaScript
└── README.md             # 本文件
```

## 故障排除

### 问题: 模型加载失败

**解决方案:**
- 检查模型文件路径是否正确
- 确保模型文件存在且可读
- 检查模型文件是否为有效的 .pth 文件

### 问题: 分析失败

**解决方案:**
- 确保牌谱格式为有效的 mjai 格式
- 每行必须是一个有效的 JSON 对象
- 检查玩家 ID 是否在 0-3 范围内

### 问题: 端口已被占用

**解决方案:**
```bash
# 使用不同的端口
python app.py --port 8080
```

## 技术栈

- **后端**: Python 3.9+, Flask
- **前端**: HTML5, CSS3, JavaScript (Vanilla)
- **AI 模型**: Mortal (PyTorch)
- **数据格式**: mjai JSON

## 许可证

本项目基于 Mortal 项目，遵循 AGPL-3.0 许可证。

## 致谢

- [Mortal](https://github.com/Equim-chan/Mortal) - 强大的麻将 AI 引擎
- [mjai](https://github.com/gimite/mjai) - 麻将 AI 接口协议

## 更多信息

- Mortal 文档: https://mortal.ekyu.moe/
- Mortal GitHub: https://github.com/Equim-chan/Mortal
