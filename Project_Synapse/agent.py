
import random
import tools

class DecisionLog:
    def __init__(self):
        self.steps = []

    def add(self, what, why, result):
        self.steps.append({"what": what, "why": why, "result": result})

    def show(self):
        print("\n--- DECISION LOG ---")
        for i, step in enumerate(self.steps, start=1):
            print(f"Step {i}:")
            print(f"  What: {step['what']}")
            print(f"  Why: {step['why']}")
            print(f"  Result: {step['result']}")
        print("---------------------\n")


class Agent:
    def __init__(self):
        self.log = DecisionLog()

    def handle_scenario(self, scenario):
        self.log = DecisionLog()
        s = scenario.lower()
        if "restaurant" in s or "kitchen" in s:
            self._handle_restaurant_delay()
        elif "traffic" in s or "accident" in s:
            self._handle_traffic_issue()
        elif "damaged" in s or "package" in s:
            self._handle_dispute()
        elif "recipient" in s or "not home" in s or "unavailable" in s:
            self._handle_recipient_unavailable()
        else:
            print("❌ No matching scenario type found.")
            return
        self.log.show()

    def _handle_restaurant_delay(self):
        status = tools.get_merchant_status()
        self.log.add("get_merchant_status", "Suspected kitchen delay", status)
        if status.get("prep_time_min", 0) >= 30:
            notif = tools.notify_customer(f"ORDER{random.randint(100,999)}", f"Kitchen delay ~{status['prep_time_min']} min at {status['name']}.", voucher=True)
            self.log.add("notify_customer", "Proactively inform customer", notif)
            reroute = tools.re_route_driver(interim_job="short nearby delivery")
            self.log.add("re_route_driver", "Avoid driver idle time", reroute)
            alt = tools.get_nearby_merchants(status["name"].split()[0], 20)
            self.log.add("get_nearby_merchants", "Offer faster alternative", alt)

    def _handle_traffic_issue(self):
        traffic = tools.check_traffic()
        self.log.add("check_traffic", "Check random route", traffic)
        if traffic.get("status") == "Blocked":
            parts = traffic["route"].split("-")
            origin = parts[0]
            destination = parts[1] if len(parts) > 1 else "Airport"
            new_route = tools.calculate_alternative_route(origin, destination)
            self.log.add("calculate_alternative_route", "Find faster detour", new_route)
            notify = tools.notify_customer(f"TRIP{random.randint(10,99)}", "We've found a faster route!", voucher=False)
            self.log.add("notify_customer", "Inform passenger", notify)

    def _handle_dispute(self):
        mediation = tools.initiate_mediation_flow(f"ORDER{random.randint(100,999)}")
        self.log.add("initiate_mediation_flow", "Start mediation", mediation)
        evidence = tools.collect_evidence(mediation["order_id"])
        self.log.add("collect_evidence", "Gather evidence", evidence)
        analysis = tools.analyze_evidence(evidence)
        self.log.add("analyze_evidence", "Analyze evidence", analysis)
        if analysis["result"] == "Merchant fault":
            refund = tools.issue_instant_refund(mediation["order_id"], 15.0)
            self.log.add("issue_instant_refund", "Refund customer", refund)
            exonerate = tools.exonerate_driver()
            self.log.add("exonerate_driver", "Clear driver", exonerate)
            merchant = tools.get_merchant_status()
            feedback = tools.log_merchant_packaging_feedback(merchant["merchant_id"], "Damaged packaging reported")
            self.log.add("log_merchant_packaging_feedback", "Log merchant issue", feedback)

    def _handle_recipient_unavailable(self):
        contact = tools.contact_recipient_via_chat(f"JOB{random.randint(100,999)}", "Delivery arrived, are you available?")
        self.log.add("contact_recipient_via_chat", "Try to contact recipient", contact)
        if contact["response"] == "No answer":
            locker = tools.find_nearby_locker()
            if locker["ok"]:
                self.log.add("find_nearby_locker", "Offer locker drop-off", locker)
            else:
                self.log.add("reschedule_delivery", "No lockers available", {"ok": True, "status": "Rescheduled"})

if __name__ == "__main__":
    agent = Agent()
    print("🚚 Project Synapse Demo — Interactive Mode")
    print("Type a scenario and press Enter. Type 'quit' to exit.\n")
    while True:
        scenario = input("Enter scenario: ").strip()
        if scenario.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        if not scenario:
            continue
        agent.handle_scenario(scenario)
