from typing import List, Dict, Union

class CostEstimator:
    """
    Estimates current vs optimized costs based on recommendations.
    Supports multiple resource types: Spark, Kubernetes, Cloud (VM, Storage, Network), Databases.
    """

    # Approximate hourly or monthly costs for different resource types
    COST_FACTORS = {
        "spark_executor": {"hourly": 0.45},
        "k8s_pod": {"hourly": 0.20},
        "cloud_vm": {"hourly": 0.60},         # avg per hour
        "cloud_storage": {"monthly_per_gb": 0.022},  # S3 Standard pricing as example
        "cloud_network_egress": {"monthly_per_tb": 90},  # AWS egress pricing
        "db_instance": {"hourly": 1.20}
    }

    def estimate_savings(self, recommendations: List[Dict]) -> Dict[str, Union[float, Dict]]:
        """
        Estimate savings across all recommendation types.

        Returns:
            Dict containing total and category-wise savings.
        """
        totals = {
            "total_current_monthly": 0,
            "total_optimized_monthly": 0,
            "monthly_saving": 0,
            "details": {
                "Spark": {"current": 0, "optimized": 0},
                "Kubernetes": {"current": 0, "optimized": 0},
                "Cloud_VM": {"current": 0, "optimized": 0},
                "Cloud_Storage": {"current": 0, "optimized": 0},
                "Cloud_Network": {"current": 0, "optimized": 0},
                "Database": {"current": 0, "optimized": 0},
            }
        }

        for rec in recommendations:
            res_type = rec["type"]
            action = rec["action"]
            details = rec.get("details", "")

            if res_type == "Spark":
                current_cost = self.COST_FACTORS["spark_executor"]["hourly"] * 24 * 30
                optimized_cost = current_cost * 0.5
                totals["details"]["Spark"]["current"] += current_cost
                totals["details"]["Spark"]["optimized"] += optimized_cost

            elif res_type == "Kubernetes":
                current_cost = self.COST_FACTORS["k8s_pod"]["hourly"] * 24 * 30
                optimized_cost = current_cost * 0.6
                totals["details"]["Kubernetes"]["current"] += current_cost
                totals["details"]["Kubernetes"]["optimized"] += optimized_cost

            elif res_type == "Cloud" and rec["category"] == "VM":
                current_cost = self.COST_FACTORS["cloud_vm"]["hourly"] * 24 * 30
                optimized_cost = current_cost * 0.4  # More aggressive saving for unused VMs
                totals["details"]["Cloud_VM"]["current"] += current_cost
                totals["details"]["Cloud_VM"]["optimized"] += optimized_cost

            elif res_type == "Cloud" and rec["category"] == "Storage":
                try:
                    gb_match = [x for x in details.split(", ") if "Size:" in x]
                    if gb_match:
                        gb = float(gb_match[0].split(":")[1].strip("GB"))
                        current_cost = self.COST_FACTORS["cloud_storage"]["monthly_per_gb"] * gb
                        optimized_cost = current_cost * 0.2  # Archive or delete
                        totals["details"]["Cloud_Storage"]["current"] += current_cost
                        totals["details"]["Cloud_Storage"]["optimized"] += optimized_cost
                except Exception as e:
                    print(f"Error parsing storage cost: {e}")

            elif res_type == "Cloud" and rec["category"] == "Network":
                try:
                    tb_match = [x for x in details.split(", ") if "Egress:" in x]
                    if tb_match:
                        tb = float(tb_match[0].split(":")[1].strip("TB"))
                        current_cost = self.COST_FACTORS["cloud_network_egress"]["monthly_per_tb"] * tb
                        optimized_cost = current_cost * 0.6
                        totals["details"]["Cloud_Network"]["current"] += current_cost
                        totals["details"]["Cloud_Network"]["optimized"] += optimized_cost
                except Exception as e:
                    print(f"Error parsing network cost: {e}")

            elif res_type == "Database":
                current_cost = self.COST_FACTORS["db_instance"]["hourly"] * 24 * 30
                optimized_cost = current_cost * 0.5
                totals["details"]["Database"]["current"] += current_cost
                totals["details"]["Database"]["optimized"] += optimized_cost

        # Aggregate totals
        totals["total_current_monthly"] = sum(
            val["current"] for val in totals["details"].values()
        )
        totals["total_optimized_monthly"] = sum(
            val["optimized"] for val in totals["details"].values()
        )

        totals["monthly_saving"] = totals["total_current_monthly"] - totals["total_optimized_monthly"]

        return totals