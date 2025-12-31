import scipy.stats as stats

def invert_mean_value(value, mean, higher_is_worse=True):
    if not higher_is_worse:
        value = -value
        mean = -mean  # Invert mean for consistency

    return mean, value

def calculate_z_score(value, mean, std_dev, higher_is_worse=True):
    mean, value = invert_mean_value(value, mean, higher_is_worse)
    return (value - mean) / std_dev

def calculate_t_score(value, mean, std_dev, higher_is_worse=True):
    mean, value = invert_mean_value(value, mean, higher_is_worse)
    z_score = calculate_z_score(value, mean, std_dev)
    t_score = 50 + 10*z_score
    return t_score

def calculate_percentile(value, mean, std_dev, higher_is_worse=True):
    mean, value = invert_mean_value(value, mean, higher_is_worse)
    return stats.norm.cdf((value - mean) / std_dev) * 100

def calculate_quintile(percentile):
    return int(percentile // 20) + 1

def calculate_zero_quintile(percentile):
    return (int(percentile // 20) + 1) - 3

def calculate_zero_decile(percentile):
    return (int(percentile // 10) + 1) - 6

def get_quintile(value, mean, std_dev, higher_is_worse=True):
    percentile = calculate_percentile(value, mean, std_dev)
    quintile = calculate_quintile(percentile)
    return quintile

def calc_stats(value, mean, std_dev, higher_is_worse=True):
    z_score = calculate_z_score(value, mean, std_dev, higher_is_worse)
    t_score = calculate_t_score(value, mean, std_dev, higher_is_worse)
    percentile = calculate_percentile(value, mean, std_dev, higher_is_worse)
    quinitile = calculate_zero_quintile(percentile)
    decile = calculate_zero_decile(percentile)

    return { 'z_score': z_score, 't_score': t_score, 'percentile': percentile, 'quintile': quinitile, 'decile': decile }

# Example usage

print(f"First word: {calc_stats(24, 12, 2.5)}")
print(f"2 words Phrase: {calc_stats(24, 24, 3.5)}")
print(f"Understood directions: {calc_stats(24 ,21, 2.5)}")
print(f"Walked alone: {calc_stats(14, 13.5, 2)}")
print(f"Toilet trained: {calc_stats(32, 30, 6)}")
print(f"Crying level: {calc_stats(0.1, 2.5, 1)}")
