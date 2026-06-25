from mycelium.core.human_review_ui import list_pending_reviews, view_request
from mycelium.core.constitution_human_override import set_decision
from mycelium.core.constitution_human_resume import resume_with_human_decision

import json


def show_queue():
    items = list_pending_reviews()

    print("\n🧠 HUMAN REVIEW QUEUE")
    print("=" * 40)

    for i in items:
        print(f"- {i['request_id']}")
        print(f"  proposal: {i['proposal_id']}")
        print(f"  status: {i['status']}")
        print()


def inspect(request_id):
    data = view_request(request_id)
    print(json.dumps(data, indent=2))


def approve(request_id, reason="approved"):
    set_decision(request_id, "approve", reason)
    return resume_with_human_decision(request_id)


def reject(request_id, reason="rejected"):
    set_decision(request_id, "reject", reason)
    return {"status": "rejected"}


from mycelium.core.governance_replay_view import print_timeline


def replay():
    print_timeline()


from mycelium.core.constitution_diff_pipeline import explain_version_change


def diff(old, new):
    return explain_version_change(int(old), int(new))


from mycelium.core.policy_sandbox_analysis import analyze_change


def sandbox(change):
    return analyze_change(change)
