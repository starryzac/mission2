/**
 * 第2题：计算平均值
 * 输入三个整数，输出平均值（保留两位小数）
 */
#include <stdio.h>

double average_of_three(int a, int b, int c) {
    return (a + b + c) / 3.0;
}

int main() {
    printf("=== 第2题：计算平均值 ===\n\n");

    /* 测试用例1：样例 */
    printf("测试1 — 输入: 20 42 55\n");
    printf("  输出: %.2f (期望: 39.00)\n", average_of_three(20, 42, 55));

    /* 测试用例2：全零 */
    printf("\n测试2 — 输入: 0 0 0\n");
    printf("  输出: %.2f (期望: 0.00)\n", average_of_three(0, 0, 0));

    /* 测试用例3：负数 */
    printf("\n测试3 — 输入: -10 0 10\n");
    printf("  输出: %.2f (期望: 0.00)\n", average_of_three(-10, 0, 10));

    /* 测试用例4：不能整除的情况 */
    printf("\n测试4 — 输入: 1 2 4\n");
    printf("  输出: %.2f (期望: 2.33)\n", average_of_three(1, 2, 4));

    /* 测试用例5：大数 */
    printf("\n测试5 — 输入: 100 200 300\n");
    printf("  输出: %.2f (期望: 200.00)\n", average_of_three(100, 200, 300));

    /* --- 交互式输入 --- */
    printf("\n--- 交互测试：请输入三个整数（空格分隔）---\n");
    int x, y, z;
    scanf("%d %d %d", &x, &y, &z);
    printf("平均值: %.2f\n", average_of_three(x, y, z));

    return 0;
}
