import pandas as pd
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import calendar
import os

def pie_plot(stat: Dict[str, Any], name: str, output_dir="figures"):
    os.makedirs(output_dir, exist_ok=True)
    labels, sizes = [], []
    for i, j in stat.items():
        labels.append(i)
        sizes.append(j)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title(f"{name} distribution")
    file_path = os.path.join(output_dir, f"{name}_pie.png")
    plt.savefig(file_path)
    plt.close()
    print(f"Saved pie chart: {file_path}")
    return file_path

def bar_chart(stat: Dict[str, Any], name: str, output_dir="figures"):
    os.makedirs(output_dir, exist_ok=True)
    x, values = [], []
    if name == 'day':
        x = list(calendar.day_name)
    elif name == 'month':
        x = list(calendar.month_name)
    else:
        x = [i for i in range(24)]
    for i in range(len(x)):
        values.append(stat[x[i]] if x[i] in stat else 0)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(x, values)
    plt.title(f"{name} distribution")
    if name == 'day' or name == 'month':
        plt.xticks(rotation=30, ha='right', fontsize=10)
        plt.tight_layout()
    file_path = os.path.join(output_dir, f"{name}_bar.png")
    plt.savefig(file_path)
    plt.close()
    print(f"Saved bar chart: {file_path}")
    return file_path

def analyze_url_stats(stats: List[Dict[str, Any]]) -> Dict[str, Any]:
    df = pd.DataFrame(stats)
    df = df.fillna(0)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    time_patterns = analyze_time_patterns(df)
    return {
        'total_visits': len(df),
        'unique_visitors': df['client_ip'].nunique(),
        'device_stats': df['device'].value_counts().to_dict(),
        'os_stats': df['os'].value_counts().to_dict(),
        'browser_stats': df['browser'].value_counts().to_dict(),
        'time_patterns': time_patterns,
    }

def analyze_time_patterns(df: pd.DataFrame) -> Dict[str, Any]:
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['month'] = df['timestamp'].dt.month
    df['week'] = df['timestamp'].dt.isocalendar().week

    time_patterns = {
        'hourly_distribution': df['hour'].value_counts().sort_index().fillna(0).to_dict(),
        'daily_distribution': df['day_of_week'].value_counts().reindex(list(calendar.day_name)).fillna(0).to_dict(),
        'monthly_distribution': df['month'].value_counts().sort_index().fillna(0).to_dict(),
        'peak_times': {
            'hour': df.groupby('hour')['id'].count().idxmax(),
            'day': df.groupby('day_of_week')['id'].count().idxmax(),
            'month': df.groupby('month')['id'].count().idxmax()
        },
        'weekly_trends': df.groupby(['week', 'day_of_week'])['id'].count().to_dict()
    }

    hourly_avg = df.groupby('hour')['id'].count().mean()
    time_patterns['busy_hours'] = df.groupby('hour')['id'].count()[
        df.groupby('hour')['id'].count() > hourly_avg * 1.2
    ].index.tolist()

    return time_patterns
def analyze(stats: List[Dict[str, Any]],id : str) -> Dict[str, Any]:
    out=rf"./figs/{id}"
    analytics = analyze_url_stats(stats)
    device_stats = pie_plot(analytics['device_stats'], 'device_dist',out)
    os_stats = pie_plot(analytics['os_stats'], 'os_dist',out)
    browser_stats = pie_plot(analytics['browser_stats'], 'browser_dist',out)
    hour_dist = bar_chart(analytics['time_patterns']['hourly_distribution'], 'hour',out)
    day_dist = bar_chart(analytics['time_patterns']['daily_distribution'], 'day',out)
    month_dist = bar_chart(analytics['time_patterns']['monthly_distribution'], 'month',out)
    return {
        'hour_chart':hour_dist ,
        'day_chart' : day_dist,
        'month_chart' : month_dist,
        'device_chart' : device_stats,
        'os_chart' : os_stats,
        'browser_chart' : browser_stats,
        'busy_hours' : analytics['time_patterns']['busy_hours']
    }
if __name__ == "__main__":
    sample_stats = [
        {
            "url_id": 1,
            "os": "Android",
            "browser": "Chrome",
            "timestamp": "2024-12-31T20:54:31",
            "device": "Mobile",
            "id": 1,
            "client_ip": "127.0.0.1"
        },
        {
            "url_id": 1,
            "os": "Android",
            "browser": "Chrome",
            "timestamp": "2024-12-31T19:54:34",
            "device": "Desktop",
            "id": 2,
            "client_ip": "127.0.0.1"
        },
        {
            "url_id": 1,
            "os": "Android",
            "browser": "Chrome",
            "timestamp": "2024-12-31T15:54:35",
            "device": "Mobile",
            "id": 3,
            "client_ip": "127.0.0.1"
        },
        {
            "url_id": 1,
            "os": "Android",
            "browser": "Chrome",
            "timestamp": "2024-12-31T07:54:37",
            "device": "Mobile",
            "id": 4,
            "client_ip": "127.0.0.1"
        },
        {
            "url_id": 1,
            "os": "Android",
            "browser": "Chrome",
            "timestamp": "2024-12-31T19:54:38",
            "device": "Mobile",
            "id": 5,
            "client_ip": "127.0.0.1"
        }
    ]
    out=r"D:\projects\backend\url-shortner\figs"
    analytics = analyze_url_stats(sample_stats)
    pie_plot(analytics['device_stats'], 'device_dist',out)
    pie_plot(analytics['os_stats'], 'os_dist',out)
    pie_plot(analytics['browser_stats'], 'browser_dist',out)
    bar_chart(analytics['time_patterns']['hourly_distribution'], 'hour',out)
    bar_chart(analytics['time_patterns']['daily_distribution'], 'day',out)
    bar_chart(analytics['time_patterns']['monthly_distribution'], 'month',out)
    print(analytics)
