def generate_quality_report(total, valid, invalid):

    return {
        "total_records": total,
        "valid_records": valid,
        "invalid_records": invalid,
        "quality_percentage": round(
            (valid / total) * 100,
            2
        )
        if total > 0
        else 0
    }