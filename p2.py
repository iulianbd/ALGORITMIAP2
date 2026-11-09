from typing import Any, Dict, List, Tuple, Optional
import random

# =============================================================================
# I. PROBLEMA DEL CAMBIO DE MONEDAS
# =============================================================================

def greedy_change(coins: List[int], amount: int) -> Tuple[List[int], int]:
    if amount < 0:
        raise ValueError("amount no puede ser negativo")

    selected: List[int] = []
    remainder: int = amount

    for coin in sorted(coins, reverse=True):
        if coin > remainder:
            continue
        count: int = remainder // coin
        selected.extend([coin] * count)
        remainder -= coin * count
        if remainder == 0:
            break

    return selected, remainder


def optimal_change(coins: List[int], amount: int) -> List[int] | None:
    if amount < 0:
        raise ValueError("amount no puede ser negativo")
    if amount == 0:
        return []

    sorted_coins: List[int] = sorted(set(coins), reverse=True)

    INF: float = float("inf")
    min_coins: List[float] = [0] + [INF] * amount

    for a in range(1, amount + 1):
        for coin in sorted_coins:
            if coin <= a and min_coins[a - coin] + 1 < min_coins[a]:
                min_coins[a] = min_coins[a - coin] + 1

    if min_coins[amount] == INF:
        return None

    result: List[int] = []
    remaining: int = amount
    while remaining > 0:
        for coin in sorted_coins:
            if coin <= remaining and min_coins[remaining - coin] == min_coins[remaining] - 1:
                result.append(coin)
                remaining -= coin
                break

    return result


def compare_change(coins: List[int], max_amount: int) -> Dict[str, List[int]]:
    result: Dict[str, List[int]] = {
        "optimal": [],
        "suboptimal": [],
        "greedy_failed": [],
        "impossible": [],
    }

    for amount in range(1, max_amount + 1):
        greedy_selected, remainder = greedy_change(coins, amount)
        best: List[int] | None = optimal_change(coins, amount)

        if best is None:
            result["impossible"].append(amount)
        elif remainder != 0:
            result["greedy_failed"].append(amount)
        elif len(greedy_selected) == len(best):
            result["optimal"].append(amount)
        else:
            result["suboptimal"].append(amount)

    return result

# =============================================================================
# II. SELECCION DE ACTIVIDADES
# =============================================================================

def activity_selection(activities: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    sorted_activities = sorted(activities, key=lambda x: (x[2], x[1], x[0]))
    
    selected_activities = []
    last_end_time = -1
    
    for activity in sorted_activities:
        if activity[1] >= last_end_time:
            selected_activities.append(activity)
            last_end_time = activity[2]
            
    return selected_activities


def generate_activities(n: int, seed: int = 42) -> List[Tuple[str, int, int]]:
    random.seed(seed) 
    
    activities = []
    for i in range(n):
        identificador = f"A{i}"
        start = random.randint(0, 10000)
        duration = random.randint(1, 100)
        end = start + duration
        
        activities.append((identificador, start, end))
        
    return activities

# =============================================================================
# III. PLANIFICACION DE TAREAS CON FECHAS LIMITE
# =============================================================================

def job_scheduling(
    jobs: List[Tuple[str, int, int]]
) -> Tuple[List[Optional[Tuple[str, int, int]]], int]:
    
    if not jobs:
        return [], 0
        
    max_deadline = max(job[2] for job in jobs)
    
    schedule = [None] * max_deadline
    total_profit = 0
    
    sorted_jobs = sorted(jobs, key=lambda x: (-x[1], x[2], x[0]))
    
    for job in sorted_jobs:
        deadline = job[2]
        
        for i in range(deadline - 1, -1, -1):
            if schedule[i] is None:
                schedule[i] = job
                total_profit += job[1]
                break
                
    return schedule, total_profit

def generate_jobs(n: int, seed: int = 42) -> List[Tuple[str, int, int]]:
    random.seed(seed)
    
    jobs = []
    max_dl = max(1, n // 10)
    
    for i in range(n):
        identificador = f"J{i}"
        profit = random.randint(1, 1000)
        deadline = random.randint(1, max_dl)
        
        jobs.append((identificador, profit, deadline))
        
    return jobs