import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_name TEXT NOT NULL,
            amount REAL NOT NULL,
            pay_time TEXT NOT NULL,
            product_description TEXT,
            order_no TEXT,
            category TEXT DEFAULT '其他',
            remark TEXT,
            screenshot_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_sample_data():
    """插入已有的消费数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM expenses")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # 已有的消费记录
    expenses = [
        ("北京月之暗面科技有限公司", 50.00, "2026-02-02 15:35:27", "账户充值", "2026020222001491831458522286", "API/AI服务", "", "file_30---cbd1e0eb-839a-41f6-a1a4-a4923c2c2306.jpg"),
        ("湖北省星浪永盛橱柜有限公司", 19.98, "2026-01-31 10:49:49", "3180854", "2026013122001491831450994506", "其他", "", "file_31---7fd2b554-fc74-4aac-a49c-b5b3e8c2c362.jpg"),
        ("闲鱼", 24.90, "2026-01-26 14:15:55", "Claude Code sonnet/opus 4.5模型国内", "", "API/AI服务", "", "file_32---8e1b2104-d873-4255-8cd6-f2096e6d12a5.jpg"),
        ("北京月之暗面科技有限公司", 4.99, "2026-02-04 08:17:10", "Kimi VIP", "4200003025202602049149799068", "API/AI服务", "", "file_33---f54034f6-59a8-4db3-8df6-22f8bb126f8a.jpg"),
        ("腾讯云", 42.00, "2026-01-26 11:34:49", "腾讯云购买云服务-100046059704", "4200002977202601268884135778", "云服务", "", "file_34---da8e2524-82c5-47fe-af4c-b19d57860ef9.jpg"),
        ("霜格科技", 15.99, "2026-01-23 09:40:46", "快冲冲 120w超级快充数据线typec", "2026012322001491831424715177", "数码配件", "", "file_35---71e64842-59ac-4003-bcc2-e11f2f5ab017.jpg"),
        ("合肥市呈零网络科技有限公司", 15.99, "2026-01-16 09:35:17", "游戏币/平台道具充值(即时到账)", "2026011622001491831459148310", "游戏/娱乐", "", "file_36---5db8aa04-8109-41f7-a92b-72143d8f341f.jpg"),
        ("合肥市珈迪网络科技有限公司", 15.99, "2026-01-09 01:49:27", "游戏币/平台道具充值(即时到账)", "202601160935003330415", "游戏/娱乐", "", "file_37---8ee84620-9def-4010-b1a3-4618a054b645.jpg"),
        ("厦门市砚汴见网络科技有限公司", 19.98, "2026-01-02 01:40:51", "软件定制开发ERP企业管理系统APP程序OA办公小程序设计java代做H5", "2026010222001491831408173919", "软件开发", "", "file_38---b04ba9ac-d7bb-4e81-be3c-bb3543901111.jpg"),
    ]
    
    cursor.executemany('''
        INSERT INTO expenses (merchant_name, amount, pay_time, product_description, order_no, category, remark, screenshot_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', expenses)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """首页 - 纯 HTML 版本（无外部依赖）"""
    return render_template('index.html')

@app.route('/react')
def react_version():
    """React 版本"""
    return render_template('index_react.html')

@app.route('/classic')
def classic():
    """经典版本 - 按月统计"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 按月统计
    cursor.execute('''
        SELECT 
            strftime('%Y-%m', pay_time) as month,
            COUNT(*) as count,
            SUM(amount) as total,
            category,
            SUM(amount) as category_total
        FROM expenses
        GROUP BY strftime('%Y-%m', pay_time), category
        ORDER BY month DESC, category_total DESC
    ''')
    
    rows = cursor.fetchall()
    
    # 整理数据
    stats = {}
    for row in rows:
        month, count, total, category, cat_total = row
        if month not in stats:
            stats[month] = {
                'total': 0,
                'count': 0,
                'categories': {}
            }
        stats[month]['categories'][category] = cat_total
        stats[month]['total'] += cat_total
        stats[month]['count'] += count
    
    # 获取所有记录
    cursor.execute('''
        SELECT * FROM expenses 
        ORDER BY pay_time DESC
    ''')
    columns = [description[0] for description in cursor.description]
    expenses = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('index.html', stats=stats, expenses=expenses)

@app.route('/api/expenses')
def api_expenses():
    """API: 获取所有消费记录 + 月度统计"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取所有记录
    cursor.execute('SELECT * FROM expenses ORDER BY pay_time DESC')
    columns = [description[0] for description in cursor.description]
    expenses = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # 按月统计
    cursor.execute('''
        SELECT 
            strftime('%Y-%m', pay_time) as month,
            COUNT(*) as count,
            SUM(amount) as total,
            category,
            SUM(amount) as category_total
        FROM expenses
        GROUP BY strftime('%Y-%m', pay_time), category
        ORDER BY month DESC, category_total DESC
    ''')
    
    rows = cursor.fetchall()
    
    # 整理月度数据
    stats = {}
    for row in rows:
        month, count, total, category, cat_total = row
        if month not in stats:
            stats[month] = {
                'total': 0,
                'count': 0,
                'categories': {}
            }
        stats[month]['categories'][category] = cat_total
        stats[month]['total'] += cat_total
        stats[month]['count'] += count
    
    conn.close()
    
    return jsonify({
        'expenses': expenses,
        'stats': stats
    })

@app.route('/api/stats')
def api_stats():
    """API: 获取统计信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 总体统计
    cursor.execute('SELECT COUNT(*), SUM(amount), AVG(amount) FROM expenses')
    total_count, total_amount, avg_amount = cursor.fetchone()
    
    # 按月份统计
    cursor.execute('''
        SELECT strftime('%Y-%m', pay_time) as month, COUNT(*), SUM(amount)
        FROM expenses
        GROUP BY strftime('%Y-%m', pay_time)
        ORDER BY month DESC
    ''')
    month_stats = [{'month': row[0], 'count': row[1], 'total': row[2]} for row in cursor.fetchall()]
    
    # 按类别统计
    cursor.execute('''
        SELECT category, COUNT(*), SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    ''')
    category_stats = [{'category': row[0], 'count': row[1], 'total': row[2]} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_count': total_count,
        'total_amount': total_amount,
        'avg_amount': avg_amount,
        'month_stats': month_stats,
        'category_stats': category_stats
    })

@app.route('/screenshots/<path:filename>')
def screenshots(filename):
    """提供截图文件"""
    return send_from_directory('/root/project/pay_for_tools', filename)

@app.route('/add', methods=['POST'])
def add_expense():
    """添加新消费记录"""
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO expenses (merchant_name, amount, pay_time, product_description, order_no, category, remark)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('merchant_name'),
        data.get('amount'),
        data.get('pay_time'),
        data.get('product_description'),
        data.get('order_no'),
        data.get('category', '其他'),
        data.get('remark', '')
    ))
    
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'id': expense_id})

@app.route('/api/expense/<int:expense_id>/remark', methods=['POST'])
def update_remark(expense_id):
    """更新支出备注"""
    data = request.json
    remark = data.get('remark', '')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET remark = ? WHERE id = ?', (remark, expense_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    return jsonify({'success': updated})

@app.route('/api/expense/<int:expense_id>/category', methods=['POST'])
def update_category(expense_id):
    """更新支出分类"""
    data = request.json
    category = data.get('category', '')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET category = ? WHERE id = ?', (category, expense_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    return jsonify({'success': updated})

# 静态测试页面路由
@app.route('/ai-chat-test.html')
def ai_chat_test():
    """AI聊天测试页"""
    return send_from_directory('/var/www/test-pages', 'ai-chat-test.html')

@app.route('/financial-dashboard.html')
def financial_dashboard():
    """财务报表仪表盘"""
    return send_from_directory('/var/www/test-pages', 'financial-dashboard.html')

if __name__ == '__main__':
    init_db()
    insert_sample_data()
    app.run(host='0.0.0.0', port=5007, debug=True)
