from datetime import date

# Week → (extra_sets, extra_reps) relative to the exercise base values
# Example: Push Up base is 3 sets × 8 reps
#   Week 1 → 3×8, Week 2 → 3×10, Week 3 → 4×10, Week 4 → 4×12 ...
OVERLOAD_SCHEDULE: dict[int, tuple[int, int]] = {
    1: (0, 0),
    2: (0, 2),
    3: (1, 2),
    4: (1, 4),
    5: (1, 4),   # consolidation
    6: (2, 2),
    7: (2, 4),
    8: (2, 6),
}

def get_current_week(plan_start: date, today: date) -> int:
    """Return the current training week (1–8) based on plan start date."""
    days_elapsed = max(0, (today - plan_start).days)
    week = (days_elapsed // 7) + 1
    return min(week, 8)

def apply_overload(base_sets: int, base_reps: int, week: int) -> tuple[int, int]:
    """Return (sets, reps) with overload modifier applied for the given week."""
    extra_sets, extra_reps = OVERLOAD_SCHEDULE.get(week, OVERLOAD_SCHEDULE[8])
    return base_sets + extra_sets, base_reps + extra_reps
