/**
 * 第5题：无向加权图最大成功概率路径
 * 给定无向图，每条边有成功概率，求起点到终点最大成功概率路径。
 * 使用 Dijkstra 算法变种（最大概率），用邻接表 + 二叉堆实现。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#define MAX_N 1000
#define MAX_M 5000

/* 邻接表边 */
typedef struct Edge {
    int to;
    double prob;
    struct Edge *next;
} Edge;

Edge *adj[MAX_N];
int edge_count = 0;
Edge edge_pool[MAX_M * 2];  /* 无向图，每条边存两次 */

void add_edge(int u, int v, double prob) {
    Edge *e1 = &edge_pool[edge_count++];
    e1->to = v;
    e1->prob = prob;
    e1->next = adj[u];
    adj[u] = e1;

    Edge *e2 = &edge_pool[edge_count++];
    e2->to = u;
    e2->prob = prob;
    e2->next = adj[v];
    adj[v] = e2;
}

/* 最大堆（按概率） */
typedef struct {
    int node;
    double prob;
} HeapNode;

typedef struct {
    HeapNode data[MAX_M * 4];
    int size;
} MaxHeap;

void heap_push(MaxHeap *h, int node, double prob) {
    int i = h->size++;
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (h->data[parent].prob >= prob) break;
        h->data[i] = h->data[parent];
        i = parent;
    }
    h->data[i].node = node;
    h->data[i].prob = prob;
}

HeapNode heap_pop(MaxHeap *h) {
    HeapNode top = h->data[0];
    HeapNode last = h->data[--h->size];
    int i = 0;
    while (1) {
        int left = 2 * i + 1, right = 2 * i + 2;
        int largest = i;
        if (left < h->size && h->data[left].prob > h->data[largest].prob)
            largest = left;
        if (right < h->size && h->data[right].prob > h->data[largest].prob)
            largest = right;
        if (largest == i) break;
        h->data[i] = h->data[largest];
        i = largest;
    }
    h->data[i] = last;
    return top;
}

double max_probability(int n, int start, int end) {
    double dist[MAX_N];
    int visited[MAX_N] = {0};
    for (int i = 0; i < n; i++) dist[i] = 0.0;
    dist[start] = 1.0;

    MaxHeap heap = {.size = 0};
    heap_push(&heap, start, 1.0);

    while (heap.size > 0) {
        HeapNode cur = heap_pop(&heap);
        int u = cur.node;

        if (visited[u]) continue;
        visited[u] = 1;

        if (u == end) return dist[end];

        for (Edge *e = adj[u]; e != NULL; e = e->next) {
            int v = e->to;
            double new_prob = dist[u] * e->prob;
            if (new_prob > dist[v]) {
                dist[v] = new_prob;
                heap_push(&heap, v, new_prob);
            }
        }
    }

    return 0.0;  /* 不可达 */
}

void reset_graph(int n) {
    edge_count = 0;
    for (int i = 0; i < n; i++) adj[i] = NULL;
}

int main() {
    printf("=== 第5题：无向加权图最大成功概率路径 ===\n\n");

    /* 测试用例1：样例1 */
    printf("测试1 — 样例1:\n");
    printf("  图: 3节点3边, 起点0终点2\n");
    printf("  边: 0-1(0.5), 1-2(0.5), 0-2(0.2)\n");
    {
        reset_graph(3);
        add_edge(0, 1, 0.5);
        add_edge(1, 2, 0.5);
        add_edge(0, 2, 0.2);
        double res = max_probability(3, 0, 2);
        printf("  最大概率: %.5f (期望: 0.25000)\n", res);
    }

    /* 测试用例2：样例2 */
    printf("\n测试2 — 样例2（改概率0.2→0.3）:\n");
    {
        reset_graph(3);
        add_edge(0, 1, 0.5);
        add_edge(1, 2, 0.5);
        add_edge(0, 2, 0.3);
        double res = max_probability(3, 0, 2);
        printf("  最大概率: %.5f (期望: 0.30000，直接走0-2)\n", res);
    }

    /* 测试用例3：不可达 */
    printf("\n测试3 — 不可达（孤立节点）:\n");
    {
        reset_graph(4);
        add_edge(0, 1, 0.8);
        add_edge(1, 2, 0.9);
        /* 节点3孤立 */
        double res = max_probability(4, 0, 3);
        printf("  最大概率: %.5f (期望: 0.00000)\n", res);
    }

    /* 测试用例4：单条边 */
    printf("\n测试4 — 只有一条直接边:\n");
    {
        reset_graph(5);
        add_edge(0, 4, 0.75);
        double res = max_probability(5, 0, 4);
        printf("  最大概率: %.5f (期望: 0.75000)\n", res);
    }

    /* 测试用例5：多条路径取最大 */
    printf("\n测试5 — 五节点图，对比两条路径:\n");
    {
        reset_graph(5);
        /* 路径1: 0-1-2-3-4 = 0.9*0.9*0.9*0.9 = 0.6561 */
        add_edge(0, 1, 0.9);
        add_edge(1, 2, 0.9);
        add_edge(2, 3, 0.9);
        add_edge(3, 4, 0.9);
        /* 路径2: 直接 0-4 = 0.7 */
        add_edge(0, 4, 0.7);
        double res = max_probability(5, 0, 4);
        printf("  最大概率: %.5f (期望: 0.70000)\n", res);
    }

    /* --- 交互式输入 --- */
    printf("\n--- 交互测试 ---\n");
    printf("请输入: n m start end\n");
    int n, m, start, end;
    scanf("%d %d %d %d", &n, &m, &start, &end);
    reset_graph(n);

    printf("请输入 %d 个概率值: ", m);
    double probs[MAX_M];
    for (int i = 0; i < m; i++) {
        scanf("%lf", &probs[i]);
    }

    printf("请输入 %d 条边 (每行两个整数 u v):\n", m);
    for (int i = 0; i < m; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        add_edge(u, v, probs[i]);
    }

    double result = max_probability(n, start, end);
    printf("最大成功概率: %.8f\n", result);

    return 0;
}
