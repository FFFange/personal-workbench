# -*- coding: utf-8 -*-
"""
背单词抽测器 —— 边用边学 Python

用法：
    python 背单词.py          开始抽测（默认 5 题）
    python 背单词.py 10       抽 10 题

词库放在同目录的 words.txt，每行一个：英文,中文
（第一次运行会自动生成一个示例词库，你可以往里加自己的单词）

本文件的教学点：
  1. 读写文件（with open）
  2. 列表和字典（存单词）
  3. random 随机抽样（出题）
  4. 函数（把大任务拆小）
  5. 异常处理（try/except，防止坏输入把程序搞崩）
"""

import random   # 随机数模块：抽题、打乱选项都靠它
import sys      # 系统模块：读命令行参数用
import os       # 操作系统模块：判断文件存不存在

# 程序所在目录下的词库文件名
WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")
WRONG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrong.txt")

# 内置示例词库：第一次运行时写入 words.txt，之后就可以自己改
SAMPLE_WORDS = [
    ("apple", "苹果"),
    ("banana", "香蕉"),
    ("orange", "橙子"),
    ("grape", "葡萄"),
    ("watermelon", "西瓜"),
    ("strawberry", "草莓"),
    ("peach", "桃子"),
    ("lemon", "柠檬"),
]


def load_words():
    """从 words.txt 读词库，返回 [(英文, 中文), ...] 列表。

    教学点：with open(...) 会在用完文件后自动关闭，不用手动 close。
    encoding="utf-8" 是为了让中文不乱码。
    """
    # 如果词库文件不存在，先把示例词库写进去
    if not os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "w", encoding="utf-8") as f:
            for en, zh in SAMPLE_WORDS:
                f.write(en + "," + zh + "\n")
        print("已生成示例词库 words.txt，你可以往里加自己的单词！格式：英文,中文\n")

    words = []
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()          # 去掉行首尾的空格和换行符
            if not line or "," not in line:
                continue                 # 跳过空行和格式不对的行
            en, zh = line.split(",", 1)  # 按第一个逗号切成两半
            words.append((en.strip(), zh.strip()))
    return words


def make_question(words):
    """出一道选择题：给英文选中文，1 个正确答案 + 3 个干扰项。

    教学点：random.sample(列表, n) 表示“不放回地随机抽 n 个”。
    """
    answer = random.choice(words)                # 随机选一个当正确答案
    distractors = random.sample(                 # 从其余单词里抽 3 个当干扰项
        [w for w in words if w != answer],       # 列表推导式：筛掉正确答案
        min(3, len(words) - 1)
    )
    options = [answer[1]] + [w[1] for w in distractors]  # 拼出中文选项列表
    random.shuffle(options)                      # 打乱选项顺序，不然答案总在第一个
    return answer, options


def save_wrong(en, zh):
    """把答错的词追加到 wrong.txt，方便之后重点复习。

    教学点：open 的模式 "a" 是 append（追加），不会覆盖旧内容。
    """
    with open(WRONG_FILE, "a", encoding="utf-8") as f:
        f.write(en + "," + zh + "\n")


def quiz(total):
    """主流程：出 total 道题，统计得分。"""
    words = load_words()
    if len(words) < 4:
        print("词库至少要有 4 个单词才能出选择题，先去 words.txt 里加点词吧！")
        return

    score = 0
    for i in range(1, total + 1):
        answer, options = make_question(words)
        print("\n第 {}/{} 题：{} 的中文是？".format(i, total, answer[0]))
        for j, opt in enumerate(options):
            # enumerate 同时给你序号和内容；字母选项 A/B/C/D 用 chr(65+j) 生成
            print("  {}) {}".format(chr(65 + j), opt))

        # 教学点：try/except 抓住坏输入，程序就不会崩
        try:
            choice = input("你的答案（A/B/C/D，q 退出）: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            break
        if choice == "Q":
            print("提前交卷！")
            break

        # 把字母转成下标：ord("A") 是 65，减 65 就得到 0
        idx = ord(choice[0]) - 65 if choice else -1
        if 0 <= idx < len(options) and options[idx] == answer[1]:
            print("✓ 答对了！")
            score += 1
        else:
            print("✗ 错了，正确答案是：{}".format(answer[1]))
            save_wrong(answer[0], answer[1])     # 错题记小本本

    print("\n===== 交卷 =====")
    print("得分：{}/{}".format(score, total))
    if os.path.exists(WRONG_FILE):
        print("错题已存进 wrong.txt，记得回头看一眼。")


if __name__ == "__main__":
    # sys.argv 是命令行参数列表：sys.argv[0] 是脚本名，后面才是参数
    n = 5
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("题数得是个数字，按默认 5 题来。")
    quiz(n)
