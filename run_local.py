from orchestration.graph import run_task

if __name__ == "__main__":
    task = (
        "Summarize competitor positioning from our docs, "
        "draft a client-ready email, and create action items."
    )

    result = run_task(task)

    print("\n================ FINAL OUTPUT ================\n")
    print(result.get("final_output", ""))

    print("\n================ TRACE LOG ===================\n")
    for row in result.get("trace", []):
        print(
            f"- {row['step']:7} | {row['agent']:10} | "
            f"{row['action']} -> {row['outcome']}"
        )
