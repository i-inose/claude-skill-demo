import argparse
from datetime import date
from task import TaskManager

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def format_task(task) -> str:
    status = "✅" if task.done else "⬜"
    due = f" (期限: {task.due_date})" if task.due_date else ""
    priority_label = {"high": "[高]", "medium": "[中]", "low": "[低]"}.get(task.priority, "")
    return f"{status} [{task.id}] {task.title}{due} {priority_label}"


def cmd_add(args, manager: TaskManager):
    due = date.fromisoformat(args.due) if args.due else None
    task = manager.add(args.title, due_date=due, priority=args.priority)
    print(f"タスクを追加しました: [{task.id}] {task.title}")


def cmd_list(args, manager: TaskManager):
    tasks = manager.list_tasks(show_done=args.all, priority=getattr(args, "priority", None))
    if not tasks:
        print("タスクはありません")
        return
    for task in tasks:
        print(format_task(task))


def cmd_done(args, manager: TaskManager):
    if manager.complete(args.id):
        print(f"タスク [{args.id}] を完了にしました")
    else:
        print(f"タスク [{args.id}] が見つかりません")


def cmd_delete(args, manager: TaskManager):
    if manager.delete(args.id):
        print(f"タスク [{args.id}] を削除しました")
    else:
        print(f"タスク [{args.id}] が見つかりません")


def main():
    parser = argparse.ArgumentParser(description="タスク管理 CLI")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="タスクを追加")
    p_add.add_argument("title")
    p_add.add_argument("--due", help="期限日 (YYYY-MM-DD)")
    p_add.add_argument("--priority", choices=["high", "medium", "low"], default="medium")

    p_list = sub.add_parser("list", help="タスク一覧")
    p_list.add_argument("--all", action="store_true", help="完了済みも表示")
    p_list.add_argument("--priority", choices=["high", "medium", "low"], help="優先度でフィルタ")

    p_done = sub.add_parser("done", help="タスクを完了")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="タスクを削除")
    p_del.add_argument("id", type=int)

    args = parser.parse_args()
    manager = TaskManager()

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "delete": cmd_delete,
    }

    if args.command in commands:
        commands[args.command](args, manager)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
