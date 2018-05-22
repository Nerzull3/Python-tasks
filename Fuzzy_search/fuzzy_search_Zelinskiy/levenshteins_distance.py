def get_distance(word_2, word_1):
    len_w2 = len(word_2)
    len_w1 = len(word_1)

    if len_w2 > len_w1:
        word_2, word_1 = word_1, word_2
        len_w2, len_w1 = len_w1, len_w2

    cur_row = range(len_w2 + 1)

    for i in range(1, len_w1 + 1):
        prev_row = cur_row
        cur_row = [i] + [0] * len_w2
        for j in range(1, len_w2 + 1):
            add = prev_row[j] + 1
            delete = cur_row[j - 1] + 1
            change = prev_row[j - 1]

            if word_2[j - 1] != word_1[i - 1]:
                change += 1
            cur_row[j] = min(add, delete, change)

    return cur_row[len_w2]
