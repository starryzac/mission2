/**
 * 第3题：图像旋转
 * 将 n×m 矩阵顺时针旋转90度后输出
 * 规律：a[i][j] → b[j][n-1-i]
 */
#include <stdio.h>

#define MAX_N 100
#define MAX_M 100

void rotate_clockwise(int src[MAX_N][MAX_M], int n, int m, int dst[MAX_M][MAX_N]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            dst[j][n - 1 - i] = src[i][j];
        }
    }
}

void print_matrix(int mat[][MAX_N], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (j > 0) printf(" ");
            printf("%d", mat[i][j]);
        }
        printf("\n");
    }
}

int main() {
    printf("=== 第3题：图像旋转 ===\n\n");

    /* 测试用例1：样例 (2×3) */
    printf("测试1 — 2×3 矩阵:\n");
    printf("  输入:\n");
    printf("    2 3\n");
    printf("    1 5 3\n");
    printf("    3 2 4\n");
    {
        int src[MAX_N][MAX_M] = {{1, 5, 3}, {3, 2, 4}};
        int dst[MAX_M][MAX_N];
        rotate_clockwise(src, 2, 3, dst);
        printf("  输出 (期望: 3 1 / 2 5 / 4 3):\n");
        print_matrix(dst, 3, 2);
    }

    /* 测试用例2：正方形矩阵 (3×3) */
    printf("\n测试2 — 3×3 矩阵:\n");
    {
        int src[MAX_N][MAX_M] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        int dst[MAX_M][MAX_N];
        rotate_clockwise(src, 3, 3, dst);
        printf("  输入:\n");
        print_matrix(src, 3, 3);
        printf("  输出 (期望: 7 4 1 / 8 5 2 / 9 6 3):\n");
        print_matrix(dst, 3, 3);
    }

    /* 测试用例3：单列矩阵 (3×1) */
    printf("\n测试3 — 3×1 矩阵（单列）:\n");
    {
        int src[MAX_N][MAX_M] = {{1}, {2}, {3}};
        int dst[MAX_M][MAX_N];
        rotate_clockwise(src, 3, 1, dst);
        printf("  输出 (期望: 3 2 1 在一行):\n");
        print_matrix(dst, 1, 3);
    }

    /* 测试用例4：单行矩阵 (1×4) */
    printf("\n测试4 — 1×4 矩阵（单行）:\n");
    {
        int src[MAX_N][MAX_M] = {{5, 6, 7, 8}};
        int dst[MAX_M][MAX_N];
        rotate_clockwise(src, 1, 4, dst);
        printf("  输出 (期望: 4行1列 5/6/7/8):\n");
        print_matrix(dst, 4, 1);
    }

    /* --- 交互式输入 --- */
    printf("\n--- 交互测试 ---\n");
    printf("请输入 n 和 m: ");
    int n, m;
    scanf("%d %d", &n, &m);
    int user_src[MAX_N][MAX_M];
    int user_dst[MAX_M][MAX_N];
    printf("请输入 %d 行，每行 %d 个整数:\n", n, m);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            scanf("%d", &user_src[i][j]);
        }
    }
    rotate_clockwise(user_src, n, m, user_dst);
    printf("旋转后:\n");
    print_matrix(user_dst, m, n);

    return 0;
}
