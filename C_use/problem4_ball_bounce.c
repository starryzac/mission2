/**
 * 第4题：皮球弹跳问题
 * 皮球从初始高度自由落下，每次反弹到原高度的一半。
 * 求第n次落地时经过的总距离和第n次反弹高度。
 */
#include <stdio.h>

void ball_bounce(double height, int n, double *total_dist, double *rebound) {
    *total_dist = 0.0;
    *rebound = 0.0;

    if (n <= 0) return;

    double h = (double)height;

    /* 第1次落地：只下落 */
    *total_dist = h;
    *rebound = h / 2.0;

    /* 第2到第n次落地：每次上弹+下落 */
    for (int i = 2; i <= n; i++) {
        *total_dist += 2.0 * (*rebound);
        *rebound /= 2.0;
    }
}

int main() {
    printf("=== 第4题：皮球弹跳问题 ===\n\n");

    double dist, rebound;

    /* 测试用例1：样例 */
    printf("测试1 — 输入: 10 2\n");
    ball_bounce(10, 2, &dist, &rebound);
    printf("  输出: %.1f %.1f (期望: 20.0 2.5)\n", dist, rebound);

    /* 测试用例2：n=1 */
    printf("\n测试2 — 输入: 10 1\n");
    ball_bounce(10, 1, &dist, &rebound);
    printf("  输出: %.1f %.1f (期望: 10.0 5.0)\n", dist, rebound);

    /* 测试用例3：n=3 */
    printf("\n测试3 — 输入: 10 3\n");
    ball_bounce(10, 3, &dist, &rebound);
    printf("  输出: %.1f %.1f (期望: 25.0 1.3)\n", dist, rebound);
    /*
     * 验算: 第1次落地=10, 反弹=5
     *       第2次落地: +10(上5下5)=20, 反弹=2.5
     *       第3次落地: +5(上2.5下2.5)=25, 反弹=1.25 → 1.3(四舍五入)
     */

    /* 测试用例4：大高度 */
    printf("\n测试4 — 输入: 100 4\n");
    ball_bounce(100, 4, &dist, &rebound);
    printf("  输出: %.1f %.1f\n", dist, rebound);
    /*
     * 验算: 第1次=100, 反弹=50
     *       第2次: +100=200, 反弹=25
     *       第3次: +50=250, 反弹=12.5
     *       第4次: +25=275, 反弹=6.25 → 6.3
     * 输出应为: 275.0 6.3
     */

    /* 测试用例5：n=0（边界） */
    printf("\n测试5 — 输入: 10 0 (边界情况)\n");
    ball_bounce(10, 0, &dist, &rebound);
    printf("  输出: %.1f %.1f (期望: 0.0 0.0)\n", dist, rebound);

    /* --- 交互式输入 --- */
    printf("\n--- 交互测试：请输入初始高度和n ---\n");
    double h;
    int n;
    scanf("%lf %d", &h, &n);
    ball_bounce(h, n, &dist, &rebound);
    printf("结果: %.1f %.1f\n", dist, rebound);

    return 0;
}
