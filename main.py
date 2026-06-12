import random
import copy


class Interactive2048:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.number_sequence = [2, 4, 8, 16]
        self.sequence_index = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.grid[row][col] = 2 if random.random() < 0.9 else 4

    def set_cell(self, row, col, value=None):
        if not (0 <= row <= 3 and 0 <= col <= 3):
            return False

        if value is None:
            value = self.number_sequence[self.sequence_index]
            self.sequence_index = (self.sequence_index + 1) % len(self.number_sequence)

        if value < 0 or (value > 0 and (value & (value - 1)) != 0):
            return False

        self.grid[row][col] = value
        return True

    def clear_cell(self, row, col):
        return self.set_cell(row, col, 0)

    def fill_row(self, row, values):
        if len(values) != 4:
            return False
        for col, value in enumerate(values):
            if value < 0 or (value > 0 and (value & (value - 1)) != 0):
                return False
            self.grid[row][col] = value
        return True

    def fill_column(self, col, values):
        if len(values) != 4:
            return False
        for row, value in enumerate(values):
            if value < 0 or (value > 0 and (value & (value - 1)) != 0):
                return False
            self.grid[row][col] = value
        return True

    def move(self, direction):
        """执行移动操作（带合并逻辑），返回是否改变了棋盘"""
        original_grid = copy.deepcopy(self.grid)
        moved = False

        if direction == 'w':  # 上移
            for col in range(4):
                numbers = []
                for row in range(4):
                    if self.grid[row][col] != 0:
                        numbers.append(self.grid[row][col])

                merged = []
                i = 0
                while i < len(numbers):
                    if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
                        merged.append(numbers[i] * 2)
                        self.score += numbers[i] * 2
                        i += 2
                    else:
                        merged.append(numbers[i])
                        i += 1

                # 检查是否有变化（合并或位置变动）
                original_col = [original_grid[row][col] for row in range(4)]
                new_col = [merged[row] if row < len(merged) else 0 for row in range(4)]

                if original_col != new_col:
                    moved = True
                    for row in range(4):
                        self.grid[row][col] = new_col[row]

        elif direction == 's':  # 下移
            for col in range(4):
                numbers = []
                for row in range(3, -1, -1):
                    if self.grid[row][col] != 0:
                        numbers.append(self.grid[row][col])

                merged = []
                i = 0
                while i < len(numbers):
                    if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
                        merged.append(numbers[i] * 2)
                        self.score += numbers[i] * 2
                        i += 2
                    else:
                        merged.append(numbers[i])
                        i += 1

                original_col = [original_grid[row][col] for row in range(4)]
                new_col = [merged[3 - row] if 3 - row < len(merged) else 0 for row in range(4)]

                if original_col != new_col:
                    moved = True
                    for row in range(4):
                        self.grid[row][col] = new_col[row]

        elif direction == 'a':  # 左移
            for row in range(4):
                numbers = []
                for col in range(4):
                    if self.grid[row][col] != 0:
                        numbers.append(self.grid[row][col])

                merged = []
                i = 0
                while i < len(numbers):
                    if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
                        merged.append(numbers[i] * 2)
                        self.score += numbers[i] * 2
                        i += 2
                    else:
                        merged.append(numbers[i])
                        i += 1

                original_row = original_grid[row]
                new_row = [merged[col] if col < len(merged) else 0 for col in range(4)]

                if original_row != new_row:
                    moved = True
                    self.grid[row] = new_row

        elif direction == 'd':  # 右移
            for row in range(4):
                numbers = []
                for col in range(3, -1, -1):
                    if self.grid[row][col] != 0:
                        numbers.append(self.grid[row][col])

                merged = []
                i = 0
                while i < len(numbers):
                    if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
                        merged.append(numbers[i] * 2)
                        self.score += numbers[i] * 2
                        i += 2
                    else:
                        merged.append(numbers[i])
                        i += 1

                original_row = original_grid[row]
                new_row = [merged[3 - col] if 3 - col < len(merged) else 0 for col in range(4)]

                if original_row != new_row:
                    moved = True
                    self.grid[row] = new_row

        if moved:
            self.add_random_tile()
            self.check_game_over()
        return moved

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        self.game_over = True
        return True

    def get_ai_suggestion(self):
        """AI：总是推荐一个方向，即使只是挪动数字"""
        directions = ['w', 's', 'a', 'd']
        best_dir = None
        best_score = -float('inf')

        for direction in directions:
            test_game = copy.deepcopy(self)
            test_game.move(direction)  # 不管有没有合并，都执行移动

            score = self.evaluate_position(test_game)
            if score > best_score:
                best_score = score
                best_dir = direction

        return best_dir  # 保证永远有返回值

    def evaluate_position(self, game_state):
        """评估棋盘状态的得分"""
        score = 0

        # 1. 空位数量（最高优先级）
        empty_cells = sum(1 for i in range(4) for j in range(4) if game_state.grid[i][j] == 0)
        score += empty_cells * 400

        # 2. 大数字在角落（战略优势）
        max_num = max(max(row) for row in game_state.grid) if any(any(row) for row in game_state.grid) else 0
        corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
        for i, j in corners:
            if game_state.grid[i][j] == max_num:
                score += 600

        # 3. 数字聚合度（鼓励相似数字靠在一起）
        cluster_score = 0
        for i in range(4):
            for j in range(4):
                current = game_state.grid[i][j]
                if current == 0:
                    continue

                # 检查周围是否有相同数字
                neighbors = []
                if j < 3: neighbors.append(game_state.grid[i][j + 1])  # 右
                if i < 3: neighbors.append(game_state.grid[i + 1][j])  # 下
                if j > 0: neighbors.append(game_state.grid[i][j - 1])  # 左
                if i > 0: neighbors.append(game_state.grid[i - 1][j])  # 上

                for neighbor in neighbors:
                    if neighbor == current:
                        cluster_score += current * 15

        score += cluster_score

        # 4. 避免中间塞满小数字
        center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        for i, j in center_positions:
            if game_state.grid[i][j] > 0 and game_state.grid[i][j] < 8:
                score -= 50

        return score

    def display(self):
        """显示带坐标的棋盘"""
        print("\n" + "═" * 44)
        print("🎮 持续提示版 2048 - AI从不放弃！")
        print("═" * 44)
        print(f"📊 分数: {self.score} | 下一数字: {self.number_sequence[self.sequence_index]}")

        if self.game_over:
            print("⚠️  游戏结束！")

        print("   ", end="")
        for col in range(4):
            print(f"   {col}  ", end="")
        print("\n   ┌──────┬──────┬──────┬──────┐")

        for i in range(4):
            print(f"{i} │", end="")
            for j in range(4):
                if self.grid[i][j] == 0:
                    print("      │", end="")
                else:
                    print(f" {self.grid[i][j]:4} │", end="")
            print(f" {i}")

            if i < 3:
                print("   ├──────┼──────┼──────┼──────┤")
            else:
                print("   └──────┴──────┴──────┴──────┘")

        print("   ", end="")
        for col in range(4):
            print(f"   {col}  ", end="")
        print("\n" + "═" * 44)


def parse_coordinate(input_str):
    if len(input_str) == 2 and input_str.isdigit():
        row, col = int(input_str[0]), int(input_str[1])
        return (row, col) if 0 <= row <= 3 and 0 <= col <= 3 else None

    parts = input_str.replace(',', ' ').replace('.', ' ').split()
    if len(parts) == 2 and all(part.isdigit() for part in parts):
        row, col = int(parts[0]), int(parts[1])
        return (row, col) if 0 <= row <= 3 and 0 <= col <= 3 else None

    return None


def main():
    game = Interactive2048()

    print("🌟" * 54)
    print("🎮 无限提示版 2048 - 在任何局面都有AI建议！")
    print("🌟" * 54)
    print("🔥 核心逻辑：")
    print("  • AI 永远推荐一个方向（即使只是挪动数字）")
    print("  • 你可以移动后手动加空格，打破死局继续玩")
    print("  • 评估侧重：空位 > 角落大数 > 数字聚合")
    print("-" * 64)
    print("⚡ 快捷操作：")
    print("  📍 00=32 或 00=2^5     🚫 c00      ➡️  w/s/a/d")
    print("  🧠 h (AI建议)  📁 row0 2 4 2 4")
    print("  🗑️  r (重置)    💾 q (退出)")
    print("🌟" * 54)

    game.display()

    while True:
        user_input = input("\n🎯 请输入指令: ").strip()

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd == 'q':
            print("👋 感谢使用！再见～")
            break

        elif cmd in ['w', 's', 'a', 'd']:
            if game.move(cmd):
                game.display()
            else:
                print("⚠️ 这个方向没有变化（但你可以加空格继续）")
                game.display()

        elif cmd == 'h':
            suggestion = game.get_ai_suggestion()
            dir_map = {'w': '⬆️ 向上', 's': '⬇️ 向下', 'a': '⬅️ 向左', 'd': '➡️ 向右'}
            print(f"🤖 AI推荐: {dir_map[suggestion]}")

            # 额外提示
            test_game = copy.deepcopy(game)
            test_game.move(suggestion)
            empty_cells = sum(1 for i in range(4) for j in range(4) if test_game.grid[i][j] == 0)
            print(f"💡 移动后预计空位: {empty_cells}")

        elif cmd == 'r':
            game = Interactive2048()
            print("🔄 棋盘已重置！")
            game.display()

        elif '=' in user_input:
            parts = user_input.split('=', 1)
            coord_part = parts[0].strip()
            value_part = parts[1].strip()

            coords = parse_coordinate(coord_part)
            if coords:
                row, col = coords
                if '^' in value_part:
                    base_exp = value_part.split('^', 1)
                    if len(base_exp) == 2 and base_exp[0].strip() == '2' and base_exp[1].strip().isdigit():
                        exp = int(base_exp[1].strip())
                        value = 2 ** exp
                    else:
                        print("❌ 指数格式错误！正确格式: 00=2^5")
                        continue
                elif value_part.isdigit():
                    value = int(value_part)
                else:
                    print("❌ 格式错误！正确格式: 00=32 或 00=2^5")
                    continue

                if game.set_cell(row, col, value):
                    game.display()
                else:
                    print("❌ 无效数值！只能使用 0 或 2 的幂次方")
            else:
                print("❌ 格式错误！正确格式: 00=32 或 00=2^5")

        elif user_input.startswith('c'):
            coord_part = user_input[1:].strip()
            coords = parse_coordinate(coord_part)
            if coords:
                row, col = coords
                if game.clear_cell(row, col):
                    game.display()
                else:
                    print("❌ 无法清空该位置")
            else:
                print("❌ 无效坐标！正确格式: c00 或 c 0,0")

        elif user_input.startswith('row'):
            parts = user_input[3:].strip().split()
            if len(parts) >= 2 and parts[0].isdigit():
                row = int(parts[0])
                if 0 <= row <= 3:
                    values = []
                    valid = True
                    for val in parts[1:]:
                        if '^' in val:
                            base_exp = val.split('^', 1)
                            if len(base_exp) == 2 and base_exp[0].strip() == '2' and base_exp[1].strip().isdigit():
                                exp = int(base_exp[1].strip())
                                values.append(2 ** exp)
                            else:
                                print("❌ 指数格式错误！正确格式: 2^5")
                                valid = False
                                break
                        elif val.isdigit():
                            values.append(int(val))
                        else:
                            print("❌ 数值必须为整数或 2^n 格式")
                            valid = False
                            break
                    if valid:
                        if len(values) == 4:
                            if game.fill_row(row, values):
                                game.display()
                            else:
                                print("❌ 只能填入 0 或 2 的幂次方")
                        else:
                            print(f"❌ 需要4个数值，当前提供了{len(values)}个")
                else:
                    print("❌ 行号必须在 0-3 之间")
            else:
                print("❌ 格式错误！正确格式: row0 2 4 2^5 16")

        elif user_input.startswith('col'):
            parts = user_input[3:].strip().split()
            if len(parts) >= 2 and parts[0].isdigit():
                col = int(parts[0])
                if 0 <= col <= 3:
                    values = []
                    valid = True
                    for val in parts[1:]:
                        if '^' in val:
                            base_exp = val.split('^', 1)
                            if len(base_exp) == 2 and base_exp[0].strip() == '2' and base_exp[1].strip().isdigit():
                                exp = int(base_exp[1].strip())
                                values.append(2 ** exp)
                            else:
                                print("❌ 指数格式错误！正确格式: 2^5")
                                valid = False
                                break
                        elif val.isdigit():
                            values.append(int(val))
                        else:
                            print("❌ 数值必须为整数或 2^n 格式")
                            valid = False
                            break
                    if valid:
                        if len(values) == 4:
                            if game.fill_column(col, values):
                                game.display()
                            else:
                                print("❌ 只能填入 0 或 2 的幂次方")
                        else:
                            print(f"❌ 需要4个数值，当前提供了{len(values)}个")
                else:
                    print("❌ 列号必须在 0-3 之间")
            else:
                print("❌ 格式错误！正确格式: col1 0 0 2^3 4")

        else:
            print("❓ 未知指令！输入 help 查看全部命令")


if __name__ == "__main__":
    main()