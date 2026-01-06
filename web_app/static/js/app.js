// Mortal AI 跑谱网站 JavaScript

// 检查模型状态
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const statusBadge = document.getElementById('modelStatus');
        const modelInfo = document.getElementById('modelInfo');
        
        if (data.model_loaded) {
            statusBadge.textContent = '✓ 模型已加载';
            statusBadge.className = 'status-badge status-success';
            modelInfo.textContent = `路径: ${data.model_path}`;
        } else {
            statusBadge.textContent = '模型未加载';
            statusBadge.className = 'status-badge status-warning';
            modelInfo.textContent = '';
        }
    } catch (error) {
        console.error('检查状态失败:', error);
    }
}

// 加载模型
async function loadModel() {
    const modelPath = document.getElementById('modelPath').value;
    const resultBox = document.getElementById('loadResult');
    
    if (!modelPath) {
        showResult(resultBox, '请输入模型路径', 'error');
        return;
    }
    
    resultBox.textContent = '正在加载模型...';
    resultBox.className = 'result-box';
    resultBox.style.display = 'block';
    
    try {
        const response = await fetch('/api/load_model', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ model_path: modelPath })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult(resultBox, `✓ ${data.message}`, 'success');
            checkStatus();
        } else {
            showResult(resultBox, `✗ ${data.error}`, 'error');
        }
    } catch (error) {
        showResult(resultBox, `✗ 请求失败: ${error.message}`, 'error');
    }
}

// 分析牌谱
async function analyzeGame() {
    const mjaiLog = document.getElementById('mjaiLog').value;
    const playerId = parseInt(document.getElementById('playerSelect').value);
    const resultBox = document.getElementById('analyzeResult');
    
    if (!mjaiLog.trim()) {
        showResult(resultBox, '请输入牌谱数据', 'error');
        return;
    }
    
    resultBox.textContent = '正在分析牌谱...';
    resultBox.className = 'result-box';
    resultBox.style.display = 'block';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mjai_log: mjaiLog,
                player_id: playerId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult(resultBox, `✓ 分析完成! 共 ${data.total_events} 个事件`, 'success');
            displayResults(data);
        } else {
            showResult(resultBox, `✗ ${data.error}`, 'error');
        }
    } catch (error) {
        showResult(resultBox, `✗ 分析失败: ${error.message}`, 'error');
    }
}

// 显示结果
function showResult(element, message, type) {
    element.textContent = message;
    element.className = `result-box ${type}`;
    element.style.display = 'block';
}

// 显示分析结果
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsSummary = document.getElementById('resultsSummary');
    const eventsContainer = document.getElementById('eventsContainer');
    
    resultsSection.style.display = 'block';
    
    // 显示摘要
    resultsSummary.innerHTML = `
        <h3>分析摘要</h3>
        <p><strong>分析玩家:</strong> ${data.player_id}</p>
        <p><strong>总事件数:</strong> ${data.total_events}</p>
        <p><strong>AI 反应数:</strong> ${data.events.filter(e => e.reaction.type !== 'none').length}</p>
    `;
    
    // 显示每个事件
    eventsContainer.innerHTML = '';
    
    data.events.forEach((event, index) => {
        const hasReaction = event.reaction.type !== 'none';
        const eventCard = document.createElement('div');
        eventCard.className = `event-card ${hasReaction ? 'has-reaction' : ''}`;
        
        let eventHtml = `
            <div class="event-header">
                <span class="event-type">事件 #${index + 1}: ${event.input.type}</span>
                ${event.input.actor !== undefined ? `<span class="event-actor">玩家 ${event.input.actor}</span>` : ''}
            </div>
            <div class="event-content">
                <strong>输入:</strong> ${JSON.stringify(event.input, null, 2)}
            </div>
        `;
        
        if (hasReaction) {
            eventHtml += `
                <div class="ai-recommendation">
                    <strong>🤖 AI 建议:</strong> ${event.reaction.type}
                    ${event.reaction.pai ? ` - ${event.reaction.pai}` : ''}
                    ${event.reaction.meta && event.reaction.meta.q_values ? 
                        `<div class="q-values">Q值: ${event.reaction.meta.q_values.slice(0, 5).map(v => v.toFixed(2)).join(', ')}...</div>` : ''}
                </div>
            `;
        }
        
        eventCard.innerHTML = eventHtml;
        eventsContainer.appendChild(eventCard);
    });
    
    // 滚动到结果
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// 页面加载时检查状态
window.addEventListener('DOMContentLoaded', () => {
    checkStatus();
});
