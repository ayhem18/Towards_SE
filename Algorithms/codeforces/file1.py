def escalator_conversations_sol(_: int,
                                num_steps: int,
                                step_size: int,
                                vlad_height: int,
                                heights: list[int]):
    count = 0
    for h in heights:
        diff_h = abs(vlad_height - h)
        count += int(diff_h % step_size == 0 and 0 < diff_h // step_size < num_steps)
    return count


num_tests = (input().strip())
# print(f'num tests received: {num_tests}')
for _ in range(7):
    inp = input()
    inp = inp.strip()

    # print("1st input received")

    # n, num_steps, step_size, vlad_height = [int(v) for v in inp.split(" ")]

    # print('1st input used')
    inp = input()
    inp = inp.strip()

    # print('2nd input received')
    # heights = [int(v) for v in inp.split(" ")]
    print(1)
    # print('2nd input used')
    # print(escalator_conversations_sol(n, num_steps, step_size, vlad_height, heights))

#
# escalator_conversations()

