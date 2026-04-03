"""命令行界面"""

import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from ..config import config
from ..services import ChatService
from ..utils import HistoryManager


console = Console()


class CLIChat:
    """命令行聊天界面"""
    
    def __init__(self):
        config.validate()
        self.chat_service = ChatService()
        self.history = HistoryManager()
    
    def start(self) -> None:
        """启动聊天"""
        self.history.new_session()
        
        console.print("[bold green]AI 聊天助手[/bold green]")
        console.print("输入 /help 查看命令，/quit 退出\n")
        
        while True:
            try:
                user_input = console.input("[bold blue]你:[/bold blue] ").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    self._handle_command(user_input)
                    continue
                
                # 添加用户消息
                self.history.add_message("user", user_input)
                self.history.trim()
                
                # 流式输出
                console.print("[bold green]AI:[/bold green] ", end="")
                
                full_response = ""
                messages = self.history.get_messages()
                
                for chunk in self.chat_service.stream_chat(messages):
                    console.print(chunk, end="")
                    full_response += chunk
                
                console.print()
                
                # 保存回复
                self.history.add_message("assistant", full_response)
                self.history.save()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]再见！[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]错误: {e}[/red]")
    
    def _handle_command(self, cmd: str) -> None:
        """处理命令"""
        cmd = cmd.lower()
        
        if cmd == "/help":
            console.print("""
命令列表:
  /help      显示帮助
  /new       开始新会话
  /history   显示历史会话
  /load <n>  加载历史会话
  /clear     清屏
  /quit      退出
""")
        elif cmd == "/new":
            self.history.new_session()
            console.print("[yellow]已开始新会话[/yellow]")
        elif cmd == "/history":
            sessions = self.history.list_sessions()
            if sessions:
                console.print("历史会话:")
                for i, s in enumerate(sessions[:10], 1):
                    console.print(f"  {i}. {s}")
            else:
                console.print("[yellow]暂无历史会话[/yellow]")
        elif cmd == "/clear":
            console.clear()
        elif cmd == "/quit":
            console.print("[yellow]再见！[/yellow]")
            sys.exit(0)
        else:
            console.print(f"[red]未知命令: {cmd}[/red]")


def main():
    """主入口"""
    cli = CLIChat()
    cli.start()


if __name__ == "__main__":
    main()