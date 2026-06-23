def knapsack(tasks, capacity):
    dp = [0] * (capacity + 1)
    for task in tasks:
        hours = task["Duration"]
        score = task["Impact"]
        for w in range(capacity, hours - 1, -1):
            dp[w] = max(
                dp[w],
                dp[w - hours] + score
            )
    return dp[capacity]