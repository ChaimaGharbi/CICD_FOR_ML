import json
import requests


def fetch_remote_metrics(url, output_file):
    """Fetch metrics from a remote URL and save to a local file."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to fetch remote metrics: {response.status_code}")


def load_metrics(file_path):
    """Load metrics from a JSON file."""
    with open(file_path) as f:
        return json.load(f)


def compare_metrics(local_metrics, remote_metrics):
    """Compare local and remote metrics and return a comparison dictionary."""
    comparison = {}
    all_keys = set(local_metrics.keys()).union(set(remote_metrics.keys()))

    for key in all_keys:
        local_value = local_metrics.get(key, "N/A")
        remote_value = remote_metrics.get(key, "N/A")
        comparison[key] = {"Local": local_value, "Remote": remote_value}

    return comparison


def generate_report(comparison, report_file):
    """Generate a Markdown report from the comparison dictionary."""
    with open(report_file, "w") as f:
        f.write("# Metrics Comparison Report\n\n")
        f.write("## Comparison\n")
        for key, values in comparison.items():
            f.write(
                f"- **{key}**: Local={values['Local']}, Remote={values['Remote']}\n"
            )


def main():
    remote_url = (
        "https://huggingface.co/ChaimaGharbi/Drug-Classification/raw/main/metrics.json"
    )
    remote_file = "Results/remote_metrics.json"
    local_file = "Results/metrics.json"
    report_file = "report.md"

    try:
        # Fetch remote metrics
        fetch_remote_metrics(remote_url, remote_file)

        # Load metrics
        local_metrics = load_metrics(local_file)
        remote_metrics = load_metrics(remote_file)

        # Compare metrics
        comparison = compare_metrics(local_metrics, remote_metrics)

        # Generate report
        generate_report(comparison, report_file)

        print(f"Report generated: {report_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
