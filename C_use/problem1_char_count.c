/**
 * 第1题：字符统计
 * 输入5个字符，统计其中字符 'a' 的个数（大写 'A' 也算）
 */
#include <stdio.h>

int count_a(const char chars[], int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (chars[i] == 'a' || chars[i] == 'A') {
            count++;
        }
    }
    return count;
}

int main() {
    printf("=== 第1题：字符统计 ===\n\n");

    /* 测试用例1：样例1 */
    printf("测试1 — 输入: a b c d e\n");
    {
        char test[] = {'a', 'b', 'c', 'd', 'e'};
        printf("  输出: %d (期望: 1)\n", count_a(test, 5));
    }

    /* 测试用例2：样例2 */
    printf("\n测试2 — 输入: a A b c a\n");
    {
        char test[] = {'a', 'A', 'b', 'c', 'a'};
        printf("  输出: %d (期望: 3)\n", count_a(test, 5));
    }

    /* 测试用例3：全为a/A */
    printf("\n测试3 — 输入: A A a a A\n");
    {
        char test[] = {'A', 'A', 'a', 'a', 'A'};
        printf("  输出: %d (期望: 5)\n", count_a(test, 5));
    }

    /* 测试用例4：没有a */
    printf("\n测试4 — 输入: x y z w v\n");
    {
        char test[] = {'x', 'y', 'z', 'w', 'v'};
        printf("  输出: %d (期望: 0)\n", count_a(test, 5));
    }

    /* --- 交互式输入 --- */
    printf("\n--- 交互测试：请输入5个字符（空格分隔）---\n");
    char input[5];
    for (int i = 0; i < 5; i++) {
        scanf(" %c", &input[i]);  /* %c前加空格跳过空白字符 */
    }
    printf("结果: %d\n", count_a(input, 5));

    return 0;
}
