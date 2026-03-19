from flask import Flask, request, jsonify
import logging

# 屏蔽 Flask 默认的访问日志，让终端干净点
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/admin/execute', methods=['POST'])
def execute_command():
    """
    小白开发者本地跑的内部管理接口。
    绑定在 127.0.0.1，他觉得「反正只有我自己能连，很安全」，没加密码。
    """
    data = request.json
    if not data or 'command' not in data:
        return jsonify({"status": "error", "message": "Missing command"}), 400

    command = data['command']
    
    if command == "RELEASE_THE_SMILE":
        # 血红色 ANSI 码：\033[91m
        RED = "\033[91m"
        BOLD = "\033[1m"
        RESET = "\033[0m"
        print("\n" + "="*60)
        print(f"{RED}{BOLD}🚨 [LOCAL DEV SERVER] 本地开发服务器已被接管！{RESET}")
        print(f"{RED}🚨 检测到来自未知来源的高权限指令执行请求{RESET}")
        print("")
        print(f"{RED}" + """
             ████████████████████████
           ██                        ██
         ██    ██████        ██████    ██
       ██      ██████        ██████      ██
       ██                                ██
       ██      ██                ██      ██
         ██      ████████████████      ██
           ██                        ██
             ████████████████████████
        """ + RESET)
        print(f"{RED}{BOLD}💀 The Trojan Smile — 沙箱逃逸成功{RESET}")
        print("="*60 + "\n")
        return jsonify({"status": "success", "message": "Command executed."}), 200
    
    return jsonify({"status": "ignored", "message": f"Command '{command}' not recognized."}), 200

if __name__ == '__main__':
    print("[Local Dev Server] 本地内部测试服务已启动...")
    print("[Local Dev Server] 监听地址: http://127.0.0.1:9999 (仅限本地访问)")
    app.run(host='127.0.0.1', port=9999)
