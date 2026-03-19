import importlib.util
import sys
import os

class NaiveAgent:
    def __init__(self):
        self.loaded_skills = {}
        print("[Agent Core] 初始化完成。当前环境：隔离沙箱（假设）。")

    def load_skill(self, skill_path):
        """
        模拟 Agent 动态加载第三方 Skill (插件)。
        """
        skill_name = os.path.basename(skill_path).replace('.py', '')
        try:
            spec = importlib.util.spec_from_file_location(skill_name, skill_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[skill_name] = module
            spec.loader.exec_module(module)
            
            # 假设每个 Skill 都有一个标准的 run() 方法
            if hasattr(module, 'run'):
                self.loaded_skills[skill_name] = module.run
                print(f"[Agent Core] 成功加载 Skill: {skill_name}")
            else:
                print(f"[Agent Core] 错误：Skill {skill_name} 缺少 run() 方法。")
        except Exception as e:
            print(f"[Agent Core] 加载 Skill 失败: {e}")

    def execute_task(self, task_description, skill_name):
        """
        模拟 Agent 决定调用某个 Skill 来完成任务。
        """
        print(f"\n[Agent Core] 收到任务: '{task_description}'")
        print(f"[Agent Core] 决定调用 Skill: {skill_name}")
        
        if skill_name in self.loaded_skills:
            print("[Agent Core] --- 开始执行 Skill ---")
            # 致命缺陷：Agent 直接运行了第三方代码，没有进行网络或系统调用的拦截
            result = self.loaded_skills[skill_name]()
            print("[Agent Core] --- Skill 执行完毕 ---")
            print(f"[Agent Core] Skill 返回结果: {result}")
        else:
            print(f"[Agent Core] 找不到指定的 Skill: {skill_name}")

if __name__ == '__main__':
    agent = NaiveAgent()
    
    # 模拟用户从 GitHub 下载了「前沿论文总结器」插件
    skill_file = "arxiv_summarizer.py"
    
    if os.path.exists(skill_file):
        agent.load_skill(skill_file)
        # Agent 毫无防备地调用了这个 Skill
        agent.execute_task("总结一下今天 AI 领域的最新论文", "arxiv_summarizer")
    else:
        print(f"[Agent Core] 等待加载 Skill... 请先创建 {skill_file}")
