#!/usr/bin/env python3
"""
Mortal AI 本地跑谱网站 / Local Game Review Web Application
基于 Flask 框架，支持上传牌谱并使用自己训练的 AI 模型进行分析
"""

import sys
import os
import json
import torch
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
from datetime import datetime, timezone
from io import StringIO

# 添加 mortal 模块到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'mortal'))

from model import Brain, DQN, GRP
from engine import MortalEngine
from common import filtered_trimmed_lines
from libriichi.mjai import Bot
from libriichi.dataset import Grp

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max upload

# 全局配置
MODEL_PATH = None
ENGINE = None
BOT = None
DEVICE = torch.device('cpu')

def load_model(model_path):
    """加载 Mortal 模型"""
    global ENGINE
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"模型文件不存在: {model_path}")
    
    print(f"正在加载模型: {model_path}")
    state = torch.load(model_path, weights_only=True, map_location=DEVICE)
    cfg = state['config']
    version = cfg['control'].get('version', 1)
    num_blocks = cfg['resnet']['num_blocks']
    conv_channels = cfg['resnet']['conv_channels']
    
    # 创建模型标签
    if 'tag' in state:
        tag = state['tag']
    else:
        time = datetime.fromtimestamp(state['timestamp'], tz=timezone.utc).strftime('%y%m%d%H')
        tag = f'mortal{version}-b{num_blocks}c{conv_channels}-t{time}'
    
    # 加载神经网络
    mortal = Brain(version=version, num_blocks=num_blocks, conv_channels=conv_channels).eval()
    dqn = DQN(version=version).eval()
    mortal.load_state_dict(state['mortal'])
    dqn.load_state_dict(state['current_dqn'])
    
    # 创建引擎
    engine = MortalEngine(
        mortal,
        dqn,
        version=version,
        is_oracle=False,
        device=DEVICE,
        enable_amp=False,
        enable_quick_eval=False,  # Review mode
        enable_rule_based_agari_guard=True,
        name=tag,
    )
    
    print(f"模型加载成功! 标签: {tag}")
    return engine, tag

def analyze_game(mjai_log_text, player_id=0):
    """分析牌谱，返回每一步的 AI 建议"""
    global ENGINE
    
    if ENGINE is None:
        return {"error": "模型未加载"}
    
    # 创建 Bot
    bot = Bot(ENGINE, player_id)
    
    results = []
    logs = []
    
    lines = [line.strip() for line in mjai_log_text.strip().split('\n') if line.strip()]
    
    for line in lines:
        logs.append(line)
        
        try:
            event = json.loads(line)
            
            # 获取 AI 反应
            reaction = bot.react(line)
            
            if reaction:
                reaction_obj = json.loads(reaction)
                results.append({
                    'input': event,
                    'reaction': reaction_obj
                })
            else:
                # 对于没有反应的事件，也记录
                results.append({
                    'input': event,
                    'reaction': {'type': 'none', 'meta': {'mask_bits': 0}}
                })
        except Exception as e:
            print(f"处理行时出错: {line}")
            print(f"错误: {e}")
            continue
    
    return {
        'success': True,
        'player_id': player_id,
        'total_events': len(results),
        'events': results
    }

@app.route('/')
def index():
    """主页"""
    return render_template('index.html', model_loaded=(ENGINE is not None))

@app.route('/api/load_model', methods=['POST'])
def api_load_model():
    """加载模型 API"""
    global ENGINE, MODEL_PATH
    
    data = request.get_json()
    model_path = data.get('model_path')
    
    if not model_path:
        return jsonify({'success': False, 'error': '请提供模型路径'})
    
    try:
        engine, tag = load_model(model_path)
        ENGINE = engine
        MODEL_PATH = model_path
        return jsonify({
            'success': True,
            'message': f'模型加载成功: {tag}',
            'tag': tag
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'加载模型失败: {str(e)}'
        })

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """分析牌谱 API"""
    if ENGINE is None:
        return jsonify({'success': False, 'error': '请先加载模型'})
    
    data = request.get_json()
    mjai_log = data.get('mjai_log')
    player_id = data.get('player_id', 0)
    
    if not mjai_log:
        return jsonify({'success': False, 'error': '请提供牌谱数据'})
    
    try:
        result = analyze_game(mjai_log, player_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'分析失败: {str(e)}'
        })

@app.route('/api/status')
def api_status():
    """获取当前状态"""
    return jsonify({
        'model_loaded': ENGINE is not None,
        'model_path': MODEL_PATH,
        'device': str(DEVICE)
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    """提供静态文件"""
    return send_from_directory('static', filename)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Mortal AI 本地跑谱网站')
    parser.add_argument('--model', '-m', type=str,
                        help='模型文件路径 (例如: D:\\vscode\\Mortal\\model\\Corn.pth)')
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help='服务器端口 (默认: 5000)')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='服务器地址 (默认: 127.0.0.1)')
    
    args = parser.parse_args()
    
    # 如果提供了模型路径，预加载模型
    if args.model:
        try:
            global ENGINE, MODEL_PATH
            ENGINE, tag = load_model(args.model)
            MODEL_PATH = args.model
            print(f"✓ 模型已预加载: {tag}")
        except Exception as e:
            print(f"✗ 模型加载失败: {e}")
            print("  您可以稍后在网页界面中加载模型")
    
    print(f"\n{'='*60}")
    print(f"Mortal AI 本地跑谱网站")
    print(f"{'='*60}")
    print(f"服务器地址: http://{args.host}:{args.port}")
    print(f"模型状态: {'已加载' if ENGINE else '未加载'}")
    print(f"{'='*60}\n")
    
    # 启动服务器
    app.run(host=args.host, port=args.port, debug=True)

if __name__ == '__main__':
    main()
