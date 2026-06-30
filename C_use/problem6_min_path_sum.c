/**
 * 第6题：矩阵的最小路径和
 * 给定 n×m 矩阵，从左上角到右下角，每次只能向右或向下，
 * 求最小路径和。使用动态规划 O(n*m)。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 500
#define MAX_M 500

int min_path_sum(int matrix[MAX_N][MAX_M], int n, int m) {
    int dp[MAX_M];  /* 一维DP数组优化空间 */

    /* 初始化第一行 */
    dp[0] = matrix[0][0];
    for (int j = 1; j < m; j++) {
        dp[j] = dp[j - 1] + matrix[0][j];
    }

    /* 逐行递推 */
    for (int i = 1; i < n; i++) {
        dp[0] += matrix[i][0];  /* 第一列只能从上方来 */
        for (int j = 1; j < m; j++) {
            dp[j] = matrix[i][j] + (dp[j] < dp[j - 1] ? dp[j] : dp[j - 1]);
        }
    }

    return dp[m - 1];
}

/**
 * 解析矩阵格式字符串，如 "[[1,2,3],[1,2,3]]"
 * 返回实际读取的行数，n和m通过指针返回
 */
int parse_matrix(const char *s, int matrix[MAX_N][MAX_M], int *n, int *m) {
    int row = -1, col = 0, num = 0;
    int has_num = 0;
    *m = 0;

    for (const char *p = s; *p; p++) {
        if (*p >= '0' && *p <= '9') {
            num = num * 10 + (*p - '0');
            has_num = 1;
        } else {
            if (has_num) {
                if (row == 0) (*m)++;  /* 第一行时统计列数 */
                matrix[row][col++] = num;
                num = 0;
                has_num = 0;
            }
            if (*p == '[') {
                if (p == s) continue;     /* 最外层 [[，跳过 */
                row++;                     /* 每个内层 [ 表示新一行开始 */
                col = 0;
            }
        }
    }

    *n = row + 1;  /* row是0-based索引，行数=row+1 */
    return 1;
}

int main() {
    printf("=== 第6题：矩阵的最小路径和 ===\n\n");

    int matrix[MAX_N][MAX_M];
    int n, m;

    /* 测试用例1：样例 [[1,2,3],[1,2,3]] */
    printf("测试1 — 输入: [[1,2,3],[1,2,3]]\n");
    parse_matrix("[[1,2,3],[1,2,3]]", matrix, &n, &m);
    printf("  矩阵: %d×%d\n", n, m);
    printf("  输出: %d (期望: 7)\n", min_path_sum(matrix, n, m));
    /* 路径: 1→2→3→2→3 = 11? No...
     * 路径: 1→1→2→2→3 = 9? Let me check:
     * Actually: dp calculation:
     * [1, 3, 6]
     * [2, 3, 5]  wait let me trace properly
     * 1 2 3
     * 1 2 3
     * dp[0][0]=1, dp[0][1]=3, dp[0][2]=6
     * dp[1][0]=2, dp[1][1]=min(2,3)+2=4, dp[1][2]=min(4,6)+3=7
     * Output: 7. Yes, correct. Path: 1→1→2→3 (right then down-right-right) */

    /* 测试用例2：题目例子 [[1,3,5,9],[8,1,3,4],[5,0,6,1],[8,8,4,0]] */
    printf("\n测试2 — 输入: [[1,3,5,9],[8,1,3,4],[5,0,6,1],[8,8,4,0]]\n");
    parse_matrix("[[1,3,5,9],[8,1,3,4],[5,0,6,1],[8,8,4,0]]", matrix, &n, &m);
    printf("  矩阵: %d×%d\n", n, m);
    printf("  输出: %d (期望: 12)\n", min_path_sum(matrix, n, m));
    /* 路径: 1→3→1→0→6→1→0 = 12 */

    /* 测试用例3：单行 */
    printf("\n测试3 — 输入: [[1,2,3,4]]\n");
    parse_matrix("[[1,2,3,4]]", matrix, &n, &m);
    printf("  输出: %d (期望: 10)\n", min_path_sum(matrix, n, m));

    /* 测试用例4：单列 */
    printf("\n测试4 — 输入: [[5],[3],[2],[1]]\n");
    parse_matrix("[[5],[3],[2],[1]]", matrix, &n, &m);
    printf("  输出: %d (期望: 11)\n", min_path_sum(matrix, n, m));

    /* 测试用例5：1×1 */
    printf("\n测试5 — 输入: [[7]]\n");
    parse_matrix("[[7]]", matrix, &n, &m);
    printf("  输出: %d (期望: 7)\n", min_path_sum(matrix, n, m));

    /* 测试用例6：2×2 */
    printf("\n测试6 — 输入: [[1,4],[2,1]]\n");
    parse_matrix("[[1,4],[2,1]]", matrix, &n, &m);
    printf("  输出: %d (期望: 4，路径1→2→1)\n", min_path_sum(matrix, n, m));

    /* --- 交互式输入 --- */
    printf("\n--- 交互测试：请输入矩阵（格式如 [[1,2],[3,4]]）---\n");
    char input[8192];
    scanf("%s", input);
    parse_matrix(input, matrix, &n, &m);
    printf("矩阵大小: %d×%d\n", n, m);
    printf("最小路径和: %d\n", min_path_sum(matrix, n, m));

    return 0;
}
